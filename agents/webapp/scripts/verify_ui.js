#!/usr/bin/env node
/**
 * Verification suite for the ADK course webapp SPA.
 * Drives shipped ui-state.js and validates public assets structure.
 *
 * Usage: node scripts/verify_ui.js
 * Exit 0 on success, 1 on failure.
 */
"use strict";

const fs = require("fs");
const path = require("path");
const assert = require("assert");

const ROOT = path.resolve(__dirname, "..");
const PUBLIC = path.join(ROOT, "public");

function read(rel) {
  return fs.readFileSync(path.join(PUBLIC, rel), "utf8");
}

function fail(msg) {
  console.error("FAIL:", msg);
  process.exitCode = 1;
}

function ok(msg) {
  console.log("OK:", msg);
}

// —— 1. Pure unit tests of shipped ui-state.js ——
const Ui = require(path.join(PUBLIC, "ui-state.js"));

assert.strictEqual(Ui.MOBILE_MAX, 860);
assert.strictEqual(Ui.isMobileWidth(860), true);
assert.strictEqual(Ui.isMobileWidth(861), false);
assert.strictEqual(Ui.isMobileWidth(375), true);
ok("isMobileWidth breakpoints");

const closedMobile = Ui.drawerState(false, true);
assert.strictEqual(closedMobile.sidebarHasOpenClass, false);
assert.strictEqual(closedMobile.bodyHasSidebarOpen, false);
assert.strictEqual(closedMobile.backdropHidden, true);
assert.strictEqual(closedMobile.sidebarAriaHidden, true);
assert.strictEqual(closedMobile.lockBodyScroll, false);
assert.strictEqual(closedMobile.menuAriaExpanded, false);
ok("drawerState closed mobile");

const openMobile = Ui.drawerState(true, true);
assert.strictEqual(openMobile.sidebarHasOpenClass, true);
assert.strictEqual(openMobile.bodyHasSidebarOpen, true);
assert.strictEqual(openMobile.backdropHidden, false);
assert.strictEqual(openMobile.sidebarAriaHidden, false);
assert.strictEqual(openMobile.lockBodyScroll, true);
assert.strictEqual(openMobile.menuLabel, "Close menu");
ok("drawerState open mobile");

const openDesktop = Ui.drawerState(true, false);
// Desktop should not lock scroll / treat as drawer presentation when not mobile
assert.strictEqual(openDesktop.bodyHasSidebarOpen, false);
assert.strictEqual(openDesktop.backdropHidden, true);
assert.strictEqual(openDesktop.sidebarAriaHidden, false);
assert.strictEqual(openDesktop.lockBodyScroll, false);
ok("drawerState open desktop does not lock/backdrop");

// applyDrawerState with mock DOM
function mockEl(initial) {
  const classes = new Set(initial.classList || []);
  const attrs = { ...(initial.attrs || {}) };
  return {
    classList: {
      add: (c) => classes.add(c),
      remove: (c) => classes.delete(c),
      contains: (c) => classes.has(c),
      _set: classes,
    },
    setAttribute(k, v) {
      attrs[k] = v;
    },
    getAttribute(k) {
      return attrs[k];
    },
    get hidden() {
      return attrs.hidden === true || attrs.hidden === "true";
    },
    set hidden(v) {
      attrs.hidden = !!v;
    },
    _attrs: attrs,
  };
}

const sidebar = mockEl({});
const backdrop = mockEl({ attrs: { hidden: true } });
const menuBtn = mockEl({});
const body = mockEl({});
Ui.applyDrawerState({ sidebar, backdrop, menuBtn, body }, true, true);
assert.ok(sidebar.classList.contains("open"));
assert.ok(body.classList.contains("sidebar-open"));
assert.strictEqual(backdrop.hidden, false);
assert.strictEqual(menuBtn.getAttribute("aria-expanded"), "true");
Ui.applyDrawerState({ sidebar, backdrop, menuBtn, body }, false, true);
assert.ok(!sidebar.classList.contains("open"));
assert.ok(!body.classList.contains("sidebar-open"));
assert.strictEqual(backdrop.hidden, true);
assert.strictEqual(menuBtn.getAttribute("aria-expanded"), "false");
ok("applyDrawerState open/close mobile");

