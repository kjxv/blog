---
title: VPS 与机场节点不可用应急方案
description: 临时共享订阅、Sing-box Hy 节点、申请更换 IP、可用 VPS 与 WireGuard 图文教程。
hide:
  - navigation
  - toc
---

<style>
  /* 与博客文章正文保持接近的阅读宽度 */
  .md-content__inner {
    max-width: 765px !important;
    margin: 0 auto !important;
  }

  .emergency-nav {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.6rem;
    margin: 1.2rem 0 1.6rem;
  }

  .emergency-nav a {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 3.2rem;
    padding: 0.65rem 0.75rem;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 0.55rem;
    background: var(--md-default-bg-color);
    color: var(--md-typeset-a-color);
    font-weight: 700;
    line-height: 1.45;
    text-align: center;
    transition: border-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
  }

  .emergency-nav a:hover {
    border-color: var(--md-accent-fg-color);
    transform: translateY(-1px);
    box-shadow: 0 0.25rem 0.8rem rgba(0, 0, 0, 0.08);
  }

  .md-typeset h2[id],
  .emergency-anchor {
    scroll-margin-top: 5rem;
  }

  @media screen and (max-width: 44.984375em) {
    .emergency-nav {
      grid-template-columns: 1fr;
    }
  }
</style>

---

# VPS 与机场节点不可用应急方案

近期很多厂商的 VPS 和机场节点可能出现无法使用的情况。下面先提供临时共享订阅，方便群友救急，再整理四种处理方案。读者可根据当前连接情况选择，后续有新的方案会持续更新。

**更新日期：2026 年 10 月 29 日。** 线路可用性随时间和运营商变化，请以自己当前网络的实际测试为准。

<nav class="emergency-nav" aria-label="应急方案快速导航">
  <a href="#plan-1-singbox">方案一<br>Sing-box 部署 Hy 节点</a>
  <a href="#plan-2-change-ip">方案二<br>联系客服申请更换 IP</a>
  <a href="#plan-3-vps">方案三<br>选择目前可用的 VPS</a>
  <a href="#plan-4-wireguard">方案四<br>WireGuard 隧道</a>
</nav>

## 临时共享订阅：先恢复一条可用连接 { #temporary-subscriptions }

考虑到部分群友暂时没有可用代理、无法直接获取 GitHub 上的订阅，现已通过自定义域名中转，方便直接导入 v2rayN 更新订阅。

### 合并订阅（推荐）

以下链接整合了下面五个订阅源，**导入一个链接即可获取节点**：

```text
https://sub.dlzys.shop/all
```

### 独立订阅（备用）

如果合并订阅无法正常导入，可以分别尝试以下链接：

**免费订阅链接 01**

```text
https://sub.dlzys.shop/sub1
```

**免费订阅链接 02**

```text
https://sub.dlzys.shop/sub2
```

**免费订阅链接 03**

```text
https://sub.dlzys.shop/sub3
```

**免费订阅链接 04**

```text
https://sub.dlzys.shop/sub4
```

**免费订阅链接 05**

```text
https://sub.dlzys.shop/sub5
```

### 使用说明

1. 复制推荐的合并订阅链接，添加到 v2rayN 的**订阅分组设置**中并保存。
2. 更新订阅时，选择 **「更新订阅（不通过代理）」**；不同版本的菜单名称可能略有区别，请选择不通过代理更新的选项。
3. 更新完成后测试节点延迟，优先选择有有效延迟数值的节点，再打开网页确认实际连接。超时或显示 `-1` 的节点先跳过。
4. 如果合并订阅无法正常导入，改用上面的独立订阅链接逐个尝试。

!!! warning "群内临时应急使用"
    - 免费节点稳定性无法保证，仅供临时应急，不保证速度或持续可用。
    - 节点来源于第三方，不建议用于敏感账户登录或支付操作。
    - **订阅链接仅供本群群友自用，请勿转载或公开传播。**

---

## 四个方案怎么选

