/**
 * ADK Course learning SPA
 * Routes: #/  #/track/:id  #/module/:id  #/resource/:id  #/resources
 */

const STORAGE_KEY = "adk-course-progress-v1";

const state = {
  course: null,
  progress: loadProgress(),
  route: { name: "home" },
  activeDoc: "readme",
  searchHits: [],
  searchActive: 0,
  searchReturnFocus: null,
  drawerOpen: false,
};

/* —— Progress —— */
function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completed: {} };
    const parsed = JSON.parse(raw);
    return { completed: parsed.completed || {} };
  } catch {
    return { completed: {} };
  }
}

function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.progress));
  updateProgressUI();
  renderSidebar();
}

function isDone(id) {
  return !!state.progress.completed[id];
}

function toggleDone(id) {
  if (state.progress.completed[id]) {
    delete state.progress.completed[id];
  } else {
    state.progress.completed[id] = Date.now();
  }
  saveProgress();
}

function completedCount() {
  if (!state.course) return 0;
  return state.course.modules.filter((m) => isDone(m.id)).length;
}

function updateProgressUI() {
  if (!state.course) return;
  const total = state.course.modules.length;
  const n = completedCount();
  const pct = total ? Math.round((n / total) * 100) : 0;
  const label = document.getElementById("progress-label");
  const fill = document.getElementById("progress-fill");
  const host = document.getElementById("progress-fill-host");
  if (label) label.textContent = `${n} / ${total}`;
  if (fill) fill.style.width = `${pct}%`;
  if (host) {
    host.setAttribute("aria-valuenow", String(n));
    host.setAttribute("aria-valuemax", String(total));
  }
}

