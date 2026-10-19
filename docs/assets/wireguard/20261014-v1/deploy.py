#!/usr/bin/env python3
"""WireGuard live tutorial v1: exit first, relay second; no web credentials."""
import argparse, base64, datetime, ipaddress, json, os, pathlib, re, shlex, shutil, subprocess, sys, tempfile

VERSION = '20261014-v1'
WGDIR = pathlib.Path('/etc/wireguard')
STATE = WGDIR / 'wg-live-state.json'
BACKUPS = pathlib.Path('/root/wg-live-backups')
MARK = 51830
SUBNET = ipaddress.ip_network('10.77.0.0/30')

def run(args, capture=False, input=None, check=True):
    return subprocess.run(args, text=True, input=input, stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None, check=check)

def write(path, text, mode=0o600):
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    path.chmod(mode)

def parse(argv=None):
    p = argparse.ArgumentParser(description='英国出口 + 中转 WireGuard 配置')
    p.add_argument('mode', choices=['exit', 'relay', 'peer', 'exchange', 'status', 'pause', 'repair-addresses'])
    p.add_argument('--relay-ip')
    p.add_argument('--exit-ip')
    p.add_argument('--relay-ssh-port', type=int, default=22)
    p.add_argument('--exit-ssh-port', type=int, default=22)
    p.add_argument('--wg-port', type=int, default=51830)
    p.add_argument('--node-port', type=int, default=443)
    p.add_argument('--relay-public')
    p.add_argument('--dry-run', action='store_true', help='只检查参数，不执行安装')
    a = p.parse_args(argv)
    if a.mode in ['exit', 'relay', 'peer', 'repair-addresses']:
        for name in ['relay_ip', 'exit_ip']:
            try: value = ipaddress.IPv4Address(getattr(a, name))
            except (ValueError, TypeError, ipaddress.AddressValueError): p.error('请填写两台 VPS 的有效 IPv4')
            if value.is_unspecified or value.is_loopback or value.is_multicast: p.error('请填写 VPS 公网 IPv4')
        if a.relay_ip == a.exit_ip: p.error('中转与出口不能使用同一个 IP')
        for name in ['relay_ssh_port', 'exit_ssh_port', 'wg_port', 'node_port']:
            if not 1 <= getattr(a, name) <= 65535: p.error('端口范围必须为 1–65535')
        if a.node_port == a.relay_ssh_port: p.error('节点端口不能与中转 SSH 端口相同')
    if a.mode == 'peer': validate_key(a.relay_public)
    return a

def profile(a):
    return {k: getattr(a, k) for k in ['relay_ip', 'exit_ip', 'relay_ssh_port', 'exit_ssh_port', 'wg_port', 'node_port']}

def validate_key(value):
    try: valid = len(base64.b64decode(value, validate=True)) == 32
    except (ValueError, TypeError): valid = False
    if not valid: raise RuntimeError('WireGuard 密钥格式不正确')
    return value

def read_state():
    if not STATE.exists(): raise RuntimeError('未找到本教程部署记录，请先按页面部署')
    return json.loads(STATE.read_text())

def wg_config(role, p, private, psk, peer=None):
    iface = 'wg-relay' if role == 'exit' else 'wg-uk'
    text = f'''[Interface]
Address = {'10.77.0.1/30' if role == 'exit' else '10.77.0.2/30'}
ListenPort = {p['wg_port']}
PrivateKey = {validate_key(private)}
MTU = 1380
Table = off
PostUp = sysctl -q -w net.ipv4.conf.%i.rp_filter=2
'''
    if role == 'relay': text += f'PostUp = ip route replace default dev %i src 10.77.0.2 metric 10 table {MARK}\n'
    if peer:
        text += f'''
[Peer]
PublicKey = {validate_key(peer)}
PresharedKey = {validate_key(psk)}
AllowedIPs = {'10.77.0.2/32' if role == 'exit' else '0.0.0.0/0'}
Endpoint = {p['relay_ip'] if role == 'exit' else p['exit_ip']}:{p['wg_port']}
PersistentKeepalive = 25
'''
    return iface, text

