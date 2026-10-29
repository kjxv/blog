(function () {
  "use strict";

  const STORAGE_KEY = "blog.postsPerPage";
  const ALLOWED_SIZES = [10, 15, 20];
  const STATIC_PAGE_SIZE = 10;

  function normalizeUrlAttributes(root, pageUrl) {
    root.querySelectorAll("[href]").forEach(function (element) {
      const value = element.getAttribute("href");
      if (!value || value.startsWith("#") || value.startsWith("javascript:")) return;
      try {
        element.setAttribute("href", new URL(value, pageUrl).href);
      } catch (_) {}
    });

    root.querySelectorAll("[src]").forEach(function (element) {
      const value = element.getAttribute("src");
      if (!value || value.startsWith("data:")) return;
      try {
        element.setAttribute("src", new URL(value, pageUrl).href);
      } catch (_) {}
    });

    root.querySelectorAll("[srcset]").forEach(function (element) {
      const value = element.getAttribute("srcset");
      if (!value) return;
      const normalized = value.split(",").map(function (candidate) {
        const parts = candidate.trim().split(/\s+/);
        try {
          parts[0] = new URL(parts[0], pageUrl).href;
        } catch (_) {}
        return parts.join(" ");
      }).join(", ");
      element.setAttribute("srcset", normalized);
    });
  }

  function pageNumberFromUrl(url) {
    try {
      const match = new URL(url, window.location.href).pathname.match(/\/page\/(\d+)\/?$/);
      return match ? Number(match[1]) : 1;
    } catch (_) {
      return 1;
    }
  }

  function getBasePath() {
    const pathname = window.location.pathname;
    const stripped = pathname.replace(/\/page\/\d+\/?$/, "/");
    return stripped.endsWith("/") ? stripped : stripped + "/";
  }

  function getStaticPageCount(nativePagination) {
    if (!nativePagination) return 1;
    let maximum = pageNumberFromUrl(window.location.href);
    nativePagination.querySelectorAll("a[href]").forEach(function (link) {
      maximum = Math.max(maximum, pageNumberFromUrl(link.href));
    });
    return maximum;
  }

  function getStoredPageSize() {
    const stored = Number(window.localStorage.getItem(STORAGE_KEY));
    return ALLOWED_SIZES.includes(stored) ? stored : 10;
  }

  function cloneCurrentPosts(posts) {
    return posts.map(function (post) {
      const clone = post.cloneNode(true);
      normalizeUrlAttributes(clone, window.location.href);
      return clone;
    });
  }

  async function loadStaticPage(pageNumber, currentPage, currentPosts, basePath) {
    if (pageNumber === currentPage) return cloneCurrentPosts(currentPosts);

    const path = pageNumber === 1 ? basePath : basePath + "page/" + pageNumber + "/";
    const pageUrl = new URL(path, window.location.origin);
    const response = await fetch(pageUrl.href, { credentials: "same-origin" });
    if (!response.ok) throw new Error("Unable to load blog page " + pageNumber);

    const html = await response.text();
    const parsed = new DOMParser().parseFromString(html, "text/html");
    return Array.from(parsed.querySelectorAll(".md-post--excerpt")).map(function (post) {
      normalizeUrlAttributes(post, pageUrl.href);
      return post;
    });
  }

  function paginationItems(current, total) {
    if (total <= 7) return Array.from({ length: total }, function (_, index) { return index + 1; });

    const values = new Set([1, total, current - 1, current, current + 1]);
    const pages = Array.from(values).filter(function (page) {
      return page >= 1 && page <= total;
    }).sort(function (a, b) { return a - b; });

    const result = [];
    pages.forEach(function (page, index) {
      if (index && page - pages[index - 1] > 1) result.push("dots-" + page);
      result.push(page);
    });
    return result;
  }

  async function enhanceBlogPagination() {
    const content = document.querySelector(".md-content[data-md-component='content']");
    if (!content || content.dataset.blogPaginationEnhanced === "true") return;

    const currentPosts = Array.from(content.querySelectorAll(".md-post--excerpt"));
    if (!currentPosts.length) return;

    const nativePagination = content.querySelector(".md-pagination");
    const totalStaticPages = getStaticPageCount(nativePagination);
    if (totalStaticPages === 1 && currentPosts.length <= 10) return;

    content.dataset.blogPaginationEnhanced = "true";

    const currentStaticPage = pageNumberFromUrl(window.location.href);
    const basePath = getBasePath();

    try {
      const groups = await Promise.all(
        Array.from({ length: totalStaticPages }, function (_, index) {
          return loadStaticPage(index + 1, currentStaticPage, currentPosts, basePath);
        })
      );
      const allPosts = groups.flat();
      if (!allPosts.length) throw new Error("No blog posts found");

      const firstPost = currentPosts[0];
      const parent = firstPost.parentNode;
      const list = document.createElement("div");
      list.className = "blog-post-list";
      list.setAttribute("aria-live", "polite");
      parent.insertBefore(list, firstPost);
      currentPosts.forEach(function (post) { post.remove(); });

      const tools = document.createElement("div");
      tools.className = "blog-list-tools";
      tools.innerHTML = [
        '<label class="blog-page-size">',
        '<span>每页显示</span>',
        '<select aria-label="每页显示的文章数量">',
        ALLOWED_SIZES.map(function (size) { return '<option value="' + size + '">' + size + '</option>'; }).join(""),
        '</select>',
        '<span>篇，共 ' + allPosts.length + ' 篇</span>',
        '</label>',
        '<nav class="blog-client-pagination" aria-label="博客分页"></nav>'
      ].join("");

      if (nativePagination) {
        nativePagination.insertAdjacentElement("beforebegin", tools);
        nativePagination.hidden = true;
        nativePagination.style.display = "none";
      } else {
        parent.appendChild(tools);
      }

      const select = tools.querySelector("select");
      const pageNav = tools.querySelector(".blog-client-pagination");
      let pageSize = getStoredPageSize();
      const requestedPage = Number(new URL(window.location.href).searchParams.get("list_page"));
      const firstVisiblePost = (currentStaticPage - 1) * STATIC_PAGE_SIZE;
      let currentPage = requestedPage > 0
        ? requestedPage
        : Math.floor(firstVisiblePost / pageSize) + 1;
      select.value = String(pageSize);

      function updateAddress() {
        const url = new URL(window.location.href);
        url.pathname = basePath;
        if (currentPage > 1) url.searchParams.set("list_page", String(currentPage));
        else url.searchParams.delete("list_page");
        if (pageSize !== 10) url.searchParams.set("per_page", String(pageSize));
        else url.searchParams.delete("per_page");
        window.history.replaceState(null, "", url.pathname + url.search + url.hash);
      }

      function render(scrollToList) {
        const pageCount = Math.max(1, Math.ceil(allPosts.length / pageSize));
        currentPage = Math.min(Math.max(currentPage, 1), pageCount);
        const start = (currentPage - 1) * pageSize;
        const fragment = document.createDocumentFragment();
        allPosts.slice(start, start + pageSize).forEach(function (post) {
          fragment.appendChild(post.cloneNode(true));
        });
        list.replaceChildren(fragment);

        pageNav.replaceChildren();
        const addButton = function (label, page, options) {
          const button = document.createElement("button");
          button.type = "button";
          button.textContent = label;
          button.setAttribute("aria-label", options.label || ("第 " + page + " 页"));
          if (options.current) button.setAttribute("aria-current", "page");
          button.disabled = Boolean(options.disabled);
          button.addEventListener("click", function () {
            currentPage = page;
            render(true);
          });
          pageNav.appendChild(button);
        };

        addButton("‹", currentPage - 1, { label: "上一页", disabled: currentPage === 1 });
        paginationItems(currentPage, pageCount).forEach(function (item) {
          if (typeof item === "string") {
            const dots = document.createElement("span");
            dots.className = "blog-client-pagination__dots";
            dots.textContent = "…";
            pageNav.appendChild(dots);
          } else {
            addButton(String(item), item, { current: item === currentPage });
          }
        });
        addButton("›", currentPage + 1, { label: "下一页", disabled: currentPage === pageCount });
        updateAddress();

        if (scrollToList) {
          const offset = list.getBoundingClientRect().top + window.scrollY - 76;
          window.scrollTo({ top: Math.max(0, offset), behavior: "smooth" });
        }
      }

      select.addEventListener("change", function () {
        pageSize = Number(select.value);
        window.localStorage.setItem(STORAGE_KEY, String(pageSize));
        currentPage = 1;
        render(false);
      });

      render(false);
    } catch (error) {
      content.dataset.blogPaginationEnhanced = "false";
      console.warn("博客分页增强功能加载失败，已保留静态分页。", error);
    }
  }

  if (typeof window.document$ !== "undefined") {
    window.document$.subscribe(enhanceBlogPagination);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enhanceBlogPagination, { once: true });
  } else {
    enhanceBlogPagination();
  }
})();
