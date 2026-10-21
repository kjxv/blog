---
title: 小V博客
hide:
  - navigation
  - toc
---

<nav class="home-nav" aria-label="首页主导航">
  <a class="home-nav__active" href="./">首页</a>
  <a href="blog/">专栏博客</a>
  <a href="recommend/">推荐资源</a>
  <a href="about/">关于本站</a>
  <a href="privacy/">隐私政策</a>
  <a href="disclaimer/">免责声明</a>
  <a href="services/remote-support/">技术支持</a>
</nav>

<section class="home-hero" aria-label="小V博客首页">
  <div class="home-hero__far" aria-hidden="true"></div>
  <div class="home-hero__near" aria-hidden="true"></div>
  <div class="home-hero__shade" aria-hidden="true"></div>

  <div class="home-hero__statement">
    <p>没有高端技术</p>
    <h1>只有<span>使用</span>的艺术</h1>
    <i aria-hidden="true"></i>
  </div>
</section>

<style>
  /* 首页只保留单行导航与沉浸式首屏 */
  .md-banner,
  .md-footer,
  .md-header__option {
    display: none;
  }

  html,
  body,
  .md-main {
    background: #173747;
  }

  /* Material 的品牌栏和标签栏在首页重叠为同一条导航 */
  .md-header,
  .md-tabs {
    position: fixed;
    top: 0;
    right: 0;
    left: 0;
    height: 3.2rem;
    color: rgba(255, 255, 255, 0.78);
    background: transparent;
    box-shadow: none;
  }

  .md-header {
    z-index: 20;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(9, 36, 49, 0.34);
    -webkit-backdrop-filter: blur(14px) saturate(110%);
    backdrop-filter: blur(14px) saturate(110%);
  }

  .md-header--shadow {
    box-shadow: 0 10px 30px rgba(3, 20, 29, 0.08);
  }

  .md-header__inner {
    width: 100%;
    max-width: none;
    height: 3.2rem;
    padding: 0 3.2rem;
  }

  .md-header__button,
  .md-header__title,
  .md-tabs__link {
    color: inherit;
  }

  .md-logo {
    width: 1.5rem;
    height: 1.5rem;
    margin: 0;
    padding: 0.18rem;
  }

  .md-logo svg {
    width: 100%;
    height: 100%;
  }

  .md-header__title {
    flex: 0 0 auto;
    width: auto;
    margin-left: 0.5rem;
    font-size: 0.98rem;
    font-weight: 650;
    letter-spacing: 0.02em;
  }

  .md-header__topic {
    position: static;
    opacity: 1 !important;
    transform: none !important;
  }

  .md-header__topic[data-md-component="header-topic"] {
    display: none;
  }

  .md-tabs {
    z-index: 21;
    pointer-events: none;
  }

  .md-tabs > .md-grid {
    display: flex;
    justify-content: center;
    width: 100%;
    max-width: none;
    height: 3.2rem;
  }

  .md-tabs__list {
    display: flex;
    height: 3.2rem;
    margin: 0;
    pointer-events: auto;
  }

  .md-tabs__item {
    height: 3.2rem;
    padding: 0 0.85rem;
  }

  .md-tabs__link {
    display: flex;
    align-items: center;
    height: 3.2rem;
    margin: 0;
    font-size: 0.7rem;
    font-weight: 430;
    letter-spacing: 0.015em;
    opacity: 0.72;
    transition: color 180ms ease, opacity 180ms ease;
  }

  .md-tabs__link:hover,
  .md-tabs__item--active .md-tabs__link {
    color: #fff;
    opacity: 1;
  }

  /* 搜索默认收成图标，聚焦后再展开 */
  .md-search {
    z-index: 24;
    flex: 0 0 2.2rem;
    width: 2.2rem;
    margin-left: auto;
    transition: width 220ms ease, flex-basis 220ms ease;
  }

  .md-search__inner,
  .md-search__form {
    width: 2.2rem;
    transition: width 220ms ease, background 220ms ease;
  }

  .md-search__form {
    background: transparent;
    box-shadow: none;
  }

  .md-search__input {
    width: 100%;
    padding: 0;
    color: #fff;
    opacity: 0;
    cursor: pointer;
    transition: opacity 160ms ease, padding 220ms ease;
  }

  .md-search__icon {
    color: rgba(255, 255, 255, 0.86);
  }

  .md-search:focus-within {
    flex-basis: 11.5rem;
    width: 11.5rem;
  }

  .md-search:focus-within .md-search__inner,
  .md-search:focus-within .md-search__form {
    width: 11.5rem;
  }

  .md-search:focus-within .md-search__form {
    border: 1px solid rgba(255, 255, 255, 0.14);
    background: rgba(255, 255, 255, 0.08);
  }

  .md-search:focus-within .md-search__input {
    padding: 0 1.9rem 0 2.2rem;
    opacity: 1;
    cursor: text;
  }

  .md-search__input::placeholder {
    color: rgba(255, 255, 255, 0.58);
  }

  .md-main {
    min-height: 0;
    padding-top: 0;
  }

  .md-main__inner,
  .md-content {
    width: 100%;
    max-width: none;
    margin: 0 !important;
  }

  [data-md-color-scheme="default"] article.md-content__inner,
  [data-md-color-scheme="slate"] article.md-content__inner {
    margin: 0;
    padding: 0;
    border-radius: 0;
    background: transparent;
    box-shadow: none;
  }

  .home-hero {
    --far-x: 0px;
    --far-y: 0px;
    --near-x: 0px;
    --near-y: 0px;
    --light-x: 50%;
    --light-y: 45%;
    position: relative;
    isolation: isolate;
    display: grid;
    min-height: 100svh;
    place-items: center;
    overflow: hidden;
    background: #173747;
  }

  .home-hero__far,
  .home-hero__near {
    position: absolute;
    inset: -5%;
    background: url("assets/home-seascape-v2.webp") center / cover no-repeat;
    pointer-events: none;
    will-change: transform;
  }

  .home-hero__far {
    z-index: -4;
    transform: translate3d(var(--far-x), var(--far-y), 0) scale(1.07);
  }

  /* 提取右侧岩石为近景层，移动幅度略大 */
  .home-hero__near {
    z-index: -3;
    opacity: 0.98;
    -webkit-mask-image:
      radial-gradient(ellipse 62% 76% at 104% 105%, #000 0%, #000 62%, transparent 82%);
    mask-image:
      radial-gradient(ellipse 62% 76% at 104% 105%, #000 0%, #000 62%, transparent 82%);
    transform: translate3d(var(--near-x), var(--near-y), 0) scale(1.085);
  }

  .home-hero__shade {
    position: absolute;
    z-index: -2;
    inset: 0;
    background:
      radial-gradient(circle at var(--light-x) var(--light-y), rgba(65, 101, 118, 0.1), rgba(10, 38, 52, 0.42) 68%, rgba(7, 30, 43, 0.58) 100%),
      linear-gradient(180deg, rgba(18, 53, 69, 0.38), rgba(16, 48, 62, 0.5));
    box-shadow: inset 0 -130px 170px rgba(7, 29, 41, 0.18);
    pointer-events: none;
  }

  .home-hero__statement {
    position: relative;
    z-index: 2;
    width: min(1050px, calc(100% - 80px));
    margin-top: -3vh;
    color: #fff;
    text-align: center;
  }

  .home-hero__statement p {
    margin: 0 0 0.9rem;
    color: rgba(255, 255, 255, 0.72);
    font-family: "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: clamp(1rem, 1.5vw, 1.4rem);
    font-weight: 380;
    letter-spacing: 0.16em;
    line-height: 1.4;
    text-shadow: 0 3px 22px rgba(2, 20, 30, 0.22);
  }

  .home-hero__statement h1 {
    margin: 0 !important;
    color: rgba(255, 255, 255, 0.98) !important;
    font-family: "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: clamp(2.65rem, 4.4vw, 4.1rem) !important;
    font-weight: 620 !important;
    letter-spacing: 0.055em;
    line-height: 1.2;
    text-shadow: 0 9px 34px rgba(2, 20, 30, 0.28);
  }

  .home-hero__statement h1 span {
    font-weight: 720;
  }

  .home-hero__statement i {
    display: block;
    width: 1.6rem;
    height: 2px;
    margin: 1.45rem auto 0;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.65);
  }

  @media screen and (min-width: 50em) {
    .md-tabs {
      display: block !important;
    }

    .md-header__button[for="__drawer"] {
      display: none !important;
    }

    .md-header > .md-header__inner > label[for="__search"] {
      display: none !important;
    }
  }

  @media screen and (max-width: 49.9375em) {
    .md-tabs {
      display: none;
    }

    .md-header__inner {
      padding: 0 0.7rem;
    }

    .md-header__title {
      font-size: 0.88rem;
    }

    .md-search {
      display: none;
    }

    .home-hero__statement {
      width: min(100% - 32px, 680px);
    }
  }

  @media screen and (max-width: 760px) {
    .home-hero__far,
    .home-hero__near {
      background-position: 61% center;
    }

    .home-hero__statement {
      margin-top: -1vh;
    }

    .home-hero__statement p {
      margin-bottom: 0.75rem;
      font-size: 0.9rem;
      letter-spacing: 0.11em;
    }

    .home-hero__statement h1 {
      font-size: clamp(2.15rem, 10vw, 3.2rem) !important;
      letter-spacing: 0.025em;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .home-hero__far,
    .home-hero__near {
      transform: none;
    }
  }

  /* 首页使用独立导航，避免依赖主题标签栏的宽度断点 */
  .md-tabs {
    display: none !important;
  }

  .home-nav {
    display: none;
  }

  .md-header__inner > .home-nav {
    position: absolute;
    top: 0;
    left: 50%;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.7rem;
    height: 3.2rem;
    transform: translateX(-50%);
    white-space: nowrap;
  }

  .home-nav a {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.7rem;
    font-weight: 430;
    letter-spacing: 0.015em;
    transition: color 180ms ease, opacity 180ms ease;
  }

  .home-nav a:hover,
  .home-nav__active {
    color: #fff !important;
  }

  .md-header > .md-header__inner > label[for="__search"] {
    display: inline-flex !important;
    margin-left: auto;
    color: rgba(255, 255, 255, 0.86);
  }

  .md-search {
    display: none;
  }

  [data-md-toggle="search"]:checked ~ .md-header .md-search {
    display: block;
  }

  @media screen and (min-width: 50em) {
    .md-header__button[for="__drawer"] {
      display: none !important;
    }
  }

  @media screen and (max-width: 49.9375em) {
    .md-header__inner > .home-nav {
      display: none;
    }
  }
</style>

<script>
  (() => {
    const hero = document.querySelector(".home-hero");
    const homeNav = document.querySelector(".home-nav");
    const headerInner = document.querySelector(".md-header__inner");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    if (homeNav && headerInner) headerInner.appendChild(homeNav);

    if (!hero || reduceMotion.matches) return;

    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;
    let frame = 0;

    const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

    const paint = () => {
      currentX += (targetX - currentX) * 0.08;
      currentY += (targetY - currentY) * 0.08;

      hero.style.setProperty("--far-x", `${(-currentX * 4).toFixed(2)}px`);
      hero.style.setProperty("--far-y", `${(-currentY * 3).toFixed(2)}px`);
      hero.style.setProperty("--near-x", `${(currentX * 12).toFixed(2)}px`);
      hero.style.setProperty("--near-y", `${(currentY * 8).toFixed(2)}px`);
      hero.style.setProperty("--light-x", `${(50 + currentX * 6).toFixed(2)}%`);
      hero.style.setProperty("--light-y", `${(45 + currentY * 5).toFixed(2)}%`);

      if (Math.abs(targetX - currentX) > 0.001 || Math.abs(targetY - currentY) > 0.001) {
        frame = requestAnimationFrame(paint);
      } else {
        frame = 0;
      }
    };

    const moveTo = (x, y) => {
      targetX = clamp(x, -1, 1);
      targetY = clamp(y, -1, 1);
      if (!frame) frame = requestAnimationFrame(paint);
    };

    hero.addEventListener("pointermove", (event) => {
      const rect = hero.getBoundingClientRect();
      moveTo(
        ((event.clientX - rect.left) / rect.width - 0.5) * 2,
        ((event.clientY - rect.top) / rect.height - 0.5) * 2
      );
    }, { passive: true });

    hero.addEventListener("pointerleave", () => moveTo(0, 0), { passive: true });

    window.addEventListener("deviceorientation", (event) => {
      if (event.gamma == null || event.beta == null) return;
      moveTo(event.gamma / 22, (event.beta - 45) / 28);
    }, { passive: true });
  })();
</script>