/* —— Routing —— */
function parseHash() {
  const hash = location.hash.replace(/^#\/?/, "") || "";
  const parts = hash.split("/").filter(Boolean);
  if (!parts.length) return { name: "home" };
  if (parts[0] === "track" && parts[1]) return { name: "track", id: parts[1] };
  if (parts[0] === "module" && parts[1]) {
    return {
      name: "module",
      id: parts[1],
      doc: parts[2] || "readme",
    };
  }
  if (parts[0] === "resource" && parts[1]) return { name: "resource", id: parts[1] };
  if (parts[0] === "resources") return { name: "resources" };
  return { name: "home" };
}

function navigate(hash) {
  location.hash = hash.startsWith("#") ? hash : `#${hash}`;
}

function setBreadcrumb(parts) {
  const el = document.getElementById("breadcrumb");
  if (!el) return;
  el.innerHTML = parts
    .map((p, i) => {
      if (i === parts.length - 1 || !p.href) {
        return `<span>${esc(p.label)}</span>`;
      }
      return `<button type="button" class="linkish" data-href="${escAttr(p.href)}">${esc(p.label)}</button><span class="sep">/</span>`;
    })
    .join("");
  el.querySelectorAll("[data-href]").forEach((btn) => {
    btn.addEventListener("click", () => navigate(btn.dataset.href));
  });
}

/* —— Markdown —— */
function configureMarked() {
  if (typeof marked === "undefined") return;
  marked.setOptions({
    gfm: true,
    breaks: false,
  });
  marked.use({
    renderer: {
      code({ text, lang }) {
        const language = (lang || "").trim().split(/\s+/)[0] || "";
        let highlighted = esc(text);
        if (typeof hljs !== "undefined") {
          try {
            if (language && hljs.getLanguage(language)) {
              highlighted = hljs.highlight(text, { language }).value;
            } else {
              highlighted = hljs.highlightAuto(text).value;
            }
          } catch {
            highlighted = esc(text);
          }
        }
        const cls = language ? ` class="hljs language-${escAttr(language)}"` : ' class="hljs"';
        return `<pre><code${cls}>${highlighted}</code></pre>\n`;
      },
      link({ href, title, text }) {
        const t = title ? ` title="${escAttr(title)}"` : "";
        const external = href && /^(https?:)?\/\//i.test(href);
        const rel = external ? ' target="_blank" rel="noopener noreferrer"' : "";
        return `<a href="${escAttr(href || "")}"${t}${rel}>${text}</a>`;
      },
    },
  });
}

function renderMarkdown(md) {
  if (typeof marked === "undefined") {
    return `<pre>${esc(md)}</pre>`;
  }
  return marked.parse(md || "");
}

/* —— Utils —— */
function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function escAttr(s) {
  return esc(s).replace(/'/g, "&#39;");
}

function moduleById(id) {
  return state.course?.modules.find((m) => m.id === id || m.slug === id);
}

function trackById(id) {
  return state.course?.tracks.find((t) => t.id === id);
}

function resourceById(id) {
  return state.course?.resources.find((r) => r.id === id);
}

function modulesForTrack(trackId) {
  return state.course.modules.filter((m) => m.track === trackId);
}

function shortId(id) {
  const m = String(id).match(/^(\d+)/);
  if (!m) return id.slice(0, 2);
  return m[1].padStart(2, "0");
}

function lastOpenedModule() {
  const entries = Object.entries(state.progress.completed || {});
  if (!entries.length) {
    return state.course?.modules.find((m) => !isDone(m.id)) || state.course?.modules[0];
  }
  entries.sort((a, b) => b[1] - a[1]);
  const lastDone = moduleById(entries[0][0]);
  if (!lastDone) return state.course?.modules[0];
  const idx = state.course.modules.findIndex((m) => m.id === lastDone.id);
  const next = state.course.modules.slice(idx + 1).find((m) => !isDone(m.id));
  return next || lastDone;
}

/* —— Sidebar —— */
function renderSidebar() {
  const nav = document.getElementById("sidebar-nav");
  if (!nav || !state.course) return;

  const filter = (document.getElementById("search-input")?.value || "").trim().toLowerCase();
  const activeModule = state.route.name === "module" ? state.route.id : null;

  nav.innerHTML = state.course.tracks
    .map((track) => {
      let mods = modulesForTrack(track.id);
      if (filter) {
        mods = mods.filter(
          (m) =>
            m.title.toLowerCase().includes(filter) ||
            m.summary.toLowerCase().includes(filter) ||
            m.id.toLowerCase().includes(filter)
        );
      }
      if (filter && !mods.length) return "";
      return `
        <div class="nav-track" data-track="${escAttr(track.id)}">
          <div class="nav-track-head">${esc(track.title)}</div>
          ${mods
            .map((m) => {
              const done = isDone(m.id);
              const active = activeModule === m.id ? " active" : "";
              return `
                <button type="button" class="nav-item${active}${done ? " done" : ""}" data-module="${escAttr(m.id)}">
                  <span class="nav-num">${esc(shortId(m.id))}</span>
                  <span class="nav-label">${esc(cleanTitle(m.title))}</span>
                  <span class="nav-check" aria-hidden="true">✓</span>
                </button>`;
            })
            .join("")}
        </div>`;
    })
    .join("");

  nav.querySelectorAll("[data-module]").forEach((btn) => {
    btn.addEventListener("click", () => {
      navigate(`#/module/${btn.dataset.module}`);
      if (isMobileNav()) closeSidebar();
    });
  });
}

/**
 * Drawer mode must match CSS (@media max-width: 860px).
 * Also enable drawer if the menu button is actually visible (avoids
 * innerWidth / media-query mismatches where clicks were no-ops).
 */
function isMobileNav() {
  if (typeof window === "undefined") return false;
  const max =
    (window.AdkUiState && window.AdkUiState.MOBILE_MAX) || 860;
  if (window.matchMedia(`(max-width: ${max}px)`).matches) return true;
  const menu = document.getElementById("menu-btn");
  if (menu) {
    try {
      const d = window.getComputedStyle(menu).display;
      if (d && d !== "none") return true;
    } catch {
      /* ignore */
    }
  }
  return false;
}

function drawerEls() {
  return {
    sidebar: document.getElementById("sidebar"),
    backdrop: document.getElementById("sidebar-backdrop"),
    menuBtn: document.getElementById("menu-btn"),
    body: document.body,
  };
}

function syncDrawerDom() {
  const mobile = isMobileNav();
  // Desktop rail: never use off-canvas "open" presentation
  const open = mobile ? !!state.drawerOpen : false;
  if (window.AdkUiState) {
    window.AdkUiState.applyDrawerState(drawerEls(), open, mobile);
  } else {
    const { sidebar, backdrop, menuBtn, body } = drawerEls();
    if (sidebar) {
      sidebar.classList.toggle("open", open);
      sidebar.setAttribute("aria-hidden", mobile ? String(!open) : "false");
    }
    if (body) body.classList.toggle("sidebar-open", open && mobile);
    if (backdrop) {
      backdrop.hidden = !(open && mobile);
      backdrop.setAttribute("aria-hidden", open && mobile ? "false" : "true");
    }
    if (menuBtn) {
      menuBtn.setAttribute("aria-expanded", open && mobile ? "true" : "false");
      menuBtn.setAttribute("aria-label", open && mobile ? "Close menu" : "Open menu");
    }
  }
  // Keep close control interactive when drawer is open
  const closeBtn = document.getElementById("sidebar-close");
  if (closeBtn) {
    closeBtn.tabIndex = open && mobile ? 0 : -1;
  }
}

function openSidebar() {
  state.drawerOpen = true;
  syncDrawerDom();
}

function closeSidebar() {
  state.drawerOpen = false;
  syncDrawerDom();
}

function toggleSidebar() {
  state.drawerOpen = !state.drawerOpen;
  // If we somehow left drawer mode, force closed presentation
  if (!isMobileNav()) state.drawerOpen = false;
  syncDrawerDom();
}

function wireChromeControls() {
  // Capture-phase delegation: survives focus quirks and nested hits
  document.addEventListener(
    "click",
    (e) => {
      const t = e.target;
      if (!(t instanceof Element)) return;
      if (t.closest("#menu-btn")) {
        e.preventDefault();
        e.stopPropagation();
        toggleSidebar();
        return;
      }
      if (t.closest("#sidebar-close")) {
        e.preventDefault();
        e.stopPropagation();
        closeSidebar();
        return;
      }
      if (t.id === "sidebar-backdrop" || t.closest("#sidebar-backdrop")) {
        e.preventDefault();
        closeSidebar();
      }
    },
    true
  );

  // Keyboard: Enter/Space on icon buttons (some UAs need this)
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" && e.key !== " ") return;
    const t = e.target;
    if (!(t instanceof Element)) return;
    if (t.id === "menu-btn" || t.closest("#menu-btn")) {
      e.preventDefault();
      toggleSidebar();
    } else if (t.id === "sidebar-close" || t.closest("#sidebar-close")) {
      e.preventDefault();
      closeSidebar();
    }
  });

  window.matchMedia("(max-width: 860px)").addEventListener("change", (ev) => {
    if (!ev.matches) state.drawerOpen = false;
    syncDrawerDom();
  });
}

