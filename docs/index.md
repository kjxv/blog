---
# 1. YAML 配置：彻底隐藏导航栏、右侧目录、默认页脚，只留纯净首屏
hide:
  - navigation
  - toc
  - footer
---

<div class="hero-video-wrapper">
    <div class="hero-overlay"></div>
    <video autoplay loop muted playsinline>
        <source src="assets/home-bg.mp4" type="video/mp4">
    </video>
</div>

<div class="hero-container">
    <div class="hero-topbar">
        <a href="./" class="hero-logo" aria-label="V站首页">
            <img class="hero-logo-image" src="assets/site-logo-v.png" alt="V站">
        </a>
        <div class="hero-action-group">
            <a href="http://127.0.0.1:8000/blog/" class="hero-btn btn-cyan">视频文档</a>
            <a href="http://127.0.0.1:8000/recommend/" class="hero-btn btn-glass">站长推荐</a>
        </div>
    </div>

    <div class="hero-core-content">
        <div class="hero-kicker">Digital Playground</div>
        <div class="hero-typewriter">
            <span>Welcome everybody!</span>
            <span>Explore videos, tools, and ideas.</span>
            <span>Build smarter. Share better.</span>
        </div>
    </div>
</div>

<style>
  /* ----------------------------------------- */
  /* 基础画布：穿透 MkDocs 限制 */
  /* ----------------------------------------- */
  .md-main, .md-content {
      background-color: transparent !important;
  }
  .md-banner, .md-header, .md-tabs {
      display: none !important; 
  }
  .md-main {
      margin-top: 0 !important; 
  }
  .md-content__inner {
      margin: 0 !important;
      padding: 0 !important;
  }

  /* ----------------------------------------- */
  /* 视频背景与遮罩 */
  /* ----------------------------------------- */
  .hero-video-wrapper {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -2;
      pointer-events: none;
  }
  .hero-video-wrapper video {
      width: 100vw;
      height: 100vh;
      object-fit: cover;
      object-position: center center;
  }
  .hero-overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background:
          radial-gradient(circle at 17% 15%, rgba(84, 230, 246, 0.16), transparent 24%),
          linear-gradient(90deg, rgba(0, 0, 0, 0.58) 0%, rgba(0, 0, 0, 0.34) 34%, rgba(0, 0, 0, 0.12) 66%, rgba(0, 0, 0, 0.06) 100%),
          linear-gradient(180deg, rgba(3, 8, 20, 0.2), rgba(0, 0, 0, 0.48));
      z-index: -1;
  }

  /* ----------------------------------------- */
  /* 顶部品牌导航 */
  /* ----------------------------------------- */
  .hero-container {
      position: relative;
      width: 100%;
      min-height: 100vh;
      box-sizing: border-box;
      padding: 20px clamp(28px, 7vw, 112px);
  }

  .hero-topbar {
      position: fixed;
      top: 12px;
      left: 12px;
      right: clamp(22px, 3.4vw, 52px);
      display: flex;
      align-items: flex-start;
      gap: 12px;
      z-index: 2;
  }

  .hero-logo {
      display: inline-flex;
      align-items: center;
      width: 104px;
      height: 104px;
      padding: 0;
      text-decoration: none !important;
      border-radius: 16px;
      overflow: hidden;
      background: transparent;
      box-shadow: none;
  }

  .hero-logo-image {
      display: block;
      width: 100%;
      height: 100%;
      object-fit: contain;
      object-position: center;
  }

  .hero-kicker {
      display: inline-flex;
      width: fit-content;
      margin: 0 0 18px;
      color: rgba(226, 252, 255, 0.88);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.22em;
      line-height: 1.2;
      text-transform: uppercase;
      white-space: nowrap;
      text-shadow: 0 0 18px rgba(84, 230, 246, 0.32);
  }

  .hero-core-content {
      position: absolute;
      left: clamp(56px, 7vw, 120px);
      top: 42%;
      width: min(38vw, 520px);
      min-width: 360px;
      text-align: left;
      transform: translateY(-8%);
  }

  .hero-typewriter {
      position: relative;
      width: min(100%, 520px);
      min-height: 32px;
      margin: 0;
      color: rgba(233, 252, 255, 0.92);
      font-size: 1.08rem;
      font-weight: 600;
      letter-spacing: 0.03em;
      text-shadow: 0 0 18px rgba(84, 230, 246, 0.34);
  }

  .hero-typewriter span {
      position: absolute;
      left: 0;
      top: 0;
      width: 0;
      max-width: max-content;
      overflow: hidden;
      white-space: nowrap;
      border-right: 2px solid #54e6f6;
      opacity: 0;
      animation: typeCycle 12s steps(34, end) infinite;
  }

  .hero-typewriter span:nth-child(2) {
      animation-delay: 4s;
  }

  .hero-typewriter span:nth-child(3) {
      animation-delay: 8s;
  }

  /* ----------------------------------------- */
  /* 导航按钮 */
  /* ----------------------------------------- */
  .hero-action-group {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 18px;
  }
  
  .hero-btn {
      display: inline-block;
      padding: 9px 18px;
      color: #ffffff !important;
      font-size: 0.72rem;
      font-weight: 700;
      border-radius: 50px;
      border: 0;
      background: rgba(255, 255, 255, 0.13);
      text-decoration: none !important;
      transition: all 0.3s ease;
      text-align: center;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
  }
  
  .btn-cyan {
      background: rgba(255, 255, 255, 0.13);
  }
  .btn-cyan:hover {
      background: rgba(255, 255, 255, 0.24);
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(84, 230, 246, 0.16);
  }
  
  .btn-glass {
      background: rgba(255, 255, 255, 0.13);
  }
  .btn-glass:hover {
      background: rgba(255, 255, 255, 0.22);
      transform: translateY(-4px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
  }

  @keyframes typeCycle {
      0% { width: 0; opacity: 0; }
      5% { opacity: 1; }
      23% { width: 100%; opacity: 1; }
      29% { width: 100%; opacity: 1; }
      33% { width: 0; opacity: 0; }
      100% { width: 0; opacity: 0; }
  }

  /* ----------------------------------------- */
  /* 移动端完美适配 */
  /* ----------------------------------------- */
  @media screen and (max-width: 600px) {
      .hero-overlay {
          background:
              radial-gradient(circle at 50% 35%, rgba(84, 230, 246, 0.18), transparent 32%),
              linear-gradient(180deg, rgba(3, 8, 20, 0.38), rgba(0, 0, 0, 0.72));
      }
      .hero-container {
          padding: 20px;
      }
      .hero-topbar {
          top: 10px;
          left: 10px;
          right: 18px;
          flex-direction: row;
          align-items: flex-start;
          gap: 8px;
      }
      .hero-logo {
          width: 78px;
          height: 78px;
      }
      .hero-core-content {
          left: 20px;
          right: 20px;
          top: auto;
          bottom: 76px;
          width: auto;
          min-width: 0;
          text-align: center;
          transform: none;
      }
      .hero-kicker { margin: 0 auto 18px; font-size: 0.68rem; letter-spacing: 0.16em; }
      .hero-typewriter { width: min(92vw, 560px); min-height: 52px; margin: 0 auto; font-size: 0.95rem; }
      .hero-typewriter span { left: 50%; transform: translateX(-50%); }
      .hero-action-group { justify-content: flex-start; gap: 10px; margin-top: 12px; }
      .hero-btn { padding: 8px 12px; font-size: 0.68rem; box-sizing: border-box; }
  }
</style>
