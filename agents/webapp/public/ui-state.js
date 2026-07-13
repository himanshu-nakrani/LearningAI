/**
 * Pure UI state helpers for the ADK course SPA.
 * Usable in the browser (script tag) and in Node tests (require/import).
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.AdkUiState = factory();
  }
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  var MOBILE_MAX = 860;

  function isMobileWidth(widthPx) {
    return Number(widthPx) <= MOBILE_MAX;
  }

  /**
   * Compute drawer-related UI flags.
   * @param {boolean} isOpen
   * @param {boolean} isMobile
   */
  function drawerState(isOpen, isMobile) {
    var open = !!isOpen;
    var mobile = !!isMobile;
    return {
      sidebarHasOpenClass: open,
      bodyHasSidebarOpen: open && mobile,
      backdropHidden: !(open && mobile),
      sidebarAriaHidden: mobile ? !open : false,
      menuAriaExpanded: open && mobile,
      menuLabel: open && mobile ? "Close menu" : "Open menu",
      lockBodyScroll: open && mobile,
    };
  }

  /**
   * Apply drawer state to a minimal DOM-like surface (for tests + browser).
   * els: { sidebar, backdrop, menuBtn, body }
   */
  function applyDrawerState(els, isOpen, isMobile) {
    var s = drawerState(isOpen, isMobile);
    var sidebar = els.sidebar;
    var backdrop = els.backdrop;
    var menuBtn = els.menuBtn;
    var body = els.body;

    if (sidebar) {
      if (s.sidebarHasOpenClass) sidebar.classList.add("open");
      else sidebar.classList.remove("open");
      sidebar.setAttribute("aria-hidden", s.sidebarAriaHidden ? "true" : "false");
    }
    if (body) {
      if (s.bodyHasSidebarOpen) body.classList.add("sidebar-open");
      else body.classList.remove("sidebar-open");
    }
    if (backdrop) {
      backdrop.hidden = s.backdropHidden;
      if (typeof backdrop.setAttribute === "function") {
        backdrop.setAttribute("aria-hidden", s.backdropHidden ? "true" : "false");
      }
    }
    if (menuBtn) {
      menuBtn.setAttribute("aria-expanded", s.menuAriaExpanded ? "true" : "false");
      menuBtn.setAttribute("aria-label", s.menuLabel);
    }
    return s;
  }

  /** Validate course-data.json shape used by the SPA home render. */
  function validateCourseData(data) {
    var errors = [];
    if (!data || typeof data !== "object") {
      return { ok: false, errors: ["data is not an object"] };
    }
    if (!data.title) errors.push("missing title");
    if (!Array.isArray(data.modules) || data.modules.length === 0) {
      errors.push("modules empty or missing");
    } else {
      var m0 = data.modules[0];
      if (!m0.id || !m0.title || typeof m0.markdown !== "string") {
        errors.push("module missing id/title/markdown");
      }
    }
    if (!Array.isArray(data.tracks) || data.tracks.length === 0) {
      errors.push("tracks empty or missing");
    }
    if (!Array.isArray(data.resources) || data.resources.length === 0) {
      errors.push("resources empty or missing");
    }
    if (typeof data.moduleCount === "number" && data.modules && data.moduleCount !== data.modules.length) {
      errors.push("moduleCount mismatch");
    }
    return { ok: errors.length === 0, errors: errors };
  }

  var THEME_KEY = "adk-course-theme-v1";

  /**
   * Resolve stored preference to effective theme.
   * stored: "light" | "dark" | "system" | null/undefined
   * prefersDark: boolean from matchMedia
   * returns: { preference, effective } where effective is "light"|"dark"
   */
  function resolveTheme(stored, prefersDark) {
    var pref = stored === "light" || stored === "dark" || stored === "system" ? stored : "system";
    var effective = pref === "system" ? (prefersDark ? "dark" : "light") : pref;
    return { preference: pref, effective: effective };
  }

  /** Cycle: system → light → dark → system (or light ↔ dark when explicit) */
  function nextThemePreference(currentPref) {
    if (currentPref === "light") return "dark";
    if (currentPref === "dark") return "system";
    return "light";
  }

  /**
   * Apply theme to documentElement-like node.
   * docEl: { setAttribute, removeAttribute, dataset? }
   */
  function applyThemeToDocument(docEl, preference, prefersDark) {
    var r = resolveTheme(preference, prefersDark);
    if (r.preference === "system") {
      docEl.removeAttribute("data-theme");
    } else {
      docEl.setAttribute("data-theme", r.effective);
    }
    return r;
  }

  function themeToggleLabel(preference, effective) {
    if (preference === "system") {
      return "Theme: system (" + effective + ")";
    }
    return "Theme: " + effective;
  }

  function themeToggleIcon(effective) {
    return effective === "dark" ? "☾" : "☀";
  }

  return {
    MOBILE_MAX: MOBILE_MAX,
    THEME_KEY: THEME_KEY,
    isMobileWidth: isMobileWidth,
    drawerState: drawerState,
    applyDrawerState: applyDrawerState,
    validateCourseData: validateCourseData,
    resolveTheme: resolveTheme,
    nextThemePreference: nextThemePreference,
    applyThemeToDocument: applyThemeToDocument,
    themeToggleLabel: themeToggleLabel,
    themeToggleIcon: themeToggleIcon,
  };
});