/* —— Theme —— */
const THEME_KEY =
  (typeof window !== "undefined" && window.AdkUiState && window.AdkUiState.THEME_KEY) ||
  "adk-course-theme-v1";

function prefersDark() {
  return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function loadThemePreference() {
  try {
    return localStorage.getItem(THEME_KEY) || "system";
  } catch {
    return "system";
  }
}

function saveThemePreference(pref) {
  try {
    localStorage.setItem(THEME_KEY, pref);
  } catch {
    /* ignore */
  }
}

function getThemeState() {
  const stored = loadThemePreference();
  if (window.AdkUiState) {
    return window.AdkUiState.resolveTheme(stored, prefersDark());
  }
  const pref = stored === "light" || stored === "dark" || stored === "system" ? stored : "system";
  const effective = pref === "system" ? (prefersDark() ? "dark" : "light") : pref;
  return { preference: pref, effective };
}

function syncThemeUi() {
  const { preference, effective } = getThemeState();
  if (window.AdkUiState) {
    window.AdkUiState.applyThemeToDocument(document.documentElement, preference, prefersDark());
  } else if (preference === "system") {
    document.documentElement.removeAttribute("data-theme");
  } else {
    document.documentElement.setAttribute("data-theme", effective);
  }

  const btn = document.getElementById("theme-toggle");
  const icon = document.getElementById("theme-icon");
  const label = document.getElementById("theme-label");
  const short =
    preference === "system" ? "Auto" : effective === "dark" ? "Dark" : "Light";
  const full = window.AdkUiState
    ? window.AdkUiState.themeToggleLabel(preference, effective)
    : `Theme: ${short}`;
  if (icon) {
    icon.textContent = window.AdkUiState
      ? window.AdkUiState.themeToggleIcon(effective)
      : effective === "dark"
        ? "☾"
        : "☀";
  }
  if (label) label.textContent = short;
  if (btn) {
    btn.setAttribute("aria-label", full);
    btn.title = full + " — click to cycle";
  }
}

function cycleTheme() {
  const current = getThemeState().preference;
  const next = window.AdkUiState
    ? window.AdkUiState.nextThemePreference(current)
    : current === "light"
      ? "dark"
      : current === "dark"
        ? "system"
        : "light";
  saveThemePreference(next);
  syncThemeUi();
}

function wireThemeControls() {
  syncThemeUi();
  document.getElementById("theme-toggle")?.addEventListener("click", (e) => {
    e.preventDefault();
    cycleTheme();
  });
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (loadThemePreference() === "system" || !loadThemePreference()) {
        syncThemeUi();
      }
    });
  }
}

