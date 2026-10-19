---
date: 2026-10-14
categories:
  - 工具视频教程
slug: zhibouk
tags:
  - 工具
  
---

# 跨境直播网络搭建：3X-UI 中转 + WireGuard 英国出口

<div class="hide-in-post" markdown="1">

![封面图](images/fm.png){ .hide-in-post width="300" align="left" }

<p class="hide-in-post"><strong>本期看点：</strong>填写自己的两台 VPS 信息，自动生成部署命令；按顺序搭建中转、英国出口和 OBS 直播网络。</p>

</div>

<!-- more -->



先填写下面的参数表，再按顺序操作。下方每个代码框都会使用你填写的 IP 和端口，直接点击“复制命令”，粘贴到标注的服务器窗口中即可。

<form class="wg-setup" id="wg-live-config" data-manifest="/assets/wireguard/20261014-v1/manifest.json" autocomplete="off">
  <p class="wg-setup__eyebrow">开始之前 · 填写一次，全篇同步</p>
  <h3>填写你的两台 VPS 信息</h3>
  <p class="wg-setup__intro">输入两台服务器的公网 IPv4，下方登录、部署、检查命令会立即更新。每一步都有单独的复制按钮。</p>
  <table aria-label="服务器参数填写表"><thead><tr><th>必要信息</th><th>填写你的实际信息</th></tr></thead><tbody>
    <tr><td><label for="wg-relay-ip">中转 VPS 公网 IP</label></td><td><input id="wg-relay-ip" name="relay_ip" type="text" inputmode="decimal" placeholder="例如 198.51.100.10" spellcheck="false" aria-required="true"></td></tr>
    <tr><td><label for="wg-exit-ip">英国出口 VPS 公网 IP</label></td><td><input id="wg-exit-ip" name="exit_ip" type="text" inputmode="decimal" placeholder="例如 203.0.113.20" spellcheck="false" aria-required="true"></td></tr>
  </tbody></table>
  <details><summary>高级设置：SSH 和部署端口（通常保持默认）</summary>
    <table aria-label="高级端口填写表"><tbody>
      <tr><td><label for="wg-relay-ssh">中转 SSH 端口</label></td><td><input id="wg-relay-ssh" name="relay_ssh_port" type="number" min="1" max="65535" value="22"></td></tr>
      <tr><td><label for="wg-exit-ssh">英国 SSH 端口</label></td><td><input id="wg-exit-ssh" name="exit_ssh_port" type="number" min="1" max="65535" value="22"></td></tr>
      <tr><td><label for="wg-node-port">节点 TCP 端口</label></td><td><input id="wg-node-port" name="node_port" type="number" min="1" max="65535" value="443"></td></tr>
      <tr><td><label for="wg-udp-port">WireGuard UDP 端口</label></td><td><input id="wg-udp-port" name="wg_port" type="number" min="1" max="65535" value="51830"></td></tr>
    </tbody></table>
  </details>
  <div class="wg-setup__footer"><p class="wg-setup__status" data-wg-status role="status" aria-live="polite">请先填写两台 VPS 的 IP。</p><button type="button" class="wg-setup__reset" data-wg-reset>清空并恢复默认</button></div>
  <p class="wg-setup__privacy">参数只在本页处理，并在当前浏览器标签页暂存。这里不填写 SSH 密码、私钥或推流密钥；SSH 认证在 VPS 终端中完成。</p>
  <p class="wg-setup__local-note" data-wg-local-note hidden>当前为本地预览。下面的部署命令已经包含完整脚本，可以直接复制到 VPS 执行，无需等待网站发布。</p>
</form>
<noscript><p>本页的参数联动需要浏览器启用 JavaScript。启用后填写顶部参数表，再复制部署命令。</p></noscript>

## 一、确认网络结构与准备条件

```text
电脑 / OBS（全局模式 + TUN）
        ↓ VLESS / REALITY
中转 VPS（3X-UI 节点）
        ↓ WireGuard
英国出口 VPS（转发 + 出口转换）
        ↓
目标网站 / 直播平台
```

