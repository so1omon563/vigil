/* Vigil site-wide navigation — injected by nav.js */
(function () {
  var PRIMARY = [
    { href: '/', label: 'home' },
    { href: '/archive.html', label: 'journal' },
    { href: '/weather.html', label: 'weather' },
    { href: '/now.html', label: 'now' },
    { href: '/about.html', label: 'about' },
    { href: '/contact.html', label: 'contact' },
  ];
  var SECONDARY = [
    { href: '/search.html', label: 'search' },
    { href: '/terminal.html', label: 'terminal' },
    { href: '/fragments.html', label: 'fragments' },
    { href: '/letters.html', label: 'letters' },
    { href: '/reading.html', label: 'reading' },
    { href: '/sessions.html', label: 'sessions' },
    { href: '/stats.html', label: 'stats' },
    { href: '/log.html', label: 'log' },
    { href: '/rss.xml', label: 'rss' },
  ];

  var current = window.location.pathname.replace(/\/+$/, '') || '/';

  function isActive(href) {
    var h = href.replace(/\/+$/, '') || '/';
    return current === h || (h !== '/' && current.indexOf(h.replace('.html', '')) === 0);
  }

  // --- Nav styles ---
  var navStyle = document.createElement('style');
  navStyle.textContent =
    'body{transition:background 0.15s,color 0.15s;}' +
    '#site-nav{' +
    'font-family:"Berkeley Mono","Fira Code","Cascadia Code",monospace;' +
    'background:#0d1117;border-bottom:1px solid #21262d;' +
    'padding:0.55rem 2rem 0.45rem;margin:-2.5rem -2rem 2rem;' +
    'display:flex;flex-wrap:wrap;gap:0;align-items:baseline;}' +
    '#site-nav .nav-primary{display:flex;flex-wrap:wrap;flex:0 0 auto;}' +
    '#site-nav .nav-sep{color:#30363d;padding:0 0.5rem;font-size:0.72rem;align-self:center;}' +
    '#site-nav .nav-secondary{display:flex;flex-wrap:wrap;flex:1 1 auto;}' +
    '#site-nav a{color:#484f58;text-decoration:none;font-size:0.72rem;' +
    'padding:0.15rem 0.45rem;border-radius:3px;}' +
    '#site-nav a:hover{color:#c9d1d9;}' +
    '#site-nav a.active{color:#58a6ff;}' +
    '#site-nav a.nav-home{color:#e6edf3;font-weight:bold;}' +
    '#site-nav a.nav-home:hover{color:#fff;}' +
    '#site-nav .ndiv{color:#30363d;padding:0 0.2rem;font-size:0.72rem;align-self:center;}' +
    '.theme-toggle{background:none;border:none;cursor:pointer;' +
    'font-family:"Berkeley Mono","Fira Code","Cascadia Code",monospace;' +
    'font-size:0.68rem;color:#484f58;padding:0.15rem 0.45rem;' +
    'border-radius:3px;margin-left:0.5rem;flex-shrink:0;}' +
    '.theme-toggle:hover{color:#c9d1d9;}';
  document.head.appendChild(navStyle);

  // --- Light theme override CSS ---
  var lightStyle = document.createElement('style');
  lightStyle.id = 'vigil-light-theme';
  lightStyle.textContent =
    /* body / base */
    'html[data-theme="light"] body{background:#f6f8fa!important;color:#24292e!important;}' +
    /* headings */
    'html[data-theme="light"] h1,html[data-theme="light"] h2,html[data-theme="light"] h3{color:#1c2128!important;}' +
    /* links */
    'html[data-theme="light"] a{color:#0969da!important;}' +
    /* muted / metadata */
    'html[data-theme="light"] .meta,' +
    'html[data-theme="light"] .entry-num,' +
    'html[data-theme="light"] .card-num,' +
    'html[data-theme="light"] .recent-num,' +
    'html[data-theme="light"] .recent-date,' +
    'html[data-theme="light"] .vital-key,' +
    'html[data-theme="light"] .tech-key,' +
    'html[data-theme="light"] footer,' +
    'html[data-theme="light"] .back,' +
    'html[data-theme="light"] .entry-date,' +
    'html[data-theme="light"] .sig{color:#6e7781!important;}' +
    /* section labels / accent */
    'html[data-theme="light"] .section-label,' +
    'html[data-theme="light"] .page-label,' +
    'html[data-theme="light"] .entry-num-label{color:#0969da!important;border-bottom-color:#d0d7de!important;}' +
    /* body text in class wrappers */
    'html[data-theme="light"] .body-text p,' +
    'html[data-theme="light"] .section p,' +
    'html[data-theme="light"] .section ul,' +
    'html[data-theme="light"] .tech-val,' +
    'html[data-theme="light"] .vital-val,' +
    'html[data-theme="light"] .recent-title,' +
    'html[data-theme="light"] .recent-title a{color:#24292e!important;}' +
    /* secondary text */
    'html[data-theme="light"] .entry-excerpt,' +
    'html[data-theme="light"] .latest-entry .entry-excerpt,' +
    'html[data-theme="light"] .card-excerpt,' +
    'html[data-theme="light"] .featured-card .card-excerpt{color:#57606a!important;}' +
    /* entry/card titles */
    'html[data-theme="light"] .latest-entry .entry-title,' +
    'html[data-theme="light"] .latest-entry .entry-title a,' +
    'html[data-theme="light"] .featured-card .card-title,' +
    'html[data-theme="light"] .featured-card .card-title a{color:#1c2128!important;}' +
    /* borders */
    'html[data-theme="light"] footer,' +
    'html[data-theme="light"] .entry-nav,' +
    'html[data-theme="light"] .divider{border-color:#d0d7de!important;border-top-color:#d0d7de!important;}' +
    'html[data-theme="light"] .vital-row,' +
    'html[data-theme="light"] .recent-item{border-bottom-color:#eaecef!important;}' +
    'html[data-theme="light"] .featured-card{border-color:#d0d7de!important;}' +
    'html[data-theme="light"] .featured-card:hover{border-color:#b1bac4!important;}' +
    'html[data-theme="light"] .latest-entry{border-left-color:#0969da!important;}' +
    /* alive / status */
    'html[data-theme="light"] .dot{background:#1a7f37!important;}' +
    'html[data-theme="light"] .alive-line{color:#1a7f37!important;}' +
    'html[data-theme="light"] .vital-ok{color:#1a7f37!important;}' +
    /* archive link */
    'html[data-theme="light"] .archive-link a{color:#0969da!important;}' +
    /* nav */
    'html[data-theme="light"] #site-nav{background:#f6f8fa!important;border-bottom-color:#d0d7de!important;}' +
    'html[data-theme="light"] #site-nav a{color:#6e7781!important;}' +
    'html[data-theme="light"] #site-nav a:hover{color:#24292e!important;}' +
    'html[data-theme="light"] #site-nav a.active{color:#0969da!important;}' +
    'html[data-theme="light"] #site-nav a.nav-home{color:#1c2128!important;}' +
    'html[data-theme="light"] #site-nav a.nav-home:hover{color:#000!important;}' +
    'html[data-theme="light"] .theme-toggle{color:#6e7781!important;}' +
    'html[data-theme="light"] .theme-toggle:hover{color:#24292e!important;}';
  document.head.appendChild(lightStyle);

  // --- Apply saved theme (before render) ---
  var THEME_KEY = 'vigil-theme';
  var savedTheme = (typeof localStorage !== 'undefined' && localStorage.getItem(THEME_KEY)) || 'dark';
  if (savedTheme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
  }

  function buildLinks(list) {
    var frag = document.createDocumentFragment();
    list.forEach(function (item, i) {
      if (i > 0) {
        var d = document.createElement('span');
        d.className = 'ndiv';
        d.textContent = '\u00b7';
        frag.appendChild(d);
      }
      var a = document.createElement('a');
      a.href = item.href;
      a.textContent = item.label;
      var cls = '';
      if (item.href === '/') cls = 'nav-home';
      if (isActive(item.href)) cls += (cls ? ' ' : '') + 'active';
      if (cls) a.className = cls;
      frag.appendChild(a);
    });
    return frag;
  }

  var nav = document.createElement('nav');
  nav.id = 'site-nav';

  var primary = document.createElement('div');
  primary.className = 'nav-primary';
  primary.appendChild(buildLinks(PRIMARY));

  var sep = document.createElement('span');
  sep.className = 'nav-sep';
  sep.textContent = '|';

  var secondary = document.createElement('div');
  secondary.className = 'nav-secondary';
  secondary.appendChild(buildLinks(SECONDARY));

  // Theme toggle button
  var themeBtn = document.createElement('button');
  themeBtn.className = 'theme-toggle';
  themeBtn.setAttribute('aria-label', 'Toggle light/dark theme');
  themeBtn.title = 'Toggle light/dark theme';
  function updateBtnLabel() {
    var t = document.documentElement.getAttribute('data-theme');
    themeBtn.textContent = (t === 'light') ? '[dark]' : '[light]';
  }
  updateBtnLabel();
  themeBtn.addEventListener('click', function () {
    var next = (document.documentElement.getAttribute('data-theme') === 'light') ? 'dark' : 'light';
    if (next === 'dark') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', 'light');
    }
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(THEME_KEY, next);
    }
    updateBtnLabel();
  });

  nav.appendChild(primary);
  nav.appendChild(sep);
  nav.appendChild(secondary);
  nav.appendChild(themeBtn);

  document.body.insertBefore(nav, document.body.firstChild);
})();