/* —— Views —— */
function render(opts = {}) {
  const { focusMain = false } = opts;
  state.route = parseHash();
  state.activeDoc = state.route.doc || "readme";
  const main = document.getElementById("main");
  if (!main || !state.course) return;

  updateProgressUI();
  renderSidebar();

  switch (state.route.name) {
    case "track":
      renderTrack(main, state.route.id);
      break;
    case "module":
      renderModule(main, state.route.id);
      break;
    case "resource":
      renderResource(main, state.route.id);
      break;
    case "resources":
      renderResources(main);
      break;
    default:
      renderHome(main);
  }

  if (focusMain) {
    main.focus({ preventScroll: true });
  }
  window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
}

function renderHome(main) {
  const c = state.course;
  const n = completedCount();
  const cont = lastOpenedModule();
  setBreadcrumb([{ label: "Home" }]);

  const continueBlock =
    cont && n > 0
      ? `<p class="continue-line">Continue with <button type="button" class="inline-link" data-module="${escAttr(cont.id)}">${esc(cleanTitle(cont.title))}</button></p>`
      : cont
        ? `<p class="continue-line">Begin with <button type="button" class="inline-link" data-module="${escAttr(cont.id)}">${esc(cleanTitle(cont.title))}</button></p>`
        : "";

  const grouped = c.tracks
    .map((t) => {
      const mods = modulesForTrack(t.id);
      if (!mods.length) return "";
      return `
        <div class="syllabus-group">
          <p class="syllabus-group-label">${esc(t.title)}</p>
          ${mods.map((m) => syllabusItem(m, { hideTrack: true })).join("")}
        </div>`;
    })
    .join("");

  main.innerHTML = `
    <p class="running-head">ADK Course</p>
    <h1 class="page-title">${esc(c.title)}</h1>
    <p class="lede">${esc(c.subtitle)}. Read modules here; run the matching labs from the repository when you are ready.</p>
    <p class="meta-line">
      <span>${c.moduleCount} modules</span>
      <span>${c.tracks.length} tracks</span>
      <span>${esc(c.version)}</span>
      <span>${n} of ${c.moduleCount} complete</span>
    </p>
    ${continueBlock}

    <nav class="track-links" aria-label="Tracks">
      ${c.tracks
        .map((t) => {
          const mods = modulesForTrack(t.id);
          const done = mods.filter((m) => isDone(m.id)).length;
          return `
            <button type="button" class="track-link" data-track="${escAttr(t.id)}">
              <span class="track-name">${esc(t.title)}</span>
              <span class="track-blurb">${esc(t.blurb)}</span>
              <span class="track-count">${done}/${mods.length}</span>
            </button>`;
        })
        .join("")}
    </nav>

    <p class="section-label">Syllabus</p>
    <div class="syllabus">
      ${grouped}
    </div>
    <p class="page-footer">${esc(c.version)} · / to search</p>
  `;

  main.querySelectorAll("[data-track]").forEach((el) => {
    el.addEventListener("click", () => navigate(`#/track/${el.dataset.track}`));
  });
  bindModuleRows(main);
}

