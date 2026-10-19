#!/usr/bin/env python3
"""Attach only the selected 3X-UI inbound port; retain the original template."""
import argparse, copy, datetime, json, os, pathlib, re, shutil, sqlite3, subprocess, sys, time, urllib.parse

DB = pathlib.Path('/etc/x-ui/x-ui.db')
LIVE = pathlib.Path('/usr/local/x-ui/bin/config.json')
STATE = pathlib.Path('/etc/wireguard/wg-live-state.json')

def build_template(old, tags):
    t = copy.deepcopy(old)
    if t.get('routing', {}).get('script'): raise RuntimeError('检测到自定义路由脚本，请先检查现有分流')
    outbound = {'tag': 'uk-wireguard', 'protocol': 'freedom', 'sendThrough': '10.77.0.2',
                'settings': {'domainStrategy': 'ForceIPv4'},
                'streamSettings': {'sockopt': {'mark': 51830, 'interface': 'wg-uk', 'domainStrategy': 'ForceIPv4',
                                               'tcpKeepAliveIdle': 30, 'tcpKeepAliveInterval': 15}}}
    t['outbounds'] = [o for o in t.get('outbounds', []) if o.get('tag') != 'uk-wireguard'] + [outbound]
    if not any(o.get('tag') == 'blocked' for o in t['outbounds']): t['outbounds'].append({'tag': 'blocked', 'protocol': 'blackhole', 'settings': {}})
    rules = t.get('routing', {}).get('rules', [])
    api = [r for r in rules if 'api' in r.get('inboundTag', [])]
    others = []
    for rule in rules:
        if rule in api: continue
        r = copy.deepcopy(rule)
        if 'inboundTag' in r:
            remaining = [tag for tag in r['inboundTag'] if tag not in tags + ['uk-dns']]
            if not remaining: continue
            r['inboundTag'] = remaining
        others.append(r)
    t.setdefault('routing', {})['rules'] = api + [
        {'type': 'field', 'ip': ['geoip:private'], 'outboundTag': 'blocked'},
        {'type': 'field', 'protocol': ['bittorrent'], 'outboundTag': 'blocked'},
        {'type': 'field', 'inboundTag': ['uk-dns'], 'outboundTag': 'uk-wireguard'},
        {'type': 'field', 'inboundTag': tags, 'outboundTag': 'uk-wireguard'},
    ] + others
    t['routing']['domainStrategy'] = 'AsIs'
    t['dns'] = {'servers': ['https://1.1.1.1/dns-query', 'https://8.8.8.8/dns-query'], 'queryStrategy': 'UseIPv4', 'tag': 'uk-dns'}
    return t

def write(path, content, mode=0o600):
    path = pathlib.Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8'); path.chmod(mode)

def run(args, **kwargs): return subprocess.run(args, check=True, **kwargs)

def binary():
    choices = list(pathlib.Path('/usr/local/x-ui/bin').glob('xray-linux-*'))
    choices = [p for p in choices if p.is_file() and os.access(p, os.X_OK)]
    if len(choices) != 1: raise RuntimeError('未能识别标准 3X-UI 的 Xray 可执行文件')
    return choices[0]

def node_link(row, runtime, relay_ip, exe):
    stream = json.loads(row['stream_settings'])
    rs = stream.get('realitySettings', {})
    settings = rs.get('settings', {})
    public = settings.get('publicKey', '')
    if not public and rs.get('privateKey'):
        try: result = run([str(exe), 'x25519', '-i', rs['privateKey']], capture_output=True, text=True).stdout
        except subprocess.CalledProcessError: return None
        found = re.search(r'(?im)^(?:public\s*key|password)\s*:\s*(\S+)', result)
        if found: public = found.group(1)
    inbound = next((i for i in runtime.get('inbounds', []) if i.get('tag') == row['tag']), None)
    clients = inbound.get('settings', {}).get('clients', []) if inbound else []
    if row['protocol'] != 'vless' or stream.get('security') != 'reality' or not public or not clients:
        return None
    client = clients[0]; names = rs.get('serverNames', []); shorts = rs.get('shortIds', [])
    if not names or not shorts: return None
    params = {'encryption': 'none', 'flow': client.get('flow', ''), 'security': 'reality',
              'sni': names[0], 'fp': 'chrome', 'pbk': public, 'sid': shorts[0], 'type': 'tcp', 'headerType': 'none'}
    return 'vless://' + client['id'] + '@' + relay_ip + ':' + str(row['port']) + '?' + urllib.parse.urlencode(params) + '#UK-WireGuard-Live'

