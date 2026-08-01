function renderIcons() {
  if (window.lucide) {
    window.lucide.createIcons();
  }
}

function setupThemeToggle() {
  const toggle = document.querySelector("#theme-toggle");

  if (!toggle) {
    return;
  }

  const root = document.documentElement;
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme) {
    root.dataset.theme = savedTheme;
  }

  toggle.addEventListener("click", () => {
    const nextTheme = root.dataset.theme === "corporate"
      ? "business"
      : "corporate";

    root.dataset.theme = nextTheme;
    localStorage.setItem("theme", nextTheme);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  renderIcons();
  setupThemeToggle();
});

document.body.addEventListener("htmx:afterSwap", renderIcons);