def helper(role, p):
    peer = p['relay_ip'] if role == 'exit' else p['exit_ip']
    text = f'''#!/bin/sh
set -eu
PEER_IP='{peer}'
WG_PORT='{p['wg_port']}'
add_rule() {{
  table=$1; shift
  iptables -t "$table" -C "$@" 2>/dev/null || iptables -t "$table" -I "$@"
}}
iptables -N WG_LIVE_UDP 2>/dev/null || true
iptables -F WG_LIVE_UDP
iptables -A WG_LIVE_UDP -s "$PEER_IP/32" -j ACCEPT
iptables -A WG_LIVE_UDP -j DROP
add_rule filter INPUT -p udp --dport "$WG_PORT" -m comment --comment wg-live-udp -j WG_LIVE_UDP
'''
    if role == 'exit':
        text += '''WAN_IF=$(ip -4 route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++)if($i=="dev"){print $(i+1);exit}}')
WAN_SRC=$(ip -4 route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++)if($i=="src"){print $(i+1);exit}}')
test -n "$WAN_IF" && test -n "$WAN_SRC"
sysctl -q -w net.ipv4.ip_forward=1
iptables -N WG_LIVE_FWD 2>/dev/null || true
iptables -F WG_LIVE_FWD
iptables -A WG_LIVE_FWD -i wg-relay -o "$WAN_IF" -s 10.77.0.2/32 -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A WG_LIVE_FWD -i "$WAN_IF" -o wg-relay -d 10.77.0.2/32 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A WG_LIVE_FWD -i wg-relay -j DROP
iptables -A WG_LIVE_FWD -o wg-relay -j DROP
iptables -A WG_LIVE_FWD -j RETURN
add_rule filter FORWARD -m comment --comment wg-live-forward -j WG_LIVE_FWD
iptables -t nat -N WG_LIVE_NAT 2>/dev/null || true
iptables -t nat -F WG_LIVE_NAT
iptables -t nat -A WG_LIVE_NAT -s 10.77.0.2/32 -o "$WAN_IF" -j SNAT --to-source "$WAN_SRC"
add_rule nat POSTROUTING -m comment --comment wg-live-snat -j WG_LIVE_NAT
for dir in -i -o; do
  add_rule mangle FORWARD "$dir" wg-relay -p tcp --tcp-flags SYN,RST SYN -m comment --comment wg-live-mss -j TCPMSS --clamp-mss-to-pmtu
done
'''
    else:
        text += f'''ip route replace unreachable default metric 32767 table {MARK}
ip rule show | grep -q '10500:.*fwmark 0xca76.*lookup {MARK}' || ip rule add priority 10500 fwmark {MARK} table {MARK}
ip rule show | grep -q '10501:.*from 10.77.0.2.*lookup {MARK}' || ip rule add priority 10501 from 10.77.0.2/32 table {MARK}
add_rule filter OUTPUT -m mark --mark {MARK} ! -o wg-uk -m comment --comment wg-live-guard -j REJECT
add_rule filter OUTPUT -s 10.77.0.2/32 ! -o wg-uk -m comment --comment wg-live-source -j REJECT
'''
    return text