!!! info "先判断自己属于哪种情况"
    能通过 SSH 登录 VPS，可尝试方案一；希望继续使用原服务器，可联系服务商了解方案二；急需恢复且原服务器不可达，可考虑方案三；能登录 3X-UI 且 UDP 仍可达，可尝试方案四。Sing-box 和 WireGuard 均不会把机房 IP 变成住宅 IP，也不能保证在所有网络下恢复连接。

<span id="plan-2-singbox" class="emergency-anchor"></span>

## 方案一：Sing-box 部署 Hy 节点 { #plan-1-singbox }

这是临时应急方案。前提是服务器仍然可以通过 SSH 连接：能够直连时正常登录即可；无法直连但本地代理可用时，可以让 SSH 客户端通过本地代理连接 VPS。

### 适用条件

- 仍能通过 SSH 直接连接 VPS，或可借助本地代理完成连接；
- 拥有服务器的 `root` 权限，或可以使用 `sudo` 切换到 `root`；
- VPS 本身可以访问互联网；
- 可以在服务商安全组和系统防火墙中放行脚本生成的端口。

### 第一步：必要时为 FinalShell 设置本地代理

如果 VPS 被当前网络阻断、FinalShell 无法直连，可以让 SSH 通过本地代理连接。**前提是本地已有一条能连接目标 VPS 的可用代理**；可先尝试上面的临时共享订阅。

1. 打开 v2rayN 或其他代理软件，更新订阅、测试延迟并选中一条可用节点，确认代理已经正常运行。
2. 在 FinalShell 的**连接管理器**中找到该 VPS，右键选择 **「编辑」**。
3. 在左侧进入 **「代理服务器」**，点击 **「添加」**，代理类型选择 **SOCKS5**。
4. 主机填写 `127.0.0.1`；截图中 v2rayN 的本地端口为 `10808`。请以软件当前显示的 SOCKS 或混合监听端口为准，其他软件也要按实际端口填写。
5. 保存代理设置，**勾选刚添加的代理**，点击 **「应用 → 确定」**，然后重新连接 VPS。

![在 FinalShell 中为 SSH 连接设置本地 SOCKS5 代理，公网 IP 已脱敏](images/07-finalshell-proxy-redacted.png)

> `127.0.0.1:10808` 指的是这台电脑上的代理服务，并非 VPS 的 SSH 端口或新部署的 Hy 节点端口。VPS 地址、SSH 端口和登录信息仍填写原来的值。如果代理也无法访问该 VPS，请改看方案二或方案三。

### 第二步：运行 Sing-box 一键部署脚本

连接 VPS 后，先切换到 `root` 用户：

```bash
sudo -i
```

然后运行下面的**固定视频教程版**部署命令，版本为 `v1.3.28-vedio`：

```bash
bash <(wget -qO- https://raw.githubusercontent.com/kjxv/sing-box/v1.3.28-vedio/sing-box.sh)
```

脚本交互界面出现后，根据提示选择语言和安装选项；需要应急测试的协议为 **Hysteria2（Hy）**。完成部署后，记录生成的端口，并在服务商安全组和系统防火墙中放行对应的 **UDP 端口**。

如果希望自动填写参数、使用中文极速安装，可运行：

```bash
bash <(wget -qO- https://raw.githubusercontent.com/kjxv/sing-box/v1.3.28-vedio/sing-box.sh) -l
```

