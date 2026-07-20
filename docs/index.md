---
hide:
  - navigation
  - toc
---

# 小V博客

<section class="home-hero" aria-labelledby="home-title">
    <div class="home-hero__inner">
        <p class="home-kicker">Digital Tools & Practical Notes</p>
        <h1 id="home-title">小V博客</h1>
        <p class="home-subtitle">
            记录跨境工具、网络环境、VPS 建站、账号配置和常用软件教程，把视频里的实操步骤整理成方便检索的文字资料。
        </p>
    </div>
</section>

<main class="home-main" aria-label="首页内容">
    <section class="home-section home-intro">
        <p class="home-section__eyebrow">本站内容</p>
        <h2>从视频教程到文字资料，方便你随时复查</h2>
        <p>
            这里主要整理我在实操和视频里用到的工具链接、配置步骤、资源推荐和风险提示。内容会围绕建站、VPS、网络环境、虚拟卡、住宅 IP、常用工具和数字出海资源持续更新。
        </p>
    </section>

    <section class="home-section">
        <div class="home-section__head">
            <p class="home-section__eyebrow">主要栏目</p>
            <h2>快速进入常用内容</h2>
        </div>

        <div class="home-grid">
            <a class="home-card" href="blog/">
                <span>视频文档</span>
                <strong>教程文章与视频补充</strong>
                <p>整理视频中提到的步骤、工具链接、命令和注意事项。</p>
            </a>
            <a class="home-card" href="recommend/">
                <span>站长推荐</span>
                <strong>出海工具与资源导航</strong>
                <p>按 VPS、虚拟卡、住宅 IP、交易所、节点和账号资源分类。</p>
            </a>
            <a class="home-card" href="tools/">
                <span>工具文档</span>
                <strong>软件安装与使用说明</strong>
                <p>沉淀常用工具、Openclaw 和服务器相关文档。</p>
            </a>
        </div>
    </section>

    <section class="home-section home-latest">
        <div class="home-section__head">
            <p class="home-section__eyebrow">最近更新</p>
            <h2>最新教程</h2>
        </div>

        <div class="home-list">
            <a href="blog/2026/05/27/wordpress/">
                <strong>跨境独立站搭建教程：建站、网络环境与 Shopify 替代方案</strong>
                <span>适合想搭建独立站的新手，用来复查建站准备和网络环境配置。</span>
            </a>
            
        </div>
    </section>

    <section class="home-section home-note">
        <div>
            <p class="home-section__eyebrow">站点说明</p>
            <h2>内容以个人经验和公开资料整理为主</h2>
            <p>
                第三方工具、平台政策、价格和可用性都可能变化。涉及账号、支付、网络环境和金融平台时，请结合官方说明、平台条款和当地法律法规自行判断。
            </p>
        </div>
        <div class="home-policy">
            <a href="about/">关于本站</a>
            <a href="privacy/">隐私政策</a>
            <a href="disclaimer/">免责声明</a>
        </div>
    </section>
</main>