def prepare(role, p):
    os.umask(0o077)
    iface = 'wg-relay' if role == 'exit' else 'wg-uk'
    if STATE.exists():
        s = read_state()
        if s['role'] != role or s['profile'] != p or s.get('version') != VERSION:
            raise RuntimeError('已有部署使用其他参数；请先检查并恢复原出站，不会覆盖旧配置')
        return s
    if (WGDIR / (iface + '.conf')).exists(): raise RuntimeError(f'已有 {iface}.conf；本教程不会覆盖其他部署')
    osinfo = pathlib.Path('/etc/os-release').read_text()
    if not re.search(r'(?m)^ID=(?:"?)(ubuntu|debian)', osinfo): raise RuntimeError('当前脚本支持 Ubuntu / Debian')
    env = dict(os.environ, DEBIAN_FRONTEND='noninteractive')
    subprocess.run(['apt-get', 'update'], env=env, check=True)
    subprocess.run(['apt-get', 'install', '-y', '--no-install-recommends', 'wireguard-tools', 'iptables', 'curl', 'python3', 'openssh-client'], env=env, check=True)
    run(['modprobe', 'wireguard'])
    if run(['ss', '-H', '-lun', f'sport = :{p["wg_port"]}'], capture=True).stdout.strip(): raise RuntimeError('WireGuard UDP 端口已被占用')
    for line in run(['ip', '-4', 'route', 'show', 'table', 'main'], capture=True).stdout.splitlines():
        try: network = ipaddress.ip_network(line.split()[0], strict=False)
        except ValueError: continue
        if network.overlaps(SUBNET): raise RuntimeError('10.77.0.0/30 与已有网络重叠，请先调整网络规划')
    if role == 'relay':
        if re.search(r'(?m)^(10500|10501):', run(['ip', 'rule', 'show'], capture=True).stdout): raise RuntimeError('策略路由优先级已被其他配置占用')
        if run(['ip', '-4', 'route', 'show', 'table', str(MARK)], capture=True, check=False).stdout.strip(): raise RuntimeError('路由表 51830 已被占用')
    backup = BACKUPS / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True, mode=0o700)
    for name, cmd in [('iptables-before.txt', ['iptables-save']), ('rules-before.txt', ['ip', 'rule', 'show']), ('routes-before.txt', ['ip', 'route', 'show', 'table', 'all'])]:
        write(backup / name, run(cmd, capture=True).stdout)
    s = {'version': VERSION, 'role': role, 'profile': p, 'backup': str(backup), 'stage': 'prepared'}
    write(backup / 'forward-before.txt', run(['sysctl', '-n', 'net.ipv4.ip_forward'], capture=True).stdout)
    WGDIR.mkdir(mode=0o700, exist_ok=True)
    write(STATE, json.dumps(s, indent=2))
    return s

def keys():
    path = WGDIR / 'wg-live-private.key'
    if not path.exists(): write(path, run(['wg', 'genkey'], capture=True).stdout.strip() + '\n')
    public = run(['wg', 'pubkey'], capture=True, input=path.read_text()).stdout.strip()
    write(WGDIR / 'wg-live-public.key', public + '\n')
    return path.read_text().strip(), public

def install_network(s, private, psk, peer=None):
    role, p = s['role'], s['profile']
    iface, config = wg_config(role, p, private, psk, peer)
    service = 'wg-live-egress' if role == 'exit' else 'wg-live-policy'
    executable = pathlib.Path('/usr/local/sbin') / service
    write(executable, helper(role, p), 0o700)
    run(['sh', '-n', str(executable)])
    write(WGDIR / (iface + '.conf'), config)
    write(f'/etc/systemd/system/{service}.service', f'''[Unit]
Description=WireGuard live tutorial policy
Wants=network-online.target
After=network-online.target docker.service
Before=wg-quick@{iface}.service
[Service]
Type=oneshot
ExecStart={executable}
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
''', 0o644)
    write(f'/etc/systemd/system/wg-quick@{iface}.service.d/wg-live.conf', f'[Unit]\nRequires={service}.service\nAfter={service}.service\n', 0o644)
    if role == 'exit': write('/etc/sysctl.d/91-wg-live.conf', 'net.ipv4.ip_forward = 1\n', 0o644)
    run(['systemctl', 'daemon-reload'])
    run(['systemctl', 'enable', '--now', service, f'wg-quick@{iface}'])
    stripped = run(['wg-quick', 'strip', iface], capture=True).stdout
    run(['wg', 'syncconf', iface, '/dev/stdin'], input=stripped)
    # Re-apply owned rules after an interrupted install or an external firewall reload.
    run([str(executable)])
    s['stage'] = 'network-ready'
    write(STATE, json.dumps(s, indent=2))

def exchange():
    s = read_state()
    if s['role'] != 'exit' or s['stage'] != 'network-ready': raise RuntimeError('请先在英国 VPS 完成第一步')
    result = {'version': VERSION, 'profile': s['profile'], 'public_key': (WGDIR / 'wg-live-public.key').read_text().strip(),
              'preshared_key': (WGDIR / 'wg-live-preshared.key').read_text().strip()}
    # This mode is captured by the relay over authenticated SSH, never displayed by the webpage.
    print(json.dumps(result))

