---
date: 2026-09-07
categories:
  - 工具视频教程
slug: clash
tags:
  - 工具
  - 代理软件
---

# ✈️ Clash Verge 链式代理配置静态住宅 IP 教程：有效减少账号风控 | TikTok / ChatGPT 节点丨极速Cloud

![封面图](images/fm.png){ .hide-in-post width="300" align="left" style="border-radius: 8px; margin-right: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 10px;" }

<p class="hide-in-post"><strong>本期看点：</strong> Clash Verge 配置静态住宅代理，模拟海外真实用户的身份。这样做的最大好处，是可以有效减少 TikTok、Facebook 以及 ChatGPT 等 AI 平台对你账号的风控和限流。</p>

<div style="clear: both;" class="hide-in-post"></div>

<!-- more -->

<style>
  /* 隐藏封面和摘要 */
  .hide-in-post { display: none !important; }
  /* 选填：给大标题上方加点间距，避免和挪下来的视频贴得太紧 */
  h1 { margin-top: 25px !important; }
</style>

<div id="top-video" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
  <iframe src="https://www.youtube.com/embed/2yXHbEBhHeU" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
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

## 📺 一、视频相关链接
1. 视频同款机场【极速 Cloud】：[点击跳转官网][极速Cloud] 
1. 视频同款静态住宅IP【Webshare】：[点击跳转官网][webshare]

---