// Theme helpers
assert.strictEqual(Ui.resolveTheme("light", true).effective, "light");
assert.strictEqual(Ui.resolveTheme("dark", false).effective, "dark");
assert.strictEqual(Ui.resolveTheme("system", true).effective, "dark");
assert.strictEqual(Ui.resolveTheme("system", false).effective, "light");
assert.strictEqual(Ui.resolveTheme(null, true).effective, "dark");
assert.strictEqual(Ui.nextThemePreference("system"), "light");
assert.strictEqual(Ui.nextThemePreference("light"), "dark");
assert.strictEqual(Ui.nextThemePreference("dark"), "system");
const fakeDoc = {
  attrs: {},
  setAttribute(k, v) {
    this.attrs[k] = v;
  },
  removeAttribute(k) {
    delete this.attrs[k];
  },
};
Ui.applyThemeToDocument(fakeDoc, "dark", false);
assert.strictEqual(fakeDoc.attrs["data-theme"], "dark");
Ui.applyThemeToDocument(fakeDoc, "system", true);
assert.strictEqual(fakeDoc.attrs["data-theme"], undefined);
ok("theme resolve / cycle / applyThemeToDocument");

// —— 2. course-data.json shape via shipped validator ——
const coursePath = path.join(PUBLIC, "course-data.json");
assert.ok(fs.existsSync(coursePath), "course-data.json exists");
const course = JSON.parse(fs.readFileSync(coursePath, "utf8"));
const shape = Ui.validateCourseData(course);
assert.strictEqual(shape.ok, true, shape.errors.join("; "));
assert.ok(course.modules.length >= 1);
assert.ok(course.tracks.length >= 1);
assert.ok(course.resources.length >= 1);
ok(`course-data.json: ${course.modules.length} modules, ${course.tracks.length} tracks`);

// —— 3. Structural checks of shipped app.js + index.html ——
const appJs = read("app.js");
const indexHtml = read("index.html");
const stylesCss = read("styles.css");

function assertIncludes(hay, needle, label) {
  if (!hay.includes(needle)) {
    fail(`${label}: missing ${JSON.stringify(needle)}`);
  } else {
    ok(label);
  }
}

// Chrome wired before async fetch
const wireIdx = appJs.indexOf("wireChromeControls()");
const fetchIdx = appJs.indexOf('fetch("course-data.json"');
assert.ok(wireIdx >= 0, "wireChromeControls call exists");
assert.ok(fetchIdx >= 0, "fetch course-data exists");
assert.ok(wireIdx < fetchIdx, "wireChromeControls before fetch");
ok("menu/close wired before content fetch");

assertIncludes(appJs, "function openSidebar", "openSidebar exists");
assertIncludes(appJs, "function closeSidebar", "closeSidebar exists");
assertIncludes(appJs, "function toggleSidebar", "toggleSidebar exists");
assertIncludes(appJs, "state.drawerOpen", "drawerOpen state");
assertIncludes(appJs, "syncDrawerDom", "syncDrawerDom");
assertIncludes(appJs, "sidebar-open", "sidebar-open body class");
assertIncludes(appJs, "closeSearch", "closeSearch");
assertIncludes(appJs, "openSearch", "openSearch");
assertIncludes(appJs, "searchReturnFocus", "search focus restore");
assertIncludes(appJs, 'e.key === "Escape"', "Escape handling");
assertIncludes(appJs, "toggle-done", "mark complete control");

assertIncludes(indexHtml, 'id="menu-btn"', "menu button in HTML");
assertIncludes(indexHtml, 'id="sidebar-close"', "close button in HTML");
assertIncludes(indexHtml, 'id="sidebar-backdrop"', "backdrop in HTML");
assertIncludes(indexHtml, "ui-state.js", "ui-state.js script");
assertIncludes(indexHtml, 'aria-controls="sidebar"', "menu aria-controls");
assertIncludes(indexHtml, 'role="dialog"', "search dialog role");
assertIncludes(indexHtml, 'id="theme-toggle"', "theme toggle in HTML");
assertIncludes(stylesCss, '[data-theme="dark"]', "dark theme CSS tokens");
assertIncludes(appJs, "wireThemeControls", "theme controls wired");
assertIncludes(appJs, "cycleTheme", "theme cycle function");