def attach_peer(a):
    s = read_state()
    if s['role'] != 'exit' or s['profile'] != profile(a): raise RuntimeError('两端填写的参数不一致，请核对网页参数')
    if s.get('relay_public') and s['relay_public'] != a.relay_public: raise RuntimeError('已有其他中转公钥；请核对原中转，保留现有配置')
    private = (WGDIR / 'wg-live-private.key').read_text().strip()
    psk = (WGDIR / 'wg-live-preshared.key').read_text().strip()
    iface, config = wg_config('exit', s['profile'], private, psk, a.relay_public)
    write(WGDIR / (iface + '.conf'), config)
    stripped = run(['wg-quick', 'strip', iface], capture=True).stdout
    run(['wg', 'syncconf', iface, '/dev/stdin'], input=stripped)
    s['relay_public'] = a.relay_public
    write(STATE, json.dumps(s, indent=2))
    print('英国端已接入中转公钥。')

def ssh_session(p, control):
    common = ['ssh', '-p', str(p['exit_ssh_port']), '-o', 'ConnectTimeout=20',
              '-o', 'ControlPath=' + str(control), '-T']
    host = 'root@' + p['exit_ip']
    # Authenticate with inherited terminal streams before capturing secret output.
    master = common + ['-o', 'StrictHostKeyChecking=ask', '-o', 'BatchMode=no',
                       '-o', 'ControlMaster=yes', '-o', 'ControlPersist=60', '-N', '-f', host]
    client = common + ['-o', 'StrictHostKeyChecking=yes', '-o', 'BatchMode=yes',
                       '-o', 'ControlMaster=no', host]
    return master, client

def ssh_exchange(ssh, remote):
    # Only stdout contains the exchange JSON. Keep SSH errors visible, never print JSON on failure.
    result = subprocess.run(ssh + [remote], text=True, stdout=subprocess.PIPE, check=True)
    return json.loads(result.stdout)