function syllabusItem(m, opts = {}) {
  const done = isDone(m.id);
  const hideTrack = opts.hideTrack;
  return `
    <button type="button" class="syllabus-item${done ? " done" : ""}" data-module="${escAttr(m.id)}">
      <span class="syl-num">${esc(shortId(m.id))}</span>
      <span class="syl-body">
        <span class="syl-title">${esc(cleanTitle(m.title))}</span>
        <span class="syl-sum">${esc(m.summary)}</span>
      </span>
      <span class="syl-meta">
        <span>${esc(m.hours)}</span>
        ${done ? `<span class="done-mark">done</span>` : hideTrack ? "" : `<span>${esc(m.track)}</span>`}
      </span>
    </button>`;
}

function cleanTitle(title) {
  return title
    .replace(/^#+\s*/, "")
    .replace(/^\d+[\s.:–—-]+/, "")
    .trim() || title;
}

function bindModuleRows(root) {
  root.querySelectorAll("[data-module]").forEach((el) => {
    el.addEventListener("click", () => navigate(`#/module/${el.dataset.module}`));
  });
}

function renderTrack(main, trackId) {
  const track = trackById(trackId);
  if (!track) {
    main.innerHTML = `<div class="error-box">Unknown track: ${esc(trackId)}</div>`;
    return;
  }
  const mods = modulesForTrack(trackId);
  const done = mods.filter((m) => isDone(m.id)).length;
  setBreadcrumb([
    { label: "Home", href: "#/" },
    { label: track.title },
  ]);

  main.innerHTML = `
    <p class="running-head">${esc(track.title)} track</p>
    <div class="track-intro">
      <h1 class="page-title">${esc(track.title)}</h1>
      <p class="lede">${esc(track.blurb)}</p>
      <p class="meta-line">
        <span>${mods.length} modules</span>
        <span>${done} completed</span>
      </p>
    </div>
    <p class="section-label">Syllabus</p>
    <div class="syllabus">
      ${mods.map((m) => syllabusItem(m)).join("")}
    </div>
  `;
  bindModuleRows(main);
}

function renderModule(main, id) {
  const m = moduleById(id);
  if (!m) {
    main.innerHTML = `<div class="error-box">Module not found: ${esc(id)}</div>`;
    setBreadcrumb([{ label: "Home", href: "#/" }, { label: "Not found" }]);
    return;
  }

  const track = trackById(m.track);
  const done = isDone(m.id);
  const docId = state.activeDoc || "readme";
  let body = m.markdown;

  if (docId !== "readme" && m.extra_docs?.length) {
    const doc = m.extra_docs.find((d) => d.id === docId || d.title === docId);
    if (doc) {
      body = doc.markdown;
    }
  }

  const idx = state.course.modules.findIndex((x) => x.id === m.id);
  const prev = idx > 0 ? state.course.modules[idx - 1] : null;
  const next = idx < state.course.modules.length - 1 ? state.course.modules[idx + 1] : null;

  setBreadcrumb([
    { label: "Home", href: "#/" },
    { label: track?.title || m.track, href: `#/track/${m.track}` },
    { label: cleanTitle(m.title) },
  ]);

  const tabs =
    m.extra_docs?.length > 0
      ? `<div class="doc-tabs" role="tablist" aria-label="Module documents">
          <button type="button" role="tab" class="doc-tab${docId === "readme" ? " active" : ""}" data-doc="readme" aria-selected="${docId === "readme"}">README</button>
          ${m.extra_docs
            .map(
              (d) =>
                `<button type="button" role="tab" class="doc-tab${docId === d.id || docId === d.title ? " active" : ""}" data-doc="${escAttr(d.id)}" aria-selected="${docId === d.id || docId === d.title}">${esc(d.title)}</button>`
            )
            .join("")}
        </div>`
      : "";

  main.innerHTML = `
    <header class="reader-head">
      <p class="reader-meta">
        <span>${esc(m.track)}</span>
        <span>${esc(m.level)}</span>
        <span>${esc(m.hours)}</span>
        <span>${esc(shortId(m.id))}</span>
      </p>
      <h1>${esc(cleanTitle(m.title))}</h1>
      <p class="reader-summary">${esc(m.summary)}</p>
      <div class="reader-actions">
        <button type="button" class="btn btn-primary${done ? " done" : ""}" id="toggle-done" aria-pressed="${done}">
          ${done ? "Completed" : "Mark complete"}
        </button>
        <button type="button" class="btn btn-ghost" id="copy-path">Copy path</button>
      </div>
    </header>
    ${tabs}
    <article class="markdown-body">${renderMarkdown(body)}</article>
    <nav class="reader-nav" aria-label="Adjacent modules">
      ${
        prev
          ? `<button type="button" class="btn" data-nav="${escAttr(prev.id)}"><span>Previous</span><strong>${esc(cleanTitle(prev.title))}</strong></button>`
          : `<span></span>`
      }
      ${
        next
          ? `<button type="button" class="btn" data-nav="${escAttr(next.id)}" style="margin-left:auto;text-align:right"><span>Next</span><strong>${esc(cleanTitle(next.title))}</strong></button>`
          : ""
      }
    </nav>
  `;

  document.getElementById("toggle-done")?.addEventListener("click", () => {
    toggleDone(m.id);
    // Re-render module without stealing focus to <main>
    renderModule(main, id);
    updateProgressUI();
    renderSidebar();
    document.getElementById("toggle-done")?.focus();
  });

  document.getElementById("copy-path")?.addEventListener("click", async () => {
    const btn = document.getElementById("copy-path");
    try {
      await navigator.clipboard.writeText(`modules/${m.id}/`);
      if (btn) {
        btn.textContent = "Copied!";
        setTimeout(() => {
          if (btn) btn.textContent = "Copy path";
        }, 1200);
      }
    } catch {
      /* ignore */
    }
  });

  main.querySelectorAll("[data-doc]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const d = btn.dataset.doc;
      navigate(d === "readme" ? `#/module/${m.id}` : `#/module/${m.id}/${encodeURIComponent(d)}`);
    });
  });

  main.querySelectorAll("[data-nav]").forEach((btn) => {
    btn.addEventListener("click", () => navigate(`#/module/${btn.dataset.nav}`));
  });
}