def apply(port):
    if not STATE.exists() or not pathlib.Path('/sys/class/net/wg-uk').exists(): raise RuntimeError('请先完成网页的中转隧道部署步骤')
    state = json.loads(STATE.read_text())
    if state.get('role') != 'relay': raise RuntimeError('此命令只能在中转 VPS 运行')
    if not DB.exists() or not LIVE.exists(): raise RuntimeError('请先安装 3X-UI 并在面板创建入站节点')
    c = sqlite3.connect(str(DB), timeout=20); c.row_factory = sqlite3.Row
    columns = {r[1] for r in c.execute('pragma table_info(inbounds)')}
    sql = 'select * from inbounds where enable=1 and port=?'
    if 'node_id' in columns: sql += ' and (node_id is null or node_id=0)'
    rows = list(c.execute(sql, (port,)))
    if len(rows) != 1: raise RuntimeError('没有找到唯一的已启用本机入站：请在面板检查节点端口 ' + str(port))
    row = dict(rows[0]); tags = [row['tag']]
    value = c.execute("select value from settings where key='xrayTemplateConfig'").fetchone()
    if not value: raise RuntimeError('面板不是标准 SQLite 模板结构，请检查版本')
    old = json.loads(value[0]); updated = build_template(old, tags)
    backup = pathlib.Path('/root/wg-live-panel-backups') / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True, mode=0o700)
    with sqlite3.connect(str(backup / 'x-ui.db')) as dest: c.backup(dest)
    write(backup / 'template-before.json', value[0]); shutil.copy2(LIVE, backup / 'runtime-before.json')
    candidate = json.loads(LIVE.read_text())
    for name in ['outbounds', 'routing', 'dns']: candidate[name] = updated[name]
    proposed = backup / 'proposed.json'; write(proposed, json.dumps(candidate))
    exe = binary()
    run([str(exe), 'run', '-test', '-config', str(proposed)], cwd='/usr/local/x-ui')
    run(['systemctl', 'stop', 'x-ui'])
    try:
        with c: c.execute("update settings set value=? where key='xrayTemplateConfig'", (json.dumps(updated),))
        write('/etc/systemd/system/x-ui.service.d/wg-live.conf', '[Unit]\nWants=wg-quick@wg-uk.service\nAfter=wg-live-policy.service wg-quick@wg-uk.service\n', 0o644)
        run(['systemctl', 'daemon-reload']); run(['systemctl', 'start', 'x-ui'])
    except Exception:
        with c: c.execute("update settings set value=? where key='xrayTemplateConfig'", (value[0],))
        subprocess.run(['systemctl', 'start', 'x-ui']); raise
    if not state.get('panel_backup'): state['panel_backup'] = str(backup)
    state['node_tag'] = row['tag']; state['node_port'] = port
    write(STATE, json.dumps(state, indent=2))
    time.sleep(3)
    runtime = json.loads(LIVE.read_text())
    if not any(i.get('tag') == row['tag'] for i in runtime.get('inbounds', [])): raise RuntimeError('面板尚未生成入站，请检查 x-ui 日志')
    link = node_link(row, runtime, state['profile']['relay_ip'], exe)
    print('节点已接入英国出口：' + row['tag'] + '，端口 ' + str(port))
    if link:
        write('/root/wg-live/node-link.txt', link + '\n')
        print('\n复制以下链接导入客户端（链接含节点认证信息，请勿公开）：\n' + link)
    else: print('请在 3X-UI 面板复制此节点的分享链接。')
    print('\n原始模板备份：' + state['panel_backup'])

def restore():
    state = json.loads(STATE.read_text())
    backup = pathlib.Path(state.get('panel_backup', ''))
    source = backup / 'template-before.json'
    if not source.exists(): raise RuntimeError('没有可恢复的原始面板模板')
    run(['systemctl', 'stop', 'x-ui'])
    c = sqlite3.connect(str(DB), timeout=20)
    try:
        with c: c.execute("update settings set value=? where key='xrayTemplateConfig'", (source.read_text(),))
    finally:
        drop = pathlib.Path('/etc/systemd/system/x-ui.service.d/wg-live.conf')
        if drop.exists(): drop.unlink()
        run(['systemctl', 'daemon-reload']); run(['systemctl', 'start', 'x-ui'])
    print('原始出站模板已恢复。节点与流量统计保留；可按网页命令暂停隧道。')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--node-port', type=int, default=443); p.add_argument('--restore', action='store_true')
    a = p.parse_args()
    if not 1 <= a.node_port <= 65535: p.error('节点端口范围为 1–65535')
    if os.name != 'posix' or os.geteuid() != 0: raise RuntimeError('请在中转 VPS 的 root SSH 会话中执行')
    os.umask(0o077)
    restore() if a.restore else apply(a.node_port)

if __name__ == '__main__':
    try: main()
    except (RuntimeError, subprocess.CalledProcessError, OSError) as error:
        print('面板接入停止：' + str(error), file=sys.stderr); sys.exit(1)
