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
  if (label) label.textContent = `${n} / ${total}`;
  if (fill) fill.style.width = `${pct}%`;
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
  return m ? m[1] : id.slice(0, 2);
}

function trackColor(trackId) {
  return trackById(trackId)?.color || "#2dd4bf";
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
          <div class="nav-track-head">
            <span class="nav-track-dot"></span>
            ${esc(track.title)}
          </div>
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
      closeSidebar();
    });
  });
}

function openSidebar() {
  document.getElementById("sidebar")?.classList.add("open");
}

function closeSidebar() {
  document.getElementById("sidebar")?.classList.remove("open");
}

/* —— Views —— */
function render() {
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

  main.focus({ preventScroll: true });
  window.scrollTo({ top: 0, behavior: "instant" in window ? "instant" : "auto" });
}

function renderHome(main) {
  const c = state.course;
  const n = completedCount();
  setBreadcrumb([{ label: "Home" }]);

  main.innerHTML = `
    <section class="hero">
      <p class="hero-kicker">Course reader</p>
      <h1>${esc(c.title)}</h1>
      <p>${esc(c.subtitle)}</p>
      <div class="hero-stats">
        <span class="stat-chip"><strong>${c.moduleCount}</strong> modules</span>
        <span class="stat-chip"><strong>${c.tracks.length}</strong> tracks</span>
        <span class="stat-chip"><strong>${esc(c.version)}</strong></span>
        <span class="stat-chip"><strong>${n}</strong> completed</span>
      </div>
    </section>

    <div class="section-head">
      <h2>Tracks</h2>
      <span>Choose a path</span>
    </div>
    <div class="track-grid">
      ${c.tracks
        .map((t) => {
          const mods = modulesForTrack(t.id);
          const done = mods.filter((m) => isDone(m.id)).length;
          return `
            <button type="button" class="track-card" data-track="${escAttr(t.id)}" style="--track-color:${escAttr(t.color)}">
              <div class="track-dot"></div>
              <h3>${esc(t.title)}</h3>
              <p>${esc(t.blurb)}</p>
              <div class="track-meta">${done} / ${mods.length} done</div>
            </button>`;
        })
        .join("")}
    </div>

    <div class="section-head">
      <h2>All modules</h2>
      <span>${c.moduleCount}</span>
    </div>
    <div class="module-list">
      ${c.modules.map((m) => moduleRow(m)).join("")}
    </div>
  `;

  main.querySelectorAll("[data-track]").forEach((el) => {
    el.addEventListener("click", () => navigate(`#/track/${el.dataset.track}`));
  });
  bindModuleRows(main);
}