assertIncludes(stylesCss, "max-width: 860px", "mobile media query");
assertIncludes(stylesCss, "translateX(-100%)", "drawer off-canvas transform");
assertIncludes(stylesCss, ".sidebar.open", "sidebar open class CSS");
assertIncludes(stylesCss, "min-height: 44px", "44px min hit target");
assertIncludes(stylesCss, ":focus-visible", "focus-visible styles");
assertIncludes(stylesCss, "body.sidebar-open", "body scroll lock class");

// Stacking: .sidebar z-index must be > .topbar so #sidebar-close receives clicks
function cssRuleZIndex(css, selector) {
  // Match `.selector { ... z-index: N; ... }` first block for that selector
  const re = new RegExp(
    selector.replace(".", "\\.") +
      "\\s*\\{[^}]*?z-index\\s*:\\s*(-?\\d+)",
    "i"
  );
  const m = css.match(re);
  return m ? parseInt(m[1], 10) : null;
}
const zSidebar = cssRuleZIndex(stylesCss, ".sidebar");
const zTopbar = cssRuleZIndex(stylesCss, ".topbar");
const zBackdrop = cssRuleZIndex(stylesCss, ".sidebar-backdrop:not([hidden])")
  ?? cssRuleZIndex(stylesCss, ".sidebar-backdrop");
assert.ok(zSidebar != null && zTopbar != null, "parsed sidebar/topbar z-index");
assert.ok(
  zSidebar > zTopbar,
  `sidebar z-index (${zSidebar}) must be > topbar (${zTopbar}) so close (×) is not covered`
);
if (zBackdrop != null) {
  assert.ok(zSidebar > zBackdrop, `sidebar (${zSidebar}) > backdrop (${zBackdrop})`);
  // Menu sits in topbar; on mobile it is on the right, outside the drawer.
  // Backdrop must sit under the open sidebar; topbar may be under or over backdrop
  // as long as menu remains clickable (right side, clear of drawer).
  assert.ok(zSidebar > zBackdrop, "sidebar above backdrop");
}
ok(`stacking z-index sidebar=${zSidebar} > topbar=${zTopbar}, backdrop=${zBackdrop}`);
assertIncludes(appJs, 'closest("#menu-btn")', "capture delegation for menu");
assertIncludes(appJs, 'closest("#sidebar-close")', "capture delegation for close");

// No heading-in-button regression
if (appJs.includes("<h3 class=\"syl-title\"") || appJs.includes("<h3 class='syl-title'")) {
  fail("syllabus still uses h3 inside button");
} else {
  ok("syllabus uses span titles (valid button content)");
}

