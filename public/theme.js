(() => {
  const root = document.documentElement;
  const storageKey = "aixcel-color-theme";
  const media = window.matchMedia("(prefers-color-scheme: dark)");
  const toggle = document.querySelector("#theme-toggle");
  const themeMeta = document.querySelector('meta[name="theme-color"]');

  function storedTheme() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return value === "light" || value === "dark" ? value : null;
    } catch {
      return null;
    }
  }

  function applyTheme(theme, persist = false) {
    const resolved = theme === "dark" ? "dark" : "light";
    root.dataset.theme = resolved;
    root.style.colorScheme = resolved;
    if (persist) {
      try {
        window.localStorage.setItem(storageKey, resolved);
      } catch {
        // The selected theme still applies when storage is unavailable.
      }
    }

    const next = resolved === "dark" ? "light" : "dark";
    if (toggle) {
      toggle.setAttribute("aria-label", `Switch to ${next} theme`);
      toggle.setAttribute("title", `Switch to ${next} theme`);
      toggle.setAttribute("aria-pressed", String(resolved === "dark"));
    }
    if (themeMeta) {
      const browserColor = getComputedStyle(root).getPropertyValue("--theme-browser").trim();
      if (browserColor) themeMeta.setAttribute("content", browserColor);
    }
  }

  applyTheme(root.dataset.theme || storedTheme() || (media.matches ? "dark" : "light"));

  toggle?.addEventListener("click", () => {
    applyTheme(root.dataset.theme === "dark" ? "light" : "dark", true);
  });

  media.addEventListener?.("change", event => {
    if (!storedTheme()) applyTheme(event.matches ? "dark" : "light");
  });
})();
