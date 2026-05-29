---
date: 2026-05-27
categories:
  - 工具视频教程
slug: wordpress
tags:
  - 福利
  - AI
---

# 🛠️ 1Panel + WordPress 极速建站与运维调优全攻略

![封面图](../../assets/images/muban.png){ width="300" align=left style="border-radius: 8px; margin-right: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;" }

**本期要点：** [这里简述视频的核心价值，吸引读者往下看]。本教程手把手带你通过验证，建议收藏！

<div style="margin-top: 25px; text-align: center;">
  <a href="[YouTube链接]" target="_blank" class="md-button md-button--neutral" style="display: inline-flex; align-items: center; gap: 8px; padding: 10px 24px; font-size: 0.85rem; border-radius: 20px; text-decoration: none; font-weight: bold; border: 1px solid rgba(0,0,0,0.1); transition: all 0.3s ease;">
    <svg viewBox="0 0 576 512" style="height: 1.1em; fill: #FF0000; margin: 0; display: block;"><path d="M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.781 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z"/></svg>
    立即观看完整视频
  </a>
</div>

<br clear="left">
<!-- more -->
---



## 🌍 第一步：核心资产准备

> **准备工作：** 包含本期视频演示的云服务器（VPS）、域名。

* **服务器（VPS）推荐与测评结果：** [👉 点击查看详情与评测](https://tgl2775284503-hash.github.io/blog/recommend/1-vps/)
* **老牌廉价域名商（NameSilo）：** [👉 点击跳转官网选购（支持支付宝）](https://www.namesilo.com/?rid=1586892lc)
* **免税州美国地址生成器：** [👉 点击跳转生成资料](https://addressgenerator.top/us-address-generator)

> **服务器链接工具（以下两种，随便选择一个）：** 包含本期视频演示的云服务器（VPS）、域名。

* **Finalshel 远程链接工具：**[https://www.hostbuf.com](https://www.hostbuf.com/t/988.html)
* **Xshell 远程链接工具：**[https://www.xshell.com/zh](https://www.xshell.com/zh/free-for-home-school/)

---

## 🚀 第二步：环境初始化与面板安装

### 1. 内存优化（1G内存服务器必做：开启 2GB Swap 交换分区）
```bash
# 1. 检查当前内存与 Swap 状态
free -m

# 2. 物理创建一个 2GB 的优质 Swap 交换文件
fallocate -l 2G /swapfile

# 3. 设置严格的安全权限
chmod 600 /swapfile

# 4. 将该文件格式化为 Swap 分区
mkswap /swapfile

# 5. 立即启用该 Swap 激活内存
swapon /swapfile

# 6. 写入系统配置，防止服务器重启后失效
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# 7. 再次查看内存状态，确认 Swap 已成功变为 2048MB 左右
free -m

```

### 2. 安装 1Panel 面板（支持 Ubuntu / Debian 系统）

```bash
curl -sSL https://resource.fit2cloud.com/1panel/package/quick_start.sh -o quick_start.sh && bash quick_start.sh

```

---

## 🌐 第三步：WordPress 博客与独立站搭建

### 1. DNS 解析配置

* 登录 **NameSilo** 后台。
* 添加一条 `A` 记录：名称填 `@` 或 `www`，内容填你的 **服务器公网 IP**。

### 2. 1Panel 一键部署顺序

1. 在应用商店中先安装 **OpenResty**（Web 服务器网关）。
2. 在应用商店中安装 **MariaDB（或 MySQL）** 数据库。
3. 在应用商店中搜索并一键安装 **WordPress**。
4. **网站配置域名**：进入 1Panel「网站」列表 -> 绑定你的自定义域名，并一键申请 Let's Encrypt 免费 SSL 证书。
5. 安装Blocksy主题插件 → 选择网站主题
6. 设置wordpress的地址调整为域名
6. 安装备份插件：WPvivid
8. 备份，并下载到本地电脑
9. 在新服务器上按照以上操作，安装1Panel、OpenResty、MariaDB（或 MySQL）、WordPress
10.在Wordpress上安装插件（WPvivid），选择上传 → 备份文件 → 还原谢谢！事情。嗯。
---


### 💁 个人独享网络节点搭建

🤷‍♂️ 3x-ui 可视化面板 (🌟手动添加节点、更加灵活)

* **特点：** 自带 Web 图形界面。
* **优势：** 像设置路由器一样简单，后期管理、修改链式节点极方便。
* **部署命令：**
```bash
bash <(curl -Ls https://raw.githubusercontent.com/tgl2775284503-hash/3x-ui/video-v2.9.4/install.sh)
```

❤️ 饮水思源，感谢 3X-UI 原作者 (mhsanaei) 的开源奉献！想折腾最新版的兄弟可以去原项目主页，记得顺手给大佬点个赞！

* **3X-UI 官方原项目地址：**[https://github.com/mhsanaei/3x-ui](https://github.com/mhsanaei/3x-ui)

---

## 🔑 其他：WordPress 忘记密码救砖方案

> **核心思路：** 如果后台密码死活登不上，直接通过 1Panel 强行修改底层数据库字段。

1. **准备工作**：在 1Panel 的「应用商店」里点击安装 **phpMyAdmin**（数据库图形化管理工具）。
2. **获取凭证**：进入 1Panel「应用」-> 找到已安装的 `mariadb/mysql` -> 点击「参数」，查看并复制**数据库连接的 Root 账号与密码**。
3. **登录后台**：打开 phpMyAdmin 网页，**服务器名称**填写 `mariadb`（或 `mysql`），并输入上一步拿到的密码登录。
4. **重置密码字段**：
* 在左侧数据库列表中找到 WordPress 对应的数据库，点击进入。
* 找到 **`wp_users`** 表。
* 找到你的管理员账号那一行，点击 **「编辑 (Edit)」**。
* **`user_login` 字段**：删除原有内容，直接填写你想换的**新登录账号**。
* **`user_pass` 字段**：下拉函数菜单务必选择 **`MD5`**（核心加密算法），并在右侧输入框中直接填入你的**明文新密码**。
* 点击页面最下方的 **「执行 (Go)」** 即可瞬间救砖成功。



---

## ⚠️ 免责声明

* 本文及视频内容仅供网络技术交流与个人博客搭建演示使用，请自觉遵守当地法律法规，切勿用于任何非法网络用途。

```