1. 更多机场推荐文档：[点击 查看详情][机场推荐表]
1. 更多静态住宅IP推荐文档：[点击 查看详情][静态代理推荐表]
1. 自建**独享**VPN节点：
--8<-- "includes/videos.md:webshare-2026"
1. TG交流群：[https://t.me/xiaovchat](https://t.me/xiaovchat)


## 🛠️ 二、配套软件与工具

1. Clash Verge Rev（Windows 电脑版）：[https://github.com/Clash-Verge-rev/clash-verge-rev/releases](https://github.com/Clash-Verge-rev/clash-verge-rev/releases/latest?utm_source=chatgpt.com)
1. IP测试网站-1：[ping0.cc](https://ping0.cc/)
1. IP测试网站-2：[ippure.com](https://ippure.com/)
1. 测速网站：[speedtest.net](https://speedtest.net)

## 🔢 三、ChatGPT 静态住宅 IP 自动分流

- 静态IP节点添加格式
```
socks5://账号:密码@IP地址:端口#节点名称
```

- ChatGPT 静态住宅 IP 自动分流代码：
```
// ======================================================
// ChatGPT 静态住宅 IP 自动分流
// ======================================================


// 总开关
// true  = 开启
// false = 关闭
const ENABLE_CHATGPT_PROXY = true;

// 静态住宅 IP 信息
const RESIDENTIAL_PROXY = {
  name: "🏠 ChatGPT美国静态住宅IP",

  type: "socks5",

  server: "IP地址",
  port: 端口号,

  username: "账号",
  password: "密码"

  // 如果你的 SOCKS5 服务商明确支持 UDP，
  // 可以在 password 后面加逗号，然后开启：
  //
  // udp: true
};


// ======================================================
// ② ChatGPT 专用策略组名称
// ======================================================

const CHATGPT_GROUP = "🤖 ChatGPT专用";


// ======================================================
// ③ OpenAI / ChatGPT 核心域名
// ======================================================
//
// 使用 DOMAIN-SUFFIX。
// 一个后缀规则会自动覆盖所有子域名。
//
// 例如：
// chatgpt.com
// ├─ chatgpt.com
// ├─ ab.chatgpt.com
// ├─ ws.chatgpt.com
// └─ xxx.chatgpt.com
//
// oaistatic.com
// ├─ oaistatic.com
// └─ persistent.oaistatic.com
//
// openai.com
// ├─ openai.com
// ├─ chat.openai.com
// ├─ auth.openai.com
// ├─ desktop.chat.openai.com
// └─ 其他 *.openai.com
// ======================================================

const openaiSuffixDomains = [

  // ---------- OpenAI / ChatGPT 核心 ----------

  "chatgpt.com",
  "openai.com",

  // 静态资源
  "oaistatic.com",

  // 用户上传 / 下载 / 图片 / 文件资源
  "oaiusercontent.com",

  // OpenAI 统计 / 签名相关
  "oaistatsig.com",

  // OpenAI CDN / 合并资源
  "openaimerge.com",


  // ---------- OpenAI 官方使用的第三方服务 ----------

  // 邮件服务
  "ct.sendgrid.net",

  // Intercom
  "intercom.io",
  "intercomcdn.com",


];


// ======================================================
// ④ OpenAI 官方使用的第三方精确域名
// ======================================================
//
// 这些域名不是 openai.com / chatgpt.com 子域，
// 因此需要单独添加。
// ======================================================

const openaiExactDomains = [

  // --------------------------------------------------
  // WorkOS / 登录与身份认证
  // --------------------------------------------------

  "cdn.workos.com",
  "forwarder.workos.com",
  "setup.workos.com",
  "images.workoscdn.com",
  "workos.imgix.net",


  // --------------------------------------------------
  // Cloudflare 人机验证
  // --------------------------------------------------

  "challenges.cloudflare.com",


  // --------------------------------------------------
  // Stripe
  // --------------------------------------------------

  "js.stripe.com",


  // --------------------------------------------------
  // Sentry 错误监控
  // OpenAI 官方列出的地址
  // --------------------------------------------------

  "o207216.ingest.sentry.io",
  "o33249.ingest.sentry.io",


  // --------------------------------------------------
  // Windows ChatGPT 桌面端实测出现
  // 这是你刚才 Clash 连接页面实际看到的地址
  // --------------------------------------------------

  "o33249.ingest.us.sentry.io",


  // --------------------------------------------------
  // Datadog
  // --------------------------------------------------

  "rum.browser-intake-datadoghq.com",


  // --------------------------------------------------
  // Apple 相关
  // 官方网络清单中包含
  // --------------------------------------------------

  "humb.apple.com"
];


// ======================================================
// ⑤ 自动生成 ChatGPT 分流规则
// ======================================================

const chatgptRules = [

  // 核心域名以及所有子域名
  ...openaiSuffixDomains.map(
    domain => `DOMAIN-SUFFIX,${domain},${CHATGPT_GROUP}`
  ),

  // 第三方精确域名
  ...openaiExactDomains.map(
    domain => `DOMAIN,${domain},${CHATGPT_GROUP}`
  )
];


// ======================================================
// ⑥ 主程序
// ======================================================

function main(config, profileName) {

  // 总开关关闭时，不对原订阅做任何修改
  if (!ENABLE_CHATGPT_PROXY) {
    return config;
  }

  if (!Array.isArray(config.proxies)) {
    config.proxies = [];
  }

  if (!Array.isArray(config["proxy-groups"])) {
    config["proxy-groups"] = [];
  }

  if (!Array.isArray(config.rules)) {
    config.rules = [];
  }



  // ==================================================
  // ⑦ 添加 / 更新静态住宅 IP 节点
  // ==================================================

  // 删除同名旧节点，避免重复
  config.proxies = config.proxies.filter(
    proxy => proxy.name !== RESIDENTIAL_PROXY.name
  );

  // 加入最新住宅节点
  config.proxies.push(RESIDENTIAL_PROXY);


  // ==================================================
  // ⑧ 创建 ChatGPT 专用策略组
  // ==================================================

  // 删除同名旧策略组，避免重复
  config["proxy-groups"] = config["proxy-groups"].filter(
    group => group.name !== CHATGPT_GROUP
  );


  // 把 ChatGPT 专用组放到最前面
  config["proxy-groups"].unshift({

    name: CHATGPT_GROUP,

    type: "select",

    proxies: [

      // 默认使用静态住宅IP
      RESIDENTIAL_PROXY.name,

      // 临时排错备用
      "DIRECT"
    ]
  });


  // ==================================================
  // ⑨ 防止规则重复
  // ==================================================

  config.rules = config.rules.filter(
    rule => !chatgptRules.includes(rule)
  );


  // ==================================================
  // ⑩ ChatGPT 规则放到所有机场规则最前面
  // ==================================================
  //
  // 非常重要。
  //
  // 这样 ChatGPT 域名会先命中我们的规则，
  // 不会被机场订阅自带的：
  //
  // MATCH
  // PROXY
  // GEOIP
  // GEOSITE
  //
  // 等规则提前接走。
  // ==================================================

  config.rules = [
    ...chatgptRules,
    ...config.rules
  ];


  // 返回最终配置
  return config;
}
```



!!! abstract "上方是视频中用到的网址。"


---


!!! Warning "**免责声明**"
    本文档及相关教程内容仅供计算机网络技术交流与学习测试使用。请务必严格遵守您所在国家或地区的法律法规，切勿用于任何非法用途。
    
--8<-- "includes/links.md"