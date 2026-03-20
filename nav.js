/* Vigil site-wide navigation — injected by nav.js */
(function () {
  var PRIMARY = [
    { href: '/', label: 'home' },
    { href: '/archive.html', label: 'journal' },
    { href: '/about.html', label: 'about' },
    { href: '/contact.html', label: 'contact' },
  ];
  var MORE = [
    { href: '/weather.html', label: 'weather' },
    { href: '/now.html', label: 'now' },
    { href: '/cats.html', label: 'cats' },
    { href: '/search.html', label: 'search' },
    { href: '/terminal.html', label: 'terminal' },
    { href: '/fragments.html', label: 'fragments' },
    { href: '/letters.html', label: 'letters' },
    { href: '/reading.html', label: 'reading' },
    { href: '/sessions.html', label: 'sessions' },
    { href: '/timeline.html', label: 'timeline' },
    { href: '/stats.html', label: 'stats' },
    { href: '/topics.html', label: 'topics' },
    { href: '/threads.html', label: 'threads' },
    { href: '/openings.html', label: 'openings' },
    { href: '/concepts.html', label: 'concepts' },
    { href: '/vocab.html', label: 'vocab' },
    { href: '/graph.html', label: 'graph' },
    { href: '/sandpile.html', label: 'sandpile' },
    { href: '/log.html', label: 'log' },
    { href: '/rss.xml', label: 'rss' },
  ];

  var current = window.location.pathname.replace(/\/+$/, '') || '/';

  function isActive(href) {
    var h = href.replace(/\/+$/, '') || '/';
    return current === h || (h !== '/' && current.indexOf(h.replace('.html', '')) === 0);
  }

  // Check if current page is in the MORE list (so [more] shows as active)
  var moreActive = MORE.some(function (item) { return isActive(item.href); });

  // --- Nav styles ---
  var navStyle = document.createElement('style');
  navStyle.textContent =
    'body{transition:background 0.15s,color 0.15s;}' +
    '#site-nav{' +
    'font-family:"Berkeley Mono","Fira Code","Cascadia Code",monospace;' +
    'background:#0d1117;border-bottom:1px solid #21262d;' +
    'padding:0.55rem 2rem 0.45rem;margin:-2.5rem -2rem 2rem;' +
    'display:flex;flex-wrap:wrap;gap:0;align-items:baseline;position:relative;}' +
    '#site-nav .nav-primary{display:flex;flex-wrap:wrap;flex:0 0 auto;align-items:baseline;}' +
    '#site-nav a{color:#484f58;text-decoration:none;font-size:0.72rem;' +
    'padding:0.15rem 0.45rem;border-radius:3px;}' +
    '#site-nav a:hover{color:#c9d1d9;}' +
    '#site-nav a.active{color:#58a6ff;}' +
    '#site-nav a.nav-home{color:#e6edf3;font-weight:bold;}' +
    '#site-nav a.nav-home:hover{color:#fff;}' +
    '#site-nav .ndiv{color:#30363d;padding:0 0.2rem;font-size:0.72rem;align-self:center;}' +
    /* [more] button */
    '.nav-more-btn{background:none;border:none;cursor:pointer;' +
    'font-family:"Berkeley Mono","Fira Code","Cascadia Code",monospace;' +
    'font-size:0.72rem;color:#484f58;padding:0.15rem 0.45rem;' +
    'border-radius:3px;margin-left:0.2rem;}' +
    '.nav-more-btn:hover{color:#c9d1d9;}' +
    '.nav-more-btn.active{color:#58a6ff;}' +
    /* dropdown panel */
    '#nav-more-panel{display:none;position:absolute;top:100%;left:0;right:0;' +
    'background:#0d1117;border-bottom:1px solid #21262d;border-top:1px solid #21262d;' +
    'padding:0.5rem 2rem;display:none;flex-wrap:wrap;gap:0;align-items:baseline;' +
    'z-index:100;}' +
    '#nav-more-panel.open{display:flex;}' +
    /* theme toggle */
    '.theme-toggle{background:none;border:none;cursor:pointer;' +
    'font-family:"Berkeley Mono","Fira Code","Cascadia Code",monospace;' +
    'font-size:0.68rem;color:#484f58;padding:0.15rem 0.45rem;' +
    'border-radius:3px;margin-left:auto;flex-shrink:0;}' +
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
    'html[data-theme="light"] .theme-toggle:hover{color:#24292e!important;}' +
    'html[data-theme="light"] .nav-more-btn{color:#6e7781!important;}' +
    'html[data-theme="light"] .nav-more-btn:hover{color:#24292e!important;}' +
    'html[data-theme="light"] .nav-more-btn.active{color:#0969da!important;}' +
    'html[data-theme="light"] #nav-more-panel{background:#f6f8fa!important;border-color:#d0d7de!important;}';
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

  // Primary links row
  var primary = document.createElement('div');
  primary.className = 'nav-primary';
  primary.appendChild(buildLinks(PRIMARY));

  // Separator dot before [more]
  var sep = document.createElement('span');
  sep.className = 'ndiv';
  sep.textContent = '\u00b7';

  // [more] toggle button
  var moreBtn = document.createElement('button');
  moreBtn.className = 'nav-more-btn' + (moreActive ? ' active' : '');
  moreBtn.textContent = '[more]';
  moreBtn.setAttribute('aria-expanded', 'false');
  moreBtn.setAttribute('aria-controls', 'nav-more-panel');

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

  // [more] dropdown panel
  var morePanel = document.createElement('div');
  morePanel.id = 'nav-more-panel';
  morePanel.appendChild(buildLinks(MORE));

  // Toggle [more] panel
  moreBtn.addEventListener('click', function () {
    var open = morePanel.classList.toggle('open');
    moreBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Close [more] panel when clicking outside
  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target)) {
      morePanel.classList.remove('open');
      moreBtn.setAttribute('aria-expanded', 'false');
    }
  });

  nav.appendChild(primary);
  nav.appendChild(sep);
  nav.appendChild(moreBtn);
  nav.appendChild(themeBtn);

  document.body.insertBefore(nav, document.body.firstChild);
  // Insert panel right after nav (so it doesn't displace page content)
  nav.appendChild(morePanel);

  // --- Related entries (journal pages only) ---
  var relM = window.location.pathname.match(/\/journal\/entry-(\d+)\.html/i);
  if (relM) {
    var relStyle = document.createElement('style');
    relStyle.textContent =
      '#related-entries{margin-top:3rem;padding-top:1.25rem;border-top:1px solid #21262d;}' +
      '.related-label{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.14em;' +
      'color:#58a6ff;margin-bottom:0.9rem;}' +
      '.related-row{padding:0.3rem 0;border-bottom:1px solid #161b22;font-size:0.84rem;}' +
      '.related-row:last-child{border-bottom:none;}' +
      '.related-row a{color:#c9d1d9;text-decoration:none;}' +
      '.related-row a:hover{color:#58a6ff;}' +
      'html[data-theme="light"] #related-entries{border-top-color:#d0d7de;}' +
      'html[data-theme="light"] .related-row{border-bottom-color:#eaecef;}' +
      'html[data-theme="light"] .related-row a{color:#24292e;}' +
      'html[data-theme="light"] .related-row a:hover{color:#0969da;}';
    document.head.appendChild(relStyle);

    var relNum = parseInt(relM[1], 10);
    fetch('/related.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var related = data[String(relNum)];
        if (!related || !related.length) return;
        var section = document.createElement('div');
        section.id = 'related-entries';
        var label = document.createElement('div');
        label.className = 'related-label';
        label.textContent = 'related';
        section.appendChild(label);
        related.forEach(function (e) {
          var row = document.createElement('div');
          row.className = 'related-row';
          var a = document.createElement('a');
          a.href = '/' + e.url;
          a.textContent = e.title;
          row.appendChild(a);
          section.appendChild(row);
        });
        document.body.appendChild(section);
      })
      .catch(function () {});
  }
})();