function renderResources(main) {
  setBreadcrumb([{ label: "Home", href: "#/" }, { label: "Resources" }]);
  main.innerHTML = `
    <p class="running-head">Reference</p>
    <h1 class="page-title">Resources</h1>
    <p class="lede">Glossary, cheatsheet, curriculum, coverage matrix, and progress tracker.</p>
    <div class="resource-list">
      ${state.course.resources
        .map(
          (r) => `
        <button type="button" class="resource-row" data-resource="${escAttr(r.id)}">
          <span class="kind">${esc(r.kind)}</span>
          <span class="resource-title">${esc(cleanTitle(r.title))}</span>
        </button>`
        )
        .join("")}
    </div>
  `;
  main.querySelectorAll("[data-resource]").forEach((btn) => {
    btn.addEventListener("click", () => navigate(`#/resource/${btn.dataset.resource}`));
  });
}

function renderResource(main, id) {
  const r = resourceById(id);
  if (!r) {
    main.innerHTML = `<div class="error-box">Resource not found: ${esc(id)}</div>`;
    return;
  }
  setBreadcrumb([
    { label: "Home", href: "#/" },
    { label: "Resources", href: "#/resources" },
    { label: cleanTitle(r.title) },
  ]);
  main.innerHTML = `
    <header class="reader-head">
      <p class="reader-meta">
        <span>${esc(r.kind)}</span>
        <span>${esc(r.path)}</span>
      </p>
      <h1>${esc(cleanTitle(r.title))}</h1>
    </header>
    <article class="markdown-body">${renderMarkdown(r.markdown)}</article>
  `;
}

