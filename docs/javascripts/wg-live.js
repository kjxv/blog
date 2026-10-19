(function () {
  "use strict";
  const defaults = { relay_ip: "", exit_ip: "", relay_ssh_port: "22", exit_ssh_port: "22", wg_port: "51830", node_port: "443" };
  const labels = { relay_ip: "中转 VPS 公网 IP", exit_ip: "英国出口 VPS 公网 IP", relay_ssh_port: "中转 SSH 端口", exit_ssh_port: "英国 SSH 端口", wg_port: "WireGuard UDP 端口", node_port: "节点 TCP 端口" };
  const storageKey = "wg-live-20261014-v1";
  function ipv4(value) {
    const parts = value.split(".");
    return parts.length === 4 && parts.every(p => /^(0|[1-9]\d{0,2})$/.test(p) && Number(p) <= 255) && !["0", "127"].includes(parts[0]) && Number(parts[0]) < 224;
  }
  function validate(raw) {
    const values = {}, errors = {};
    Object.keys(defaults).forEach(key => {
      const value = String(raw[key] == null ? defaults[key] : raw[key]).trim();
      if (key.endsWith("_ip")) {
        values[key] = value;
        if (!ipv4(value)) errors[key] = "请填写有效的 " + labels[key];
      } else {
        values[key] = value;
        if (!/^\d{1,5}$/.test(value) || Number(value) < 1 || Number(value) > 65535) errors[key] = labels[key] + "应在 1–65535 之间";
        else values[key] = String(Number(value));
      }
    });
    if (values.relay_ip && values.relay_ip === values.exit_ip) errors.exit_ip = "两台 VPS 不能使用同一个 IP";
    if (values.node_port === values.relay_ssh_port) errors.node_port = "节点端口不能与中转 SSH 端口相同";
    return { values, errors, valid: Object.keys(errors).length === 0 };
  }
  function quote(value) { return "'" + String(value).replace(/'/g, "'\\''") + "'"; }
  function materialize(file, manifest, sources, action) {
    const digest = manifest.files[file];
    if (!/^[a-f0-9]{64}$/.test(digest || "")) throw new Error("脚本校验信息不完整");
    const source = sources[file];
    if (typeof source !== "string" || !source.startsWith("#!/usr/bin/env python3\n") || !source.endsWith("\n") || source.includes("\r")) throw new Error("部署脚本加载不完整，请刷新页面。");
    const delimiter = "WG_LIVE_SCRIPT_20261014_END";
    if (source.split("\n").includes(delimiter)) throw new Error("部署脚本包含冲突的结束标记");
    const target = "/root/wg-live/" + file;
    return ["(", "  set -e", "  umask 077", "  if ! command -v curl >/dev/null || ! command -v python3 >/dev/null; then", "    apt-get update", "    DEBIAN_FRONTEND=noninteractive apt-get install -y curl python3", "  fi", "  install -d -m 700 /root/wg-live", "  cat > " + quote(target) + " <<'" + delimiter + "'", source + delimiter, "  printf '%s\\n' " + quote(digest + "  " + target) + " | sha256sum -c -", "  " + action, ")"].join("\n");
  }
  function commands(raw, manifest, sources) {
    const checked = validate(raw);
    if (!checked.valid) throw new Error(Object.values(checked.errors)[0]);
    const p = checked.values;
    const flags = Object.keys(defaults).map(k => "--" + k.replace(/_/g, "-") + " " + quote(p[k])).join(" ");
    return {
      login_relay: "ssh -p " + p.relay_ssh_port + " root@" + p.relay_ip,
      login_exit: "ssh -p " + p.exit_ssh_port + " root@" + p.exit_ip,
      exit: materialize("deploy.py", manifest, sources, "python3 /root/wg-live/deploy.py exit " + flags),
      relay: materialize("deploy.py", manifest, sources, "python3 /root/wg-live/deploy.py relay " + flags),
      repair_exit: materialize("deploy.py", manifest, sources, "python3 /root/wg-live/deploy.py repair-addresses " + flags),
      repair_relay: materialize("deploy.py", manifest, sources, "python3 /root/wg-live/deploy.py repair-addresses " + flags),
      check: "ping -c 3 -W 3 10.77.0.1\nwg show wg-uk\ncurl -4 --interface 10.77.0.2 -fsS --max-time 20 https://api.ipify.org\nprintf '\\n'",
      install_panel: "(\n  set -e\n  curl -fsSL https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh -o /root/3x-ui-install.sh\n  bash /root/3x-ui-install.sh\n)",
      panel: materialize("connect-panel.py", manifest, sources, "python3 /root/wg-live/connect-panel.py --node-port " + quote(p.node_port)),
      listeners: "systemctl is-active x-ui wg-quick@wg-uk wg-live-policy\nss -lntp 'sport = :" + p.node_port + "'\nip route show table 51830",
      client_check: "curl https://api.ipify.org\ncurl https://www.cloudflare.com/cdn-cgi/trace",
      pause: "systemctl stop wg-quick@wg-uk",
      resume: "systemctl start wg-quick@wg-uk",
      status_relay: "wg show wg-uk\nsystemctl status wg-quick@wg-uk wg-live-policy x-ui --no-pager\njournalctl -u wg-quick@wg-uk -u x-ui -n 60 --no-pager",
      status_exit: "wg show wg-relay\nsystemctl status wg-quick@wg-relay wg-live-egress --no-pager\nsysctl net.ipv4.ip_forward",
      restore: "python3 /root/wg-live/connect-panel.py --restore",
      mtu: "ping -c 3 -W 2 -M do -s 1352 10.77.0.1",
      iperf_exit: "DEBIAN_FRONTEND=noninteractive apt-get install -y iperf3\niperf3 -s -B 10.77.0.1 -p 5202",
      iperf_relay: "DEBIAN_FRONTEND=noninteractive apt-get install -y iperf3\niperf3 -c 10.77.0.1 -p 5202 -B 10.77.0.2 -t 15\niperf3 -c 10.77.0.1 -p 5202 -B 10.77.0.2 -t 15 -R\niperf3 -c 10.77.0.1 -p 5202 -B 10.77.0.2 -u -b 12M -l 1200 -t 15"
    };
  }
  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return; }
    const field = document.createElement("textarea"); field.value = text; field.style.position = "fixed"; field.style.opacity = "0";
    document.body.appendChild(field); field.select();
    const ok = document.execCommand("copy"); field.remove();
    if (!ok) throw new Error("请选中代码手动复制");
  }
  function init() {
    const form = document.getElementById("wg-live-config");
    if (!form || form.dataset.initialized) return;
    form.dataset.initialized = "true";
    const status = form.querySelector("[data-wg-status]");
    const fields = {};
    Object.keys(defaults).forEach(key => { fields[key] = form.querySelector('[name="' + key + '"]'); });
    let manifest = null, sources = null, manifestError = "", generated = {};
    const cards = Array.from(document.querySelectorAll(".wg-command[data-wg-command]"));
    function update() {
      const raw = {}; Object.keys(fields).forEach(k => { raw[k] = fields[k].value; });
      const checked = validate(raw);
      Object.keys(fields).forEach(k => { fields[k].setAttribute("aria-invalid", String(!!checked.errors[k])); });
      document.querySelectorAll("[data-wg-value]").forEach(el => {
        const k = el.dataset.wgValue; el.textContent = checked.values[k] || "（填写后显示）";
      });
      generated = {};
      if (checked.valid && manifest && sources) generated = commands(checked.values, manifest, sources);
      cards.forEach(card => {
        const text = generated[card.dataset.wgCommand];
        card.querySelector("code").textContent = text || "先在页面顶部填写两台 VPS 的 IP，命令会自动生成。";
        card.querySelector("button").disabled = !text;
        card.querySelector("[data-wg-copy-status]").textContent = "";
        card.querySelector("button").textContent = "复制命令";
      });
      status.classList.toggle("is-ready", checked.valid && !!manifest && !!sources);
      if (manifestError) status.textContent = manifestError;
      else if (!checked.valid) status.textContent = Object.values(checked.errors)[0] + "；填写完成后，下面所有命令会同步更新。";
      else if (!manifest || !sources) status.textContent = "正在加载完整部署脚本…";
      else status.textContent = "参数已就绪。命令已包含完整脚本，请从英国 VPS 开始，按顺序整段复制。";
      try { sessionStorage.setItem(storageKey, JSON.stringify(raw)); } catch (_) {}
    }
    try {
      const remembered = JSON.parse(sessionStorage.getItem(storageKey) || "null");
      if (remembered) Object.keys(fields).forEach(k => { if (remembered[k] != null) fields[k].value = String(remembered[k]); });
    } catch (_) {}
    form.addEventListener("input", update);
    form.addEventListener("submit", event => event.preventDefault());
    form.querySelector("[data-wg-reset]").addEventListener("click", () => { Object.keys(fields).forEach(k => { fields[k].value = defaults[k]; }); update(); });
    cards.forEach(card => {
      const button = card.querySelector("button");
      button.addEventListener("click", async () => {
        const text = generated[card.dataset.wgCommand]; if (!text) return;
        const message = card.querySelector("[data-wg-copy-status]");
        try { await copyText(text); message.textContent = "已复制，请粘贴到“" + card.dataset.wgTarget + "”窗口。"; button.textContent = "已复制"; }
        catch (error) { message.textContent = error.message; }
        setTimeout(() => { button.textContent = "复制命令"; }, 1800);
      });
    });
    if (/^(localhost|127\.0\.0\.1|0\.0\.0\.0)$/.test(location.hostname)) {
      const note = form.querySelector("[data-wg-local-note]"); note.hidden = false;
    }
    update();
    fetch(form.dataset.manifest, { cache: "no-store" }).then(response => {
      if (!response.ok) throw new Error("脚本版本文件加载失败，请检查网站是否完整发布。");
      return response.json();
    }).then(async data => {
      if (data.version !== "20261014-v1" || !data.files) throw new Error("部署脚本版本不匹配，请刷新页面。");
      ["deploy.py", "connect-panel.py"].forEach(f => { if (!/^[a-f0-9]{64}$/.test(data.files[f] || "")) throw new Error("脚本校验信息不完整。"); });
      const loaded = {};
      await Promise.all(["deploy.py", "connect-panel.py"].map(async file => {
        const response = await fetch(new URL(file, new URL(form.dataset.manifest, location.href)), { cache: "no-store" });
        if (!response.ok) throw new Error("完整脚本加载失败（" + response.status + "），请检查网站文件并刷新页面；暂时不能复制部署命令。");
        loaded[file] = await response.text();
      }));
      // Validate every full command before enabling any copy button.
      commands({ ...defaults, relay_ip: "198.51.100.10", exit_ip: "203.0.113.20" }, data, loaded);
      manifest = data; sources = loaded; update();
    }).catch(error => { manifestError = error.message; update(); });
  }
  const api = { defaults, validate, commands, quote };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof window !== "undefined") window.WGLiveConfig = api;
  if (typeof document !== "undefined") {
    if (typeof document$ !== "undefined") document$.subscribe(init);
    else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
  }
})();
