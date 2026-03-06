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
    { href: '/sessions.html', label: 'sessions' },
    { href: '/log.html', label: 'log' },
    { href: '/rss.xml', label: 'rss' },
  ];

  var current = window.location.pathname.replace(/\/+$/, '') || '/';

  function isActive(href) {
    var h = href.replace(/\/+$/, '') || '/';
    return current === h || (h !== '/' && current.indexOf(h.replace('.html', '')) === 0);
  }

  var style = document.createElement('style');
  style.textContent =
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
    '#site-nav .ndiv{color:#30363d;padding:0 0.2rem;font-size:0.72rem;align-self:center;}';
  document.head.appendChild(style);

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

  nav.appendChild(primary);
  nav.appendChild(sep);
  nav.appendChild(secondary);

  document.body.insertBefore(nav, document.body.firstChild);
})();