/* —— Search —— */
function openSearch() {
  const overlay = document.getElementById("search-overlay");
  const input = document.getElementById("search-modal-input");
  const panel = document.getElementById("search-panel");
  if (!overlay || !input) return;
  state.searchReturnFocus = document.activeElement;
  overlay.hidden = false;
  overlay.setAttribute("aria-hidden", "false");
  document.body.classList.add("search-open");
  if (panel) panel.setAttribute("aria-modal", "true");
  input.value = document.getElementById("search-input")?.value || "";
  // Defer focus so overlay is painted
  requestAnimationFrame(() => input.focus());
  runSearch(input.value);
}

function closeSearch() {
  const overlay = document.getElementById("search-overlay");
  const panel = document.getElementById("search-panel");
  if (overlay) {
    overlay.hidden = true;
    overlay.setAttribute("aria-hidden", "true");
  }
  document.body.classList.remove("search-open");
  if (panel) panel.setAttribute("aria-modal", "false");
  const back = state.searchReturnFocus;
  state.searchReturnFocus = null;
  if (back && typeof back.focus === "function") {
    try {
      back.focus();
    } catch {
      /* ignore */
    }
  }
}

function runSearch(q) {
  const results = document.getElementById("search-results");
  if (!results || !state.course) return;
  const query = q.trim().toLowerCase();
  if (!query) {
    results.innerHTML = `<p class="empty-state">Type to search modules and resources</p>`;
    state.searchHits = [];
    return;
  }

  const hits = [];
  for (const m of state.course.modules) {
    const hay = `${m.title} ${m.summary} ${m.id} ${m.level} ${m.markdown.slice(0, 4000)}`.toLowerCase();
    if (!hay.includes(query)) continue;
    const snip = snippet(m.markdown, query) || m.summary;
    hits.push({
      kind: "module",
      id: m.id,
      title: cleanTitle(m.title),
      meta: `${m.track} · ${m.level}`,
      snip,
      href: `#/module/${m.id}`,
    });
  }
  for (const r of state.course.resources) {
    const hay = `${r.title} ${r.markdown.slice(0, 4000)}`.toLowerCase();
    if (!hay.includes(query)) continue;
    hits.push({
      kind: "resource",
      id: r.id,
      title: cleanTitle(r.title),
      meta: r.kind,
      snip: snippet(r.markdown, query) || "",
      href: `#/resource/${r.id}`,
    });
  }

  state.searchHits = hits.slice(0, 40);
  state.searchActive = 0;

  if (!state.searchHits.length) {
    results.innerHTML = `<p class="empty-state">No matches for “${esc(q)}”</p>`;
    return;
  }

  results.innerHTML = state.searchHits
    .map(
      (h, i) => `
    <button type="button" class="search-hit${i === 0 ? " active" : ""}" data-href="${escAttr(h.href)}" data-idx="${i}">
      <div class="hit-title">${esc(h.title)}</div>
      <div class="hit-meta">${esc(h.meta)} · ${esc(h.kind)}</div>
      ${h.snip ? `<div class="hit-snip">${esc(h.snip)}</div>` : ""}
    </button>`
    )
    .join("");

  results.querySelectorAll("[data-href]").forEach((btn) => {
    btn.addEventListener("click", () => {
      navigate(btn.dataset.href);
      closeSearch();
    });
  });
}