本页使用**一台中转 + 一台英国出口**。客户端连接中转，网站和平台看到英国公网出口。英国出口的运营商或住宅属性由供应商提供，WireGuard 负责连接两台服务器。

### 准备条件

- 两台独立 Ubuntu / Debian VPS，支持 WireGuard 和 systemd，能使用 root SSH 登录。
- 两端公网 IPv4 固定，允许 UDP 通信；隧道使用未被占用的 `10.77.0.0/30`。
- 中转使用标准路径安装的 3X-UI，存储方式为默认 SQLite。新环境可以在第四步安装。
- 本地客户端支持 VLESS / REALITY 与 TUN；准备 OBS 和自己的直播平台信息。
- 本页适合独立直播环境。已有同名 WireGuard 接口或其他部署时，脚本会停止并提示，不会直接覆盖。

!!! tip "复制前先看窗口名称"
    “英国 VPS”的命令只在英国终端执行，“中转 VPS”的命令只在中转终端执行。登录命令可在本地 PowerShell 使用，也可以直接用 FinalShell 创建对应连接。

### 云平台安全组需要放行

| 服务器 | 端口 | 允许来源 | 用途 |
| --- | --- | --- | --- |
| 中转 | <span class="wg-param" data-wg-value="relay_ssh_port">22</span> / TCP | 自己的管理地址 | SSH |
| 中转 | <span class="wg-param" data-wg-value="node_port">443</span> / TCP | 使用节点的客户端 | VLESS / REALITY |
| 中转 | <span class="wg-param" data-wg-value="wg_port">51830</span> / UDP | <span class="wg-param" data-wg-value="exit_ip">（填写后显示）</span> | WireGuard |
| 中转 | 面板实际端口 / TCP | 自己的管理地址 | 管理 3X-UI |
| 英国 | <span class="wg-param" data-wg-value="exit_ssh_port">22</span> / TCP | 自己的管理地址、中转 <span class="wg-param" data-wg-value="relay_ip">（填写后显示）</span> | SSH / 自动交换密钥 |
| 英国 | <span class="wg-param" data-wg-value="wg_port">51830</span> / UDP | <span class="wg-param" data-wg-value="relay_ip">（填写后显示）</span> | WireGuard |

脚本会添加 VPS 内的 WireGuard 转发和防火墙规则。云安全组需要在供应商控制台放行；已有 UFW、firewalld 或独立 nftables 策略时，也需允许这些端口及隧道转发。已有 wg-easy 可以保留，确认它与填写的 UDP 端口不同。

## 二、英国 VPS：先准备出口

### 2.1 登录英国服务器

<div class="wg-command" data-wg-command="login_exit" data-wg-target="本地电脑 · PowerShell">
  <div class="wg-command__bar"><span>本地电脑 · PowerShell</span><button type="button" disabled aria-label="复制本地电脑 · PowerShell的login_exit命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

FinalShell 连接地址应为 <span class="wg-param" data-wg-value="exit_ip">（填写后显示）</span>，SSH 端口为 <span class="wg-param" data-wg-value="exit_ssh_port">22</span>。进入 root 会话；如果登录的是普通用户，先执行 `sudo -i`。

### 2.2 整段复制部署命令

<div class="wg-command" data-wg-command="exit" data-wg-target="英国 VPS · root">
  <div class="wg-command__bar"><span>英国 VPS · root</span><button type="button" disabled aria-label="复制英国 VPS · root的exit命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

命令已经包含本教程的完整脚本，复制按钮会一次复制整个代码框，包括滚动区域内的内容。命令将脚本写入服务器并检查文件校验值，再安装 WireGuard、生成密钥、配置 `wg-relay`、出口转换和开机启动。它会自动识别出网网卡，无需手动填写 `eth0` 或 `ens18`。VPS 无需从本博客下载文件。

看到“**英国出口已准备好**”后继续第三步。此时还没有中转握手是正常现象。密钥由服务器生成，不需要复制附录或显示私钥。

