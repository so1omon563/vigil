(function () {
  try {
    var theme = localStorage.getItem('theme');
    if (theme) document.documentElement.setAttribute('data-theme', theme);
  } catch (e) {
    // Theme preference is optional; older pages should still render without it.
  }
}());