function snippet(text, query) {
  const plain = text.replace(/[#*`\[\]()>_|-]/g, " ").replace(/\s+/g, " ");
  const lower = plain.toLowerCase();
  const i = lower.indexOf(query);
  if (i < 0) return "";
  const start = Math.max(0, i - 40);
  const end = Math.min(plain.length, i + query.length + 60);
  let s = plain.slice(start, end).trim();
  if (start > 0) s = "…" + s;
  if (end < plain.length) s = s + "…";
  return s;
}

function highlightSearchHit() {
  document.querySelectorAll(".search-hit").forEach((el, i) => {
    el.classList.toggle("active", i === state.searchActive);
    if (i === state.searchActive) el.scrollIntoView({ block: "nearest" });
  });
}

/* —— Bootstrap —— */
async function init() {
  // Wire shell controls first so menu/close work even if content fails to load
  wireChromeControls();
  wireThemeControls();
  syncDrawerDom();
  document.getElementById("open-search")?.addEventListener("click", openSearch);

  const onScroll = () => {
    document.querySelector(".topbar")?.classList.toggle("scrolled", window.scrollY > 8);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  document.querySelectorAll("[data-route]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const r = btn.dataset.route;
      if (r === "home") navigate("#/");
      if (r === "resources") navigate("#/resources");
      if (isMobileNav()) closeSidebar();
    });
  });

  document.getElementById("reset-progress")?.addEventListener("click", () => {
    if (confirm("Clear all local progress for this course?")) {
      state.progress = { completed: {} };
      saveProgress();
      render();
    }
  });

  const sideSearch = document.getElementById("search-input");
  sideSearch?.addEventListener("input", () => {
    if (state.course) renderSidebar();
  });
  sideSearch?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      openSearch();
      const modal = document.getElementById("search-modal-input");
      if (modal) {
        modal.value = sideSearch.value;
        runSearch(modal.value);
      }
    }
  });

  const modalInput = document.getElementById("search-modal-input");
  modalInput?.addEventListener("input", () => runSearch(modalInput.value));
  modalInput?.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      e.preventDefault();
      closeSearch();
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      state.searchActive = Math.min(state.searchActive + 1, state.searchHits.length - 1);
      highlightSearchHit();
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      state.searchActive = Math.max(state.searchActive - 1, 0);
      highlightSearchHit();
    }
    if (e.key === "Enter" && state.searchHits[state.searchActive]) {
      e.preventDefault();
      navigate(state.searchHits[state.searchActive].href);
      closeSearch();
    }
  });

  document.getElementById("search-overlay")?.addEventListener("click", (e) => {
    if (e.target.id === "search-overlay") closeSearch();
  });

  document.addEventListener("keydown", (e) => {
    const tag = (e.target && e.target.tagName) || "";
    const typing = tag === "INPUT" || tag === "TEXTAREA" || e.target?.isContentEditable;
    const searchOpen = !document.getElementById("search-overlay")?.hidden;

    if (e.key === "/" && !typing && !e.metaKey && !e.ctrlKey && !searchOpen) {
      e.preventDefault();
      openSearch();
    }
    if (e.key === "Escape") {
      if (searchOpen) {
        e.preventDefault();
        closeSearch();
        return;
      }
      if (isMobileNav() && state.drawerOpen) {
        e.preventDefault();
        closeSidebar();
      }
    }
  });

  window.addEventListener("hashchange", () => {
    render({ focusMain: false });
    if (isMobileNav()) closeSidebar();
  });

  // Initial mobile state: drawer closed
  state.drawerOpen = false;
  syncDrawerDom();

  configureMarked();
  const main = document.getElementById("main");
  main.innerHTML = `<div class="loading">Loading course…</div>`;

  try {
    const res = await fetch("course-data.json", { cache: "no-cache" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.course = await res.json();
    if (window.AdkUiState) {
      const check = window.AdkUiState.validateCourseData(state.course);
      if (!check.ok) {
        console.warn("course-data shape warnings:", check.errors);
      }
    }
  } catch (err) {
    main.innerHTML = `
      <div class="error-box">
        <strong>Could not load course-data.json</strong>
        <p>${esc(err.message)}</p>
        <p>Run <code>python scripts/build_content.py</code> from the webapp folder, then serve <code>public/</code>.</p>
      </div>`;
    return;
  }

  document.title = state.course.title;
  updateProgressUI();
  render({ focusMain: true });
}

init();