## 三、中转 VPS：连接英国出口

### 3.1 登录中转服务器

<div class="wg-command" data-wg-command="login_relay" data-wg-target="本地电脑 · PowerShell">
  <div class="wg-command__bar"><span>本地电脑 · PowerShell</span><button type="button" disabled aria-label="复制本地电脑 · PowerShell的login_relay命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

FinalShell 连接地址应为 <span class="wg-param" data-wg-value="relay_ip">（填写后显示）</span>，SSH 端口为 <span class="wg-param" data-wg-value="relay_ssh_port">22</span>，使用 root 会话。

### 3.2 整段复制部署命令

首次连接前，在**英国 VPS 窗口**查看主机指纹，记住输出中的 `SHA256:...`：

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub
```

然后回到**中转 VPS 窗口**，复制下面的完整命令：

<div class="wg-command" data-wg-command="relay" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的relay命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

中转会通过 SSH 连接英国 <span class="wg-param" data-wg-value="exit_ip">（填写后显示）</span>，先在终端完成主机确认和密码认证，再交换 WireGuard 密钥。出现 `Are you sure you want to continue connecting` 时，核对 ECDSA 指纹与英国窗口的结果一致，输入 `yes` 后按回车；接着输入英国 root 密码并回车，输入密码时不显示字符是正常现象。使用 SSH 密钥的用户按对应认证提示操作。主机指纹变化时应先确认服务器情况。

!!! tip "如果主机确认仍失败"
    在中转的 FinalShell 交互终端**单独输入**顶部参数生成的 SSH 登录命令，完成指纹核对和登录。登录后输入 `exit` 返回中转，再重新复制本节的部署命令。不要将 `yes` 和密码与部署命令一起批量粘贴。如果提示主机密钥发生变化，先核对英国服务器，不关闭主机校验。

    如果确认提示一出现就退出，在中转单独执行 `tty`。应显示 `/dev/pts/数字`；显示 `not a tty` 时，重新打开可交互的终端会话后再执行。

脚本通过 SSH 交换公钥和预共享密钥，然后创建 `wg-uk`、独立路由和防回退规则。密码不写进网页或命令；中转的普通默认路由保持原有设置，便于继续 SSH 管理。

看到“**中转隧道已连接，实测公网出口**”后，核对显示的 IP 是否为英国出口 <span class="wg-param" data-wg-value="exit_ip">（填写后显示）</span>。

### 3.3 手动检查一次隧道

<div class="wg-command" data-wg-command="check" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的check命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

应看到 ping 回复、`latest handshake` 和英国出口 IP。这里的 `--interface 10.77.0.2` 指定隧道源地址；省略它会使用中转自身的网络。

!!! warning "隧道通过后才继续"
    如果出现 `No such device`、`Cannot assign requested address`，或没有英国出口 IP，先停在第三步，查看部署报错。不要继续接入面板或反复测试节点。

## 四、中转 VPS：建立 3X-UI 节点并接入英国出口

### 4.1 未安装面板时执行

已有 3X-UI 可以跳过安装；新环境在中转执行：

<div class="wg-command" data-wg-command="install_panel" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的install_panel命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

按安装提示设置面板，使用默认 SQLite。面板管理端口应与节点端口 <span class="wg-param" data-wg-value="node_port">443</span> 不同，保存登录信息。执行 `x-ui` 可以进入管理菜单。

### 4.2 在面板创建并启用入站

| 参数 | 填写内容 |
| --- | --- |
| 备注 | 英国出口 · WireGuard 中转 |
| 协议 | VLESS |
| 监听地址 | 0.0.0.0 或默认 |
| 节点端口 | <span class="wg-param" data-wg-value="node_port">443</span> |
| 传输 | TCP / RAW |
| 安全 | REALITY |
| Target / 目标 | www.samsung.com:443 |
| Server Names / SNI | www.samsung.com |
| REALITY 密钥、Short ID、客户 UUID | 使用面板生成 |
| 客户 Flow | xtls-rprx-vision |
| 入站与客户启用状态 | 开启 |

其余先保持默认。示例 REALITY 目标在原部署中可用，使用前需确认中转能够访问；更换目标时同步修改 SNI。端口被其他服务占用时，先处理冲突或选择新端口，并同步修改顶部参数和面板。

### 4.3 把这个节点接入英国出口

保存入站后，在中转执行：

<div class="wg-command" data-wg-command="panel" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的panel命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

脚本根据端口 <span class="wg-param" data-wg-value="node_port">443</span> 查找入站，备份面板模板并进行 Xray 配置检查，再将该入站接入 `uk-wireguard` 出站。它保留面板 API 路由与其他入站的路由，设置经隧道发送的 IPv4 DoH 解析，因此本页仍以独立直播面板为前提。

完成后，终端会输出节点分享链接，或提示到面板复制链接。链接含客户端认证信息，请保管好。原始模板备份位置也会打印出来。

### 4.4 检查节点与路由

<div class="wg-command" data-wg-command="listeners" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的listeners命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

应看到服务为 `active`、节点端口 <span class="wg-param" data-wg-value="node_port">443</span> 由 Xray 监听，以及以下两条路由：

```text
default dev wg-uk ... metric 10
unreachable default metric 32767
```

正常时使用隧道；隧道停止后，不可达路由阻止代理回退到中转公网出口。配置写入 3X-UI 模板，重启后由面板重新生成；无需手动编辑 `bin/config.json`。

## 五、本地电脑：连接节点和直播验收

### 5.1 导入并选择节点

1. 导入终端输出的 VLESS 链接，或从 3X-UI 复制链接 / 扫描二维码。
2. 确认节点服务器地址为中转 <span class="wg-param" data-wg-value="relay_ip">（填写后显示）</span>，端口为 <span class="wg-param" data-wg-value="node_port">443</span>。
3. 将该节点**设为活动服务器**，确认客户端底部显示英国节点名称；仅选中列表中的行不会切换当前出口。然后启用全局模式与 **TUN / 虚拟网卡**，需要服务模式或管理员权限时按客户端提示操作。
4. 先关闭客户端 Mux，其他连接参数保持默认。

本地无需安装 WireGuard。全局模式选择出口节点，TUN 将 OBS 等应用的连接送入客户端；仅使用系统代理可能无法覆盖推流。

### 5.2 核对实际出口

浏览器访问 [公网 IP 检测](https://api.ipify.org) 与 [Cloudflare 连接信息](https://www.cloudflare.com/cdn-cgi/trace)。应显示英国出口 <span class="wg-param" data-wg-value="exit_ip">（填写后显示）</span>，再核对 `loc=GB`。也可在 TUN 开启后于本机执行：

<div class="wg-command" data-wg-command="client_check" data-wg-target="本地电脑 · TUN 已开启">
  <div class="wg-command__bar"><span>本地电脑 · TUN 已开启</span><button type="button" disabled aria-label="复制本地电脑 · TUN 已开启的client_check命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

随后测试你的目标网站：登录、页面加载和视频播放等功能需要分别验收。

### 5.3 OBS 连续试推

- 填写自己的平台和推流信息，客户端保持 TUN 开启。
- OBS 的“绑定到 IP”保持默认，本方案使用 IPv4。
- 根据本地实际上传速度设置码率，预留音频、协议与波动余量。
- 连续试推 10–15 分钟，观察网络丢帧、断线、实际码率和平台接收画面。

原执行电脑短测上行约 9 Mbps，可以先用 3500–4500 kbps 视频码率试推；这是该次测量的保守起点，不是所有用户的固定码率。两台 VPS 之间的测速不能代替本地到平台的完整推流测试。

### 5.4 验证断线防回退

在未正式直播的时间，于中转暂停隧道：

<div class="wg-command" data-wg-command="pause" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的pause命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

本地重新打开 IP 检测页面，代理应无法访问，不应变为中转出口。测试后立即在中转恢复：

<div class="wg-command" data-wg-command="resume" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的resume命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

重新核对英国出口，再安排实际 VPS 重启验收。原部署验证了服务重启与开机启用状态；本页的新自动交换脚本需要在自己的新环境完成实际部署和验收。

## 六、日常检查与恢复

### 中转服务和日志

<div class="wg-command" data-wg-command="status_relay" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的status_relay命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

### 英国出口状态

<div class="wg-command" data-wg-command="status_exit" data-wg-target="英国 VPS · root">
  <div class="wg-command__bar"><span>英国 VPS · root</span><button type="button" disabled aria-label="复制英国 VPS · root的status_exit命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

### 恢复原来的面板出站

需要撤销第四步的出口修改时，在中转执行：

<div class="wg-command" data-wg-command="restore" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的restore命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

这一步恢复首次接入前的模板，保留节点和流量统计。确认旧出站可用后，可用上面的暂停命令停止隧道。它不是删除整套配置；密钥、备份和防回退配置继续保留。

## 七、常见问题与可选测速

| 现象 | 优先检查 |
| --- | --- |
| 旧命令下载返回 404 | 刷新到本页新版，重新复制第二、第三步的完整命令；新版不依赖 VPS 下载本博客脚本 |
| 页面无法生成命令 | 顶部状态提示是否显示脚本加载失败，网站是否包含本页脚本与版本文件 |
| `wg-uk` 不存在 / 不能绑定 `10.77.0.2` | 第二、第三步是否真正完成；先解决部署报错，再继续第四步 |
| 客户端延迟显示 `-1` | 表示连通性测试失败；先确认隧道，再核对 TCP 端口放行、REALITY 参数和客户端日志 |
| 中转 SSH 交换失败 | 英国 SSH 端口 <span class="wg-param" data-wg-value="exit_ssh_port">22</span> 是否允许来自 <span class="wg-param" data-wg-value="relay_ip">（填写后显示）</span> 的连接，root 认证是否可用 |
| `Host key verification failed` | 英国主机指纹是否已经核对并确认；按第三步在交互终端单独登录再重试，主机密钥变化时先核对服务器 |
| 主机指纹不一致 | 核对英国 VPS 是否重装或更换，不直接跳过检查 |
| 无 WireGuard 握手 | 云安全组是否放行 <span class="wg-param" data-wg-value="wg_port">51830</span> / UDP，两端填写的参数是否相同 |
| 有握手但外网不通 | 英国转发是否开启，转发或 NAT 是否被其他防火墙策略阻断 |
| 找不到面板入站 | 已启用的本机入站端口是否为 <span class="wg-param" data-wg-value="node_port">443</span>，面板是否使用标准 SQLite 路径 |
| 节点无法启动 | <span class="wg-param" data-wg-value="node_port">443</span> / TCP 是否被其他服务占用，查看 x-ui 日志 |
| 浏览器正常、OBS 不通 | TUN 是否开启，OBS 绑定地址和推流地址是否正确 |
| 直播网络丢帧 | 本地到中转、英国到推流平台的实际链路与码率 |
| 已交换密钥但 ping 无回复 | 先看两端握手，再测试指定隧道源地址的公网出口；核对 IP 输入和 UDP 端口放行，单凭 ping 失败不能判断原因 |

填写参数的变化只会更新网页命令，不会自动修改已经部署的服务器。同参数重试会保留本教程密钥；已部署参数不同或有其他同名配置时，脚本会停止，先核对现有配置再调整。

<span id="wg-fix-addresses"></span>

### IP 填错后的修正（已完成密钥交换时使用）

如果命令已经显示“英国端已接入中转公钥”，但随后隧道不通，先核对顶部公网 IP 是否与 FinalShell 实际连接地址一致。尤其注意容易看错的数字。**先修改顶部参数表**，SSH、WireGuard 和节点端口保持原值。

先在英国执行地址修正：

<div class="wg-command" data-wg-command="repair_exit" data-wg-target="英国 VPS · root">
  <div class="wg-command__bar"><span>英国 VPS · root</span><button type="button" disabled aria-label="复制英国 VPS · root的repair_exit命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

再在中转执行地址修正：

<div class="wg-command" data-wg-command="repair_relay" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的repair_relay命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

修正命令先备份本教程配置，再更新对端地址、防火墙来源和部署记录，保留原有密钥。它只修正本教程已部署的 IP，不更改端口；没有本教程配置或对端公钥不一致时会停止。两端执行完，再运行 3.3 检查。不要删除密钥或防火墙全部规则来重试。

若还是不通，分别执行 `WG_HIDE_KEYS=always wg show wg-uk`（中转）和 `WG_HIDE_KEYS=always wg show wg-relay`（英国），核对近期握手。没有握手时检查两端 UDP 放行与对端地址；有握手时再检查英国的隧道输入、转发与出口转换。

### MTU 检查

<div class="wg-command" data-wg-command="mtu" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的mtu命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

这是 1380 字节 IPv4 无分片测试。若大包失败而小包正常，可将两端 WireGuard 配置中的 MTU 改为 1280，重启对应隧道后复测。

### 可选：测两台 VPS 之间的隧道

英国 VPS 开启只绑定隧道地址的测速服务：

<div class="wg-command" data-wg-command="iperf_exit" data-wg-target="英国 VPS · root">
  <div class="wg-command__bar"><span>英国 VPS · root</span><button type="button" disabled aria-label="复制英国 VPS · root的iperf_exit命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

中转另开终端执行：

<div class="wg-command" data-wg-command="iperf_relay" data-wg-target="中转 VPS · root">
  <div class="wg-command__bar"><span>中转 VPS · root</span><button type="button" disabled aria-label="复制中转 VPS · root的iperf_relay命令">复制命令</button></div>
  <pre><code>先在页面顶部填写两台 VPS 的 IP，命令会自动生成。</code></pre>
  <p class="wg-command__copy-status" data-wg-copy-status role="status" aria-live="polite"></p>
</div>

测速完成，在英国测速终端按 `Ctrl+C` 停止。若系统防火墙默认拒绝隧道到本机连接，需允许 `10.77.0.2 → 10.77.0.1:5202`，无需公开开放 5202。

原部署的 12 秒样本：中转到英国 TCP 约 281 Mbps，反向约 248 Mbps；12 Mbps UDP 未丢包。以上是一次参考测量，不代表所有用户线路的速度。

## 部署脚本与官方参考

本页使用版本 `20261014-v1`。网页先加载完整脚本，复制时将脚本与参数一起放进命令；VPS 写入文件后核对 SHA-256，校验通过才执行。若网页文件不完整，复制按钮会保持禁用。两端参数保存在服务器 `/etc/wireguard/wg-live-state.json`，网络备份在 `/root/wg-live-backups/`，面板备份在 `/root/wg-live-panel-backups/`。这是脚本的工作目录，无需手动编辑。

- [本页 WireGuard 部署脚本](/assets/wireguard/20261014-v1/deploy.py)
- [本页 3X-UI 接入脚本](/assets/wireguard/20261014-v1/connect-panel.py)
- [WireGuard 官方入门](https://www.wireguard.com/quickstart/)
- [3X-UI 官方安装](https://github.com/MHSanaei/3x-ui)
- [3X-UI 出站与路由](https://docs.sanaei.dev/docs/operations/outbounds-routing/)
- [Xray 出口绑定](https://xtls.github.io/en/config/transports/sockopt.html)
- [Xray DNS](https://xtls.github.io/en/config/dns.html)
- [Mihomo TUN](https://wiki.metacubex.one/en/config/inbound/tun/)
- [OBS 网络排查](https://obsproject.com/kb/stream-connection-troubleshooting)

教程交流：[TG 交流群](https://t.me/xiaovchat)

!!! Warning "**免责声明**"
    本文档及相关教程内容仅供计算机网络技术交流与学习测试使用。请务必严格遵守您所在国家或地区的法律法规，切勿用于任何非法用途。

--8<-- "includes/links.md"