def repair_addresses(a):
    os.umask(0o077)
    s = read_state()
    if s.get('version') != VERSION or s.get('role') not in ['exit', 'relay'] or s.get('stage') != 'network-ready':
        raise RuntimeError('仅能修正本教程已写入网络配置的服务器；请先核对部署状态')
    old, new = s['profile'], profile(a)
    for name in ['relay_ssh_port', 'exit_ssh_port', 'wg_port', 'node_port']:
        if old[name] != new[name]: raise RuntimeError('地址修正只能更改 IP；端口需保持已部署的值')
    if old == new:
        print('本机记录的 IP 已与页面一致，无需修正。')
        return
    iface = 'wg-relay' if s['role'] == 'exit' else 'wg-uk'
    files = [STATE, WGDIR / (iface + '.conf'), WGDIR / 'wg-live-private.key', WGDIR / 'wg-live-preshared.key']
    if not all(path.is_file() for path in files): raise RuntimeError('本教程配置或密钥不完整，停止地址修正')
    peers = run(['wg', 'show', iface, 'peers'], capture=True).stdout.split()
    if len(peers) != 1: raise RuntimeError('现有隧道须有且仅有一个对端，停止地址修正')
    peer = validate_key(peers[0])
    if s['role'] == 'exit' and peer != s.get('relay_public'):
        raise RuntimeError('运行中的中转公钥与部署记录不一致，停止地址修正')
    private = validate_key(files[2].read_text().strip())
    psk = validate_key(files[3].read_text().strip())
    backup = BACKUPS / ('address-fix-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
    backup.mkdir(parents=True, mode=0o700)
    service = 'wg-live-egress' if s['role'] == 'exit' else 'wg-live-policy'
    for path in files + [pathlib.Path('/usr/local/sbin') / service]:
        if path.is_file():
            saved = backup / path.name
            shutil.copyfile(path, saved)
            saved.chmod(0o600)
    print('修正前记录已备份：' + str(backup), flush=True)
    s.setdefault('address_changes', []).append({'old': old, 'new': new, 'backup': str(backup)})
    s['profile'] = new
    install_network(s, private, psk, peer)
    print(('英国出口' if s['role'] == 'exit' else '中转') + '的 IP 已修正，原 WireGuard 密钥已保留。请在另一台也执行地址修正，再检查隧道。')

def deploy(a):
    p = profile(a)
    s = prepare(a.mode, p)
    private, public = keys()
    if a.mode == 'exit':
        pskfile = WGDIR / 'wg-live-preshared.key'
        if not pskfile.exists(): write(pskfile, run(['wg', 'genpsk'], capture=True).stdout.strip() + '\n')
        install_network(s, private, pskfile.read_text().strip(), s.get('relay_public'))
        print('英国出口已准备好。现在到中转 VPS 执行网页的第二条命令。')
        return
    with tempfile.TemporaryDirectory(prefix='wg-live-', dir='/run') as tmp:
        master, ssh = ssh_session(p, pathlib.Path(tmp) / 'ssh')
        try:
            print('正在连接英国 VPS。核对主机指纹后输入 yes，再输入英国 root 密码；输入密码时没有字符显示。密码不保存到网页或配置文件。', flush=True)
            try: run(master)
            except subprocess.CalledProcessError:
                raise RuntimeError('英国 SSH 确认或认证未完成。请在 FinalShell 的交互终端中单独运行 ssh -p '
                                   + str(p['exit_ssh_port']) + ' root@' + p['exit_ip']
                                   + '，核对指纹并登录成功后输入 exit 返回中转，再重试。若提示立即退出，单独执行 tty；如显示 not a tty，请改用交互终端。不要关闭主机校验。')
            run(ssh[:-1] + ['-O', 'check', ssh[-1]], capture=True)
            print('SSH 认证已完成，正在安全交换 WireGuard 密钥…', flush=True)
            remote = shlex.join(['python3', '/root/wg-live/deploy.py', 'exchange'])
            payload = ssh_exchange(ssh, remote)
            if payload.get('version') != VERSION or payload['profile'] != p: raise RuntimeError('英国端版本或参数与当前网页不一致')
            peer = validate_key(payload['public_key']); psk = validate_key(payload['preshared_key'])
            write(WGDIR / 'wg-live-preshared.key', psk + '\n')
            peer_args = ['python3', '/root/wg-live/deploy.py', 'peer', '--relay-public', public]
            for name, value in p.items(): peer_args += ['--' + name.replace('_', '-'), str(value)]
            run(ssh + [shlex.join(peer_args)])
            install_network(s, private, psk, peer)
        finally:
            # Only close the temporary multiplexed connection, never alter SSH keys or host verification.
            control = ssh[:-1] + ['-O', 'exit', ssh[-1]]
            run(control, capture=True, check=False)
    run(['ping', '-c', '3', '-W', '3', '10.77.0.1'])
    result = run(['curl', '-4', '--interface', '10.77.0.2', '-fsS', '--max-time', '20', 'https://api.ipify.org'], capture=True).stdout.strip()
    print('中转隧道已连接，实测公网出口：' + result)
    if result != p['exit_ip']: print('实测出口与填写的英国 IP 不同，请核对供应商出口地址后验收。')
    print('接下来按网页创建 3X-UI 入站，再执行“接入英国出口”的命令。')

def status(pause=False):
    s = read_state()
    iface = 'wg-relay' if s['role'] == 'exit' else 'wg-uk'
    if pause:
        run(['systemctl', 'stop', 'wg-quick@' + iface])
        print('隧道已暂停，代理可能停止；使用 systemctl start wg-quick@' + iface + ' 恢复。')
    else:
        run(['wg', 'show', iface])
        if s['role'] == 'relay': run(['ip', 'route', 'show', 'table', str(MARK)])

def main(argv=None):
    a = parse(argv)
    if a.dry_run:
        print(json.dumps({'mode': a.mode, 'version': VERSION, 'profile': profile(a)}, ensure_ascii=False))
        return
    if os.name != 'posix' or os.geteuid() != 0: raise RuntimeError('请在 VPS 的 root SSH 会话中执行')
    if a.mode in ['exit', 'relay']: deploy(a)
    elif a.mode == 'peer': attach_peer(a)
    elif a.mode == 'exchange': exchange()
    elif a.mode == 'repair-addresses': repair_addresses(a)
    else: status(a.mode == 'pause')

if __name__ == '__main__':
    try: main()
    except (RuntimeError, subprocess.CalledProcessError, json.JSONDecodeError, OSError) as e:
        # Do not include captured exchange payloads, which contain the preshared key.
        print('部署停止：' + (str(e) if not isinstance(e, subprocess.CalledProcessError) else '某个命令失败，请查看上方终端提示。'), file=sys.stderr)
        print('已有配置不会自动覆盖。备份位于 /root/wg-live-backups/；可按页面排查后重试。', file=sys.stderr)
        sys.exit(1)