function moduleRow(m) {
  const done = isDone(m.id);
  return `
    <button type="button" class="module-row${done ? " done" : ""}" data-module="${escAttr(m.id)}">
      <span class="mod-id">${esc(shortId(m.id))}</span>
      <div class="mod-body">
        <h3>${esc(cleanTitle(m.title))}</h3>
        <p>${esc(m.summary)}</p>
      </div>
      <div class="mod-side">
        <div class="mod-tags">
          <span class="tag track-${escAttr(m.track)}">${esc(m.track)}</span>
          <span class="tag level">${esc(m.level)}</span>
          <span class="tag hours">${esc(m.hours)}</span>
        </div>
        <span class="mod-done" aria-hidden="true">✓</span>
      </div>
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
    <section class="hero" style="--track-color:${escAttr(track.color)}">
      <p class="hero-kicker" style="color:${escAttr(track.color)}">${esc(track.title)} track</p>
      <h1>${esc(track.title)}</h1>
      <p>${esc(track.blurb)}</p>
      <div class="hero-stats">
        <span class="stat-chip"><strong>${mods.length}</strong> modules</span>
        <span class="stat-chip"><strong>${done}</strong> completed</span>
      </div>
    </section>
    <div class="module-list">
      ${mods.map((m) => moduleRow(m)).join("")}
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
  let docTitle = "README";

  if (docId !== "readme" && m.extra_docs?.length) {
    const doc = m.extra_docs.find((d) => d.id === docId || d.title === docId);
    if (doc) {
      body = doc.markdown;
      docTitle = doc.title;
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
      ? `<div class="doc-tabs">
          <button type="button" class="doc-tab${docId === "readme" ? " active" : ""}" data-doc="readme">README</button>
          ${m.extra_docs
            .map(
              (d) =>
                `<button type="button" class="doc-tab${docId === d.id || docId === d.title ? " active" : ""}" data-doc="${escAttr(d.id)}">${esc(d.title)}</button>`
            )
            .join("")}
        </div>`
      : "";

  main.innerHTML = `
    <header class="reader-head">
      <div class="reader-meta">
        <span class="tag track-${escAttr(m.track)}">${esc(m.track)}</span>
        <span class="tag level">${esc(m.level)}</span>
        <span class="tag hours">${esc(m.hours)}</span>
      </div>
      <h1>${esc(cleanTitle(m.title))}</h1>
      <p class="reader-summary">${esc(m.summary)}</p>
      <div class="reader-actions">
        <button type="button" class="btn btn-primary${done ? " done" : ""}" id="toggle-done">
          ${done ? "✓ Completed" : "Mark complete"}
        </button>
        <button type="button" class="btn" id="copy-path">Copy path</button>
      </div>
    </header>
    ${tabs}
    <article class="markdown-body">${renderMarkdown(body)}</article>
    <nav class="reader-nav">
      ${
        prev
          ? `<button type="button" class="btn" data-nav="${escAttr(prev.id)}"><span>← Previous</span><strong>${esc(cleanTitle(prev.title))}</strong></button>`
          : `<span></span>`
      }
      ${
        next
          ? `<button type="button" class="btn" data-nav="${escAttr(next.id)}" style="margin-left:auto;text-align:right"><span>Next →</span><strong>${esc(cleanTitle(next.title))}</strong></button>`
          : ""
      }
    </nav>
  `;

  document.getElementById("toggle-done")?.addEventListener("click", () => {
    toggleDone(m.id);
    renderModule(main, id);
  });

  document.getElementById("copy-path")?.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(`modules/${m.id}/`);
      const btn = document.getElementById("copy-path");
      if (btn) {
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = "Copy path"), 1200);
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
    <section class="hero">
      <p class="hero-kicker">Reference</p>
      <h1>Resources</h1>
      <p>Glossary, cheatsheet, curriculum, coverage matrix, and progress tracker.</p>
    </section>
    <div class="resource-grid">
      ${state.course.resources
        .map(
          (r) => `
        <button type="button" class="resource-card" data-resource="${escAttr(r.id)}">
          <div class="kind">${esc(r.kind)}</div>
          <h3>${esc(cleanTitle(r.title))}</h3>
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
      <div class="reader-meta">
        <span class="tag level">${esc(r.kind)}</span>
        <span class="tag level">${esc(r.path)}</span>
      </div>
      <h1>${esc(cleanTitle(r.title))}</h1>
    </header>
    <article class="markdown-body">${renderMarkdown(r.markdown)}</article>
  `;
}

/* —— Search —— */
function openSearch() {
  const overlay = document.getElementById("search-overlay");
  const input = document.getElementById("search-modal-input");
  if (!overlay || !input) return;
  overlay.hidden = false;
  input.value = document.getElementById("search-input")?.value || "";
  input.focus();
  runSearch(input.value);
}

function closeSearch() {
  const overlay = document.getElementById("search-overlay");
  if (overlay) overlay.hidden = true;
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

/* —— Bootstrap —— */
async function init() {
  configureMarked();
  const main = document.getElementById("main");
  main.innerHTML = `<div class="loading">Loading course…</div>`;

  try {
    const res = await fetch("course-data.json", { cache: "no-cache" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.course = await res.json();
  } catch (err) {
    main.innerHTML = `
      <div class="error-box">
        <strong>Could not load course-data.json</strong>
        <p>${esc(err.message)}</p>
        <p>Run <code>python scripts/build_content.py</code> from the webapp folder, then serve <code>public/</code>.</p>
      </div>`;
    return;
  }

  document.title = `${state.course.title} · Learn`;
  updateProgressUI();
  render();

  window.addEventListener("hashchange", () => render());

  document.getElementById("menu-btn")?.addEventListener("click", openSidebar);
  document.getElementById("sidebar-close")?.addEventListener("click", closeSidebar);

  document.querySelectorAll("[data-route]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const r = btn.dataset.route;
      if (r === "home") navigate("#/");
      if (r === "resources") navigate("#/resources");
      closeSidebar();
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
  sideSearch?.addEventListener("input", () => renderSidebar());
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
    if (e.key === "/" && !typing && !e.metaKey && !e.ctrlKey) {
      e.preventDefault();
      openSearch();
    }
    if (e.key === "Escape") {
      closeSearch();
      closeSidebar();
    }
  });
}

function highlightSearchHit() {
  document.querySelectorAll(".search-hit").forEach((el, i) => {
    el.classList.toggle("active", i === state.searchActive);
    if (i === state.searchActive) el.scrollIntoView({ block: "nearest" });
  });
}

init();
