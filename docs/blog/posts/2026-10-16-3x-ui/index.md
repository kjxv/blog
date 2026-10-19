---
date: 2026-10-16
categories:
  - 工具视频教程
slug: uszhibo
tags:
  - 跨境工具

---

# 🌍 最简单的VPN搭建教程｜3x-ui一键部署｜VPS自建节点｜静态住宅IP配置

![封面图](images/fm.png){ .hide-in-post width="300" align="left" style="border-radius: 8px; margin-right: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;" }

<p class="hide-in-post"><strong>本期看点：</strong>有手就行！</p>

<div style="clear: both;" class="hide-in-post"></div>

<!-- more -->

<style>
  /* 隐藏封面和摘要 */
  .hide-in-post { display: none !important; }
  /* 选填：给大标题上方加点间距，避免和挪下来的视频贴得太紧 */
  h1 { margin-top: 25px !important; }
</style>

<div id="top-video" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <iframe src="https://www.youtube.com/embed/" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

<script>
  (function(){
    var video = document.getElementById('top-video');
    var h1 = document.querySelector('h1'); // 抓取文档生成的第一个大标题
    if(video && h1) {
      h1.parentNode.insertBefore(video, h1); // 把视频节点插入到大标题前面
    }
  })();
</script>


---

## 📺 视频相关链接

1. 🍺 本期视频同款——中转VPS（精品线路）:[点击跳转](https://bwh81.net/aff.php?aff=81595&pid=87)
1. ➡️ 本期视频同款——美国住宅IP（每月不到8元）:[点击跳转][webshare]

1. 📖 其他中转服务器（VPS）：[点击查看详情][VPS推荐表]
1. 🌍 其他静态住宅IP：[点击查看详情][静态代理推荐表]


1. ✈️ TG交流群：[https://t.me/xiaovchat](https://t.me/xiaovchat)

!!! abstract "上方是视频中用到的网址。"

## 🛠️ 代理软件
1. V2rayN（Windows 电脑版）：[https://github.com/2dust/v2rayN/releases](https://github.com/2dust/v2rayN/releases)
1. V2rayNG（Android 手机版）：[https://github.com/2dust/v2rayNG/releases](https://github.com/2dust/v2rayNG/releases)
1. Clash Verge Rev（Windows 电脑版）：[https://github.com/Clash-Verge-rev/clash-verge-rev/releases](https://github.com/Clash-Verge-rev/clash-verge-rev/releases/latest?utm_source=chatgpt.com)
1. Clash Meta for Android(Android 手机端):[https://github.com/MetaCubeX](https://github.com/MetaCubeX/ClashMetaForAndroid/releases/latest?utm_source=chatgpt.com)
1. Shadowrocket(小火箭)，请自行在苹果AppStore中下载

## 🔠 视频相关命令：

1. 服务器远程连接工具（FinalShell）： [https://www.hostbuf.com/t/988.html](https://www.hostbuf.com/t/988.html)

1. 安装Curl（PanstarVPS需要安装Curl，其他推荐VPS不需要）
```
apt update && apt install -y curl
```

- 安装Curl（以上如果报错，尝试一下命令）
```
apt-get install -y --allow-downgrades curl/bullseye
```


1. 3X-UI一键部署命令(版本 3.10.2)：
```bash
bash <(curl -fLsS https://raw.githubusercontent.com/kjxv/3x-ui/v3.10.2-preset/deploy/preset/install.sh)
```
> 项目原地址：https://github.com/mhsanaei/3x-ui感谢原作者 mhsanaei 以及所有参与该项目开发、维护和贡献的开源作者。
---


!!! Warning "**免责声明**"
    本文档及相关教程内容仅供计算机网络技术交流与学习测试使用。请务必严格遵守您所在国家或地区的法律法规，切勿用于任何非法用途。
    
--8<-- "includes/links.md"