// —— 4. Live hit-test: elementFromPoint on #sidebar-close with drawer open ——
async function runCloseButtonHitTest() {
  const { spawn } = require("child_process");
  const http = require("http");
  const PORT = 8791;
  const BASE = `http://127.0.0.1:${PORT}`;

  function waitHttp(ms = 8000) {
    const start = Date.now();
    return new Promise((resolve, reject) => {
      const tick = () => {
        http
          .get(BASE + "/", (res) => {
            res.resume();
            resolve(res.statusCode);
          })
          .on("error", () => {
            if (Date.now() - start > ms) reject(new Error("server not up"));
            else setTimeout(tick, 150);
          });
      };
      tick();
    });
  }

  let playwright;
  try {
    playwright = require("playwright");
  } catch {
    // Try loading from npx cache path is unreliable; install-adjacent optional
    try {
      playwright = require(path.join(ROOT, "node_modules", "playwright"));
    } catch {
      console.log("SKIP: playwright not installed — run: cd webapp && npm i playwright && npx playwright install chromium");
      return { skipped: true };
    }
  }

  const server = spawn("python3", [path.join(ROOT, "serve.py"), "--no-open", "-p", String(PORT)], {
    cwd: ROOT,
    stdio: ["ignore", "pipe", "pipe"],
  });

  let serverLog = "";
  server.stdout.on("data", (d) => (serverLog += d));
  server.stderr.on("data", (d) => (serverLog += d));

  try {
    await waitHttp();
    const browser = await playwright.chromium.launch({ headless: true });
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const pageErrors = [];
    page.on("pageerror", (e) => pageErrors.push(String(e.message || e)));

    await page.goto(BASE + "/", { waitUntil: "networkidle", timeout: 30000 });
    await page.waitForSelector("#menu-btn", { state: "visible", timeout: 10000 });

    // Open drawer and wait for transform (0.2s) so close is on-screen
    await page.locator("#menu-btn").click();
    await page.waitForSelector("#sidebar.open", { timeout: 5000 });
    await page.waitForFunction(
      () => {
        const btn = document.getElementById("sidebar-close");
        if (!btn) return false;
        const r = btn.getBoundingClientRect();
        return r.width > 0 && r.left >= 0 && r.right <= window.innerWidth + 1;
      },
      { timeout: 5000 }
    );

    // Hit-test center of close button — must be the topmost target
    const hit = await page.evaluate(() => {
      const btn = document.getElementById("sidebar-close");
      if (!btn) return { error: "no close btn" };
      const r = btn.getBoundingClientRect();
      const x = r.left + r.width / 2;
      const y = r.top + r.height / 2;
      const top = document.elementFromPoint(x, y);
      let el = top;
      let matched = false;
      while (el) {
        if (el.id === "sidebar-close") {
          matched = true;
          break;
        }
        el = el.parentElement;
      }
      const sidebar = document.getElementById("sidebar");
      const topbar = document.querySelector(".topbar");
      const csSide = sidebar ? getComputedStyle(sidebar) : null;
      const csTop = topbar ? getComputedStyle(topbar) : null;
      return {
        x,
        y,
        topId: top && top.id,
        topTag: top && top.tagName,
        topClass: top && top.className,
        matched,
        rect: { left: r.left, top: r.top, width: r.width, height: r.height },
        zSidebar: csSide && csSide.zIndex,
        zTopbar: csTop && csTop.zIndex,
      };
    });

    if (!hit.matched) {
      throw new Error(
        `elementFromPoint on #sidebar-close hit ${hit.topTag}.${hit.topClass}#${hit.topId} instead of close button: ${JSON.stringify(hit)}`
      );
    }
    if (!(parseInt(hit.zSidebar, 10) > parseInt(hit.zTopbar, 10))) {
      throw new Error(`computed z-index sidebar (${hit.zSidebar}) not > topbar (${hit.zTopbar})`);
    }

    // Click dismisses drawer
    await page.locator("#sidebar-close").click({ force: false });
    await page.waitForFunction(() => !document.getElementById("sidebar")?.classList.contains("open"), {
      timeout: 5000,
    });
    const stillOpen = await page.locator("#sidebar.open").count();
    if (stillOpen !== 0) {
      throw new Error("drawer still open after clicking #sidebar-close");
    }

    await browser.close();
    return { skipped: false, hit, pageErrors, serverLog };
  } finally {
    server.kill("SIGTERM");
    try {
      server.kill("SIGKILL");
    } catch {
      /* ignore */
    }
  }
}

(async () => {
  try {
    const result = await runCloseButtonHitTest();
    if (result.skipped) {
      // Hard-require stacking assert already passed; still fail CI if env forces live test
      if (process.env.REQUIRE_HIT_TEST === "1") {
        fail("REQUIRE_HIT_TEST=1 but playwright unavailable");
      } else {
        ok("close-button hit-test skipped (no playwright); z-index stacking asserted");
      }
    } else {
      if (result.pageErrors && result.pageErrors.length) {
        fail("page errors: " + result.pageErrors.join("; "));
      } else {
        ok("elementFromPoint hits #sidebar-close when drawer open; click closes drawer");
      }
    }
  } catch (err) {
    fail("close-button hit-test: " + err.message);
  }

  if (process.exitCode) {
    console.error("\nverify_ui.js FAILED");
    process.exit(1);
  }
  console.log("\nverify_ui.js PASSED");
})();