该标签固定用于本期教程，后续 `main` 同步上游不会改变这条命令对应的脚本。具体版本信息和使用说明见 [v1.3.28-vedio Release](https://github.com/kjxv/sing-box/releases/tag/v1.3.28-vedio)。已有部署的用户应先保留原配置，避免覆盖正在使用的服务。

!!! danger "运行远程脚本前请确认"
    上面的命令会下载并以服务器权限直接执行脚本。建议先打开 [kjxv/sing-box 项目页面](https://github.com/kjxv/sing-box) 查看来源和更新记录。谨慎操作时，也可以先下载并检查脚本，再手动执行：

    ```bash
    wget -O sing-box.sh https://raw.githubusercontent.com/kjxv/sing-box/v1.3.28-vedio/sing-box.sh
    less sing-box.sh
    bash sing-box.sh
    ```

### 第三步：导出并测试 Hy 节点

安装完成后，可以运行下面的快捷命令查看节点信息：

```bash
sb -n
```

复制生成的 Hysteria2 节点链接，导入 v2rayN 等兼容客户端后进行延迟和连接测试。如果节点无法使用，请优先检查：

1. 安全组和系统防火墙是否放行了生成的 **UDP 端口**；
2. 客户端是否支持 Hysteria2；
3. VPS 的公网 IP 是否仍然可以从当前网络访问；
4. 服务器时间、域名解析和出站网络是否正常。

> 能通过代理登录 SSH，只说明这条代理能够访问服务器，不代表新部署的 Hy 节点一定能从本地直连使用。如果测试仍失败，可联系服务商更换 IP，或按方案三选择其他可用 VPS。

---

## 方案二：联系客服或提交工单更换 IP { #plan-2-change-ip }

如果希望继续使用原 VPS，可以联系服务商客服，或在用户后台提交工单，说明当前网络无法连接，请客服协助检查，并咨询是否支持更换公网 IP。

**如果暂时不着急使用，建议先等几天，待情况相对稳定后再考虑更换。** 如果急需恢复，可先用临时订阅，或尝试其他应急方案；新 IP 是否可用仍需实际测试。

提交工单前，准备好以下信息：

- VPS 订单号、实例名称、当前 IP，以及大致开始异常的时间；
- 当前使用的运营商和地区，SSH、面板和节点分别是否可以连接；
- 询问能否免费更换、是否收费，以及换 IP 是否影响现有数据。

客服完成更换后，将 FinalShell 的服务器地址、客户端节点地址及必要的域名解析更新为新 IP，再重新测试。**不要把更换 IP 等同于重装系统**，是否需要重建实例、数据能否保留，应以客服明确说明为准。

---

## 方案三：选择目前可用的 VPS { #plan-3-vps }

如果原服务器已经无法使用，或者需要继续搭建住宅 IP 出口，可以先选择一台当前连接正常的 VPS 作为中转或基础服务器，再在其后配置自己合法持有或授权使用的住宅 IP 服务。

按目前整理的反馈，可优先测试以下备选。Panstar 截图记录的是 **2026 年 10 月 27 日** 的测试情况，不能代表之后每个时间点、每个运营商的连接状态。

| 备选产品 | 更适合的场景 |
| --- | --- |
| 美国三网精品 VPS | 面向美国方向使用，作为临时中转或住宅 IP 前置服务器 |
| 德国 9929 VPS | 需要欧洲地区出口或中欧方向连接的用户 |
| 香港 Pro VPS | 更看重亚洲地区延迟和香港方向连接的用户 |
| JTTI 日本轻量云 | 需要日本方向服务器，可先测试该线路在本地运营商的可用性 |

![Panstar 美国、德国和香港节点当日连接测试情况](images/06-panstar-vps-test.png)

!!! info "测试结果具有时效性"
    截图只代表测试当时的网络情况。线路状态、延迟、库存和价格都可能发生变化，购买前建议先月付测试，并以官网实时显示为准。

### Panstar：美国、德国 9929、香港 Pro

[进入 Panstar 注册页面](https://panstar.ai/register?aff=DCAD1VCH)

![Panstar 购买指引](images/Panstar购买指引.png)

---

### JTTI：日本轻量云

[进入 JTTI 日本轻量云页面](https://www.jtti.cc/zh/light_cloud.html?k=T7KBH7) · [查看本站 JTTI 详细下单教程](../2026-10-26-VPS-JTT/index.md)

![JTTI 日本轻量云购买操作指引](images/Jtti日本云购买操作指引.png)

[查看本站 VPS 实测推荐与套餐说明](../../recommend/1-vps/index.md)

> **注意：** VPS 本身通常属于机房 IP。若最终目标是住宅 IP，需要在可用 VPS 上继续配置合规的住宅代理或 ISP 出口；购买 Panstar VPS 并不等于直接获得住宅 IP。

---

<span id="plan-1-wireguard" class="emergency-anchor"></span>

## 方案四：WireGuard 隧道 { #plan-4-wireguard }

本方案适合**仍能登录 3X-UI 控制台，且服务器的 UDP 端口可以访问**的用户。出口仍然是 VPS 的机房 IP。Windows 用户请先安装 [WireGuard 官方客户端](https://www.wireguard.com/install/)。

### 第一步：创建 WireGuard 入站

进入 3X-UI 入站列表，点击 **「添加入站」**，协议选择 **WireGuard**，填写备注，并设置一个未被占用的高位端口。在服务商安全组和系统防火墙中放行对应的 **UDP 端口**。

![在 3X-UI 中创建 WireGuard 入站并设置 UDP 端口](images/01-create-wireguard-inbound.png)

点击 **「保存更改」**，确认该入站已启用。截图中的端口仅作演示，请使用自己的端口。

### 第二步：复制配置

进入对应客户端详情，在 **「WireGuard 配置」** 一栏点击复制按钮，复制完整配置。

![在客户端详情中复制 WireGuard 配置文件](images/02-copy-wireguard-config-redacted.png)

!!! warning "保管好自己的配置"
    配置包含私钥和服务器连接信息，请使用自己控制台生成的内容。图中敏感信息已隐藏，不要照抄，也不要公开自己的配置、二维码或私钥。

### 第三步：保存为 `.conf` 文件

新建记事本文档，粘贴刚复制的配置，再点击 **「文件 → 另存为」**。文件名可填写 `emergency-wg.conf`，保存类型选择 **「所有文件」**，编码保留 UTF-8，确认文件名末尾是 **`.conf` 而非 `.conf.txt`**。

![将 WireGuard 配置保存为 conf 文件](images/03-save-wireguard-config-redacted.png)

### 第四步：导入并启用隧道

打开 WireGuard，点击左下角 **「新建隧道」** 旁边的下拉菜单，选择 **「从文件导入隧道」**，打开刚保存的 `.conf` 文件。选中新隧道，点击 **「连接」或「启用」**。

![在 WireGuard 客户端中从文件导入隧道](images/04-import-wireguard-tunnel.png)

### 第五步：检查实际连接

确认客户端有**最近握手时间**、接收与发送流量发生变化，再查询浏览器出口 IP，并实际打开需要使用的网页。仅看到「已连接」不能单独证明服务器已经连通。

![检查 WireGuard 握手、流量与出口 IP](images/05-verify-wireguard-connection-redacted.png)

没有握手时，先检查入站是否启用、`Endpoint` 地址和端口是否正确、UDP 是否放行，以及当前网络能否访问该 VPS。有握手但网页打不开时，再检查 DNS、`AllowedIPs`、服务器转发与 NAT。

如果控制台或公网 IP 已经完全不可达，WireGuard 也不能保证恢复。可以按方案二联系服务商，或按方案三准备可用 VPS。原有线路恢复后，可停用临时隧道，再按需删除配置和入站。

---

## 如何选择

- **当前没有可用代理，想先救急：** 先尝试上面的临时共享订阅，并测试实际连接。
- **能通过 SSH 直连，或能通过本地代理登录 VPS：** 尝试方案一部署 Hy 节点。
- **想保留原服务器且不着急使用：** 按方案二联系服务商，待情况稳定后再考虑换 IP。
- **原服务器无法使用、又急需恢复：** 按方案三测试其他可用 VPS。
- **能登录 3X-UI，且 UDP 仍可达：** 可尝试方案四 WireGuard。
- **必须使用住宅 IP：** 在可用 VPS 的基础上，另行配置自己拥有使用权限的住宅 IP 服务。

本文方案仅用于正常的网络维护、远程办公和个人服务恢复。请遵守所在国家或地区的法律法规以及服务商条款，不要用于未经授权的访问或其他违规用途。