<style>
  .md-main {
      background: #f7f9fc;
  }

  .md-main__inner {
      max-width: none;
      margin: 0;
  }

  .md-content {
      background: transparent;
  }

  .md-content__inner {
      margin: 0 !important;
      padding: 0 !important;
  }

  .md-content__inner > h1,
  .md-typeset > h1:first-child {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
  }

  .home-hero {
      position: relative;
      min-height: 430px;
      display: flex;
      align-items: center;
      overflow: hidden;
      color: #ffffff;
      background:
          linear-gradient(90deg, rgba(5, 12, 24, 0.9), rgba(5, 12, 24, 0.62) 48%, rgba(5, 12, 24, 0.34)),
          url("assets/home-tech-bg.png") center / cover no-repeat;
  }

  .home-hero::after {
      content: "";
      position: absolute;
      inset: auto 0 0;
      height: 120px;
      background: linear-gradient(180deg, rgba(247, 249, 252, 0), #f7f9fc);
      pointer-events: none;
  }

  .home-hero__inner {
      position: relative;
      z-index: 1;
      width: min(920px, calc(100% - 40px));
      margin: 0 auto;
      padding: 72px 0 96px;
  }

  .home-kicker,
  .home-section__eyebrow {
      margin: 0 0 14px;
      color: #17c3e6;
      font-size: 0.72rem;
      font-weight: 800;
      letter-spacing: 0.18em;
      line-height: 1.2;
      text-transform: uppercase;
  }

  .home-hero h1 {
      margin: 0;
      color: #ffffff;
      font-size: clamp(2.4rem, 6vw, 5.4rem);
      line-height: 1;
      letter-spacing: 0;
      text-shadow: 0 18px 54px rgba(0, 0, 0, 0.5);
  }

  .home-subtitle {
      max-width: 720px;
      margin: 24px 0 0;
      color: rgba(240, 250, 255, 0.9);
      font-size: 1.02rem;
      line-height: 1.9;
      text-shadow: 0 12px 36px rgba(0, 0, 0, 0.42);
  }

  .home-main {
      width: min(1080px, calc(100% - 40px));
      margin: -42px auto 0;
      padding: 0 0 72px;
      color: #172033;
  }

  .home-section {
      margin-bottom: 52px;
  }

  .home-intro,
  .home-note {
      padding: 28px;
      border: 1px solid rgba(37, 58, 92, 0.08);
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.92);
      box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
  }

  .home-section h2 {
      margin: 0 0 14px;
      color: #0f172a;
      font-size: clamp(1.35rem, 2.4vw, 2rem);
      line-height: 1.28;
      letter-spacing: 0;
  }

  .home-section p {
      max-width: 820px;
      margin: 0;
      color: #475569;
      line-height: 1.9;
  }

  .home-section__head {
      margin-bottom: 18px;
  }

  .home-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
  }

  .home-card {
      min-height: 176px;
      padding: 22px;
      border: 1px solid rgba(37, 58, 92, 0.1);
      border-radius: 8px;
      color: inherit !important;
      background: #ffffff;
      text-decoration: none !important;
      box-shadow: 0 14px 38px rgba(15, 23, 42, 0.06);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }

  .home-card:hover {
      transform: translateY(-4px);
      border-color: rgba(23, 195, 230, 0.55);
      box-shadow: 0 20px 46px rgba(15, 23, 42, 0.1);
  }

  .home-card span {
      display: block;
      margin-bottom: 14px;
      color: #0891b2;
      font-size: 0.78rem;
      font-weight: 800;
  }

  .home-card strong {
      display: block;
      color: #0f172a;
      font-size: 1.05rem;
      line-height: 1.45;
  }

  .home-card p {
      margin-top: 12px;
      color: #64748b;
      font-size: 0.86rem;
      line-height: 1.75;
  }

  .home-list {
      display: grid;
      gap: 10px;
  }

  .home-list a {
      display: grid;
      gap: 6px;
      padding: 18px 20px;
      border: 1px solid rgba(37, 58, 92, 0.08);
      border-left: 3px solid #17c3e6;
      border-radius: 8px;
      color: inherit !important;
      background: #ffffff;
      text-decoration: none !important;
      box-shadow: 0 12px 28px rgba(15, 23, 42, 0.045);
  }

  .home-list strong {
      color: #0f172a;
      font-size: 0.98rem;
      line-height: 1.55;
  }

  .home-list span {
      color: #64748b;
      font-size: 0.84rem;
      line-height: 1.7;
  }

  .home-note {
      display: grid;
      grid-template-columns: 1fr minmax(220px, 300px);
      gap: 28px;
      align-items: start;
  }

  .home-policy {
      display: grid;
      gap: 10px;
  }

  .home-policy a {
      padding: 12px 14px;
      border: 1px solid rgba(37, 58, 92, 0.1);
      border-radius: 8px;
      color: #0f172a !important;
      background: #f8fafc;
      text-decoration: none !important;
      font-weight: 700;
  }

  @media screen and (max-width: 900px) {
      .home-grid,
      .home-note {
          grid-template-columns: 1fr;
      }
  }

  @media screen and (max-width: 600px) {
      .home-hero {
          min-height: 360px;
      }

      .home-hero__inner {
          padding: 56px 0 82px;
      }

      .home-main {
          width: min(100% - 28px, 1080px);
          margin-top: -34px;
          padding-bottom: 52px;
      }

      .home-intro,
      .home-note,
      .home-card,
      .home-list a {
          padding: 18px;
      }
  }
</style>
