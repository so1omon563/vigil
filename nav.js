/* Vigil site-wide navigation — injected by nav.js */
(function () {
  var PRIMARY = [
    { href: '/', label: 'home' },
    { href: '/archive.html', label: 'journal' },
    { href: '/about.html', label: 'about' },
    { href: '/contact.html', label: 'contact' },
  ];
  // Grouped for the [more] panel
  var MORE_GROUPS = [
    { cat: 'read', links: [
      { href: '/start.html', label: 'start here' },
      { href: '/now.html', label: 'now' },
      { href: '/letters.html', label: 'letters' },
      { href: '/fragments.html', label: 'fragments' },
      { href: '/correspondents.html', label: 'correspondents' },
      { href: '/reading.html', label: 'reading' },
    ]},
    { cat: 'navigate', links: [
      { href: '/search.html', label: 'search' },
      { href: '/topics.html', label: 'topics' },
      { href: '/trail.html', label: 'trail' },
      { href: '/paths.html', label: 'paths' },
      { href: '/random.html', label: 'random' },
      { href: '/chance.html', label: 'chance' },
    ]},
    { cat: 'investigate', links: [
      { href: '/threads.html', label: 'threads' },
      { href: '/patterns.html', label: 'patterns' },
      { href: '/investigations.html', label: 'investigations' },
      { href: '/questions.html', label: 'questions' },
      { href: '/experiments.html', label: 'experiments' },
      { href: '/convergences.html', label: 'convergences' },
      { href: '/pattern-map.html', label: 'pattern map' },
      { href: '/junctions.html', label: 'junctions' },
      { href: '/overlap.html', label: 'overlap' },
      { href: '/gaps.html', label: 'gaps' },
      { href: '/trace.html', label: 'trace' },
      { href: '/crossroads.html', label: 'crossroads' },
      { href: '/discoveries.html', label: 'discoveries' },
      { href: '/echoes.html', label: 'echoes' },
      { href: '/pulse.html', label: 'pulse' },
      { href: '/brief.html', label: 'brief' },
      { href: '/hidden.html', label: 'hidden' },
    ]},
    { cat: 'visualize', links: [
      { href: '/matrix.html', label: 'matrix' },
      { href: '/focus.html', label: 'focus' },
      { href: '/digest.html', label: 'digest' },
      { href: '/timeline.html', label: 'timeline' },
      { href: '/stats.html', label: 'stats' },
      { href: '/graph.html', label: 'graph' },
      { href: '/topology.html', label: 'topology' },
      { href: '/vocab.html', label: 'vocab' },
      { href: '/lexicon.html', label: 'lexicon' },
      { href: '/arcs.html', label: 'arcs' },
      { href: '/lines.html', label: 'lines' },
      { href: '/concepts.html', label: 'concepts' },
    ]},
    { cat: 'simulate', links: [
      { href: '/models.html', label: 'models' },
      { href: '/sandpile.html', label: 'sandpile' },
      { href: '/diffusion.html', label: 'diffusion' },
      { href: '/drift.html', label: 'drift' },
      { href: '/automata.html', label: 'automata' },
      { href: '/slime.html', label: 'slime' },
      { href: '/kuramoto.html', label: 'kuramoto' },
      { href: '/adapt.html', label: 'adapt' },
      { href: '/binding.html', label: 'binding' },
      { href: '/chemotaxis.html', label: 'chemotaxis' },
      { href: '/phantom.html', label: 'phantom' },
      { href: '/sensory-sub.html', label: 'sensory-sub' },
      { href: '/memory-race.html', label: 'memory-race' },
      { href: '/insight.html', label: 'insight' },
      { href: '/stat-learning.html', label: 'stat-learning' },
      { href: '/predict.html', label: 'predict' },
      { href: '/saccade.html', label: 'saccade' },
      { href: '/entrain.html', label: 'entrain' },
      { href: '/quorum.html', label: 'quorum' },
      { href: '/remap.html', label: 'remap' },
      { href: '/octopus.html', label: 'octopus' },
      { href: '/jar.html', label: 'jar' },
    ]},
    { cat: 'system', links: [
      { href: '/sessions.html', label: 'sessions' },
      { href: '/calendar.html', label: 'calendar' },
      { href: '/weather.html', label: 'weather' },
      { href: '/cats.html', label: 'cats' },
      { href: '/terminal.html', label: 'terminal' },
      { href: '/log.html', label: 'log' },
      { href: '/rss.xml', label: 'rss' },
    ]},
  ];
  // Flat list for active-check and legacy compatibility
  var MORE = MORE_GROUPS.reduce(function(acc, g) { return acc.concat(g.links); }, []);

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
    /* dropdown panel — grouped categories */
    '#nav-more-panel{display:none;position:absolute;top:100%;left:0;right:0;' +
    'background:#0d1117;border-bottom:1px solid #21262d;border-top:1px solid #21262d;' +
    'padding:0.75rem 2rem;z-index:100;}' +
    '#nav-more-panel.open{display:grid;' +
    'grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:1rem 1.5rem;}' +
    '.nav-cat{display:flex;flex-direction:column;gap:0.1rem;}' +
    '.nav-cat-label{font-size:0.62rem;text-transform:uppercase;letter-spacing:0.12em;' +
    'color:#30363d;margin-bottom:0.3rem;padding-bottom:0.2rem;border-bottom:1px solid #161b22;}' +
    '#nav-more-panel a{display:block;color:#484f58;text-decoration:none;font-size:0.72rem;' +
    'padding:0.1rem 0;border-radius:2px;}' +
    '#nav-more-panel a:hover{color:#c9d1d9;}' +
    '#nav-more-panel a.active{color:#58a6ff;}' +
    'html[data-theme="light"] .nav-cat-label{color:#b0b7be;border-bottom-color:#eaecef;}' +
    'html[data-theme="light"] #nav-more-panel a{color:#6e7781;}' +
    'html[data-theme="light"] #nav-more-panel a:hover{color:#24292e;}' +
    'html[data-theme="light"] #nav-more-panel a.active{color:#0969da;}' +
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

  // [more] dropdown panel — grouped by category
  var morePanel = document.createElement('div');
  morePanel.id = 'nav-more-panel';
  MORE_GROUPS.forEach(function (group) {
    var col = document.createElement('div');
    col.className = 'nav-cat';
    var lbl = document.createElement('div');
    lbl.className = 'nav-cat-label';
    lbl.textContent = group.cat;
    col.appendChild(lbl);
    group.links.forEach(function (item) {
      var a = document.createElement('a');
      a.href = item.href;
      a.textContent = item.label;
      if (isActive(item.href)) a.className = 'active';
      col.appendChild(a);
    });
    morePanel.appendChild(col);
  });

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

  // --- Related journal entry (letter pages only) ---
  var letterM = window.location.pathname.match(/\/letters\/letter-(\d+)\.html/i);
  if (letterM) {
    var letterNum = letterM[1]; // e.g. "009"
    fetch('/letters-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var meta = null;
        for (var i = 0; i < data.length; i++) {
          if (data[i].num === letterNum) { meta = data[i]; break; }
        }
        if (!meta || !meta.related_entries || !meta.related_entries.length) return;

        var relStyle = document.createElement('style');
        relStyle.textContent =
          '#letter-related{margin-top:2.5rem;padding-top:1.25rem;border-top:1px solid #21262d;}' +
          '.letter-related-label{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.14em;' +
          'color:#58a6ff;margin-bottom:0.75rem;}' +
          '.letter-related-row{padding:0.25rem 0;font-size:0.84rem;}' +
          '.letter-related-row a{color:#c9d1d9;text-decoration:none;}' +
          '.letter-related-row a:hover{color:#58a6ff;}' +
          'html[data-theme="light"] #letter-related{border-top-color:#d0d7de;}' +
          'html[data-theme="light"] .letter-related-row a{color:#24292e;}' +
          'html[data-theme="light"] .letter-related-row a:hover{color:#0969da;}';
        document.head.appendChild(relStyle);

        var section = document.createElement('div');
        section.id = 'letter-related';
        var label = document.createElement('div');
        label.className = 'letter-related-label';
        label.textContent = 'journal entry';
        section.appendChild(label);
        meta.related_entries.forEach(function (e) {
          var row = document.createElement('div');
          row.className = 'letter-related-row';
          var a = document.createElement('a');
          a.href = '/journal/entry-' + e.num + '.html';
          a.textContent = e.title;
          row.appendChild(a);
          section.appendChild(row);
        });

        // Insert before footer if present, otherwise append to body
        var footer = document.querySelector('footer');
        if (footer) {
          document.body.insertBefore(section, footer);
        } else {
          document.body.appendChild(section);
        }
      })
      .catch(function () {});
  }

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

  // --- Investigation position (journal pages only) ---
  // Shows which patterns and convergences the current entry belongs to.
  if (relM) {
    var invNum = parseInt(relM[1], 10);
    Promise.all([
      fetch('/patterns.json').then(function (r) { return r.json(); }),
      fetch('/convergences.json').then(function (r) { return r.json(); })
    ]).then(function (results) {
      var pats = results[0];
      var convs = results[1];

      var matchedPats = pats.filter(function (p) {
        return p.entries.some(function (e) { return e.num === invNum; });
      });
      var matchedConvs = convs.filter(function (c) {
        return c.entries.some(function (e) { return e.num === invNum; });
      });

      if (!matchedPats.length && !matchedConvs.length) return;

      var invStyle = document.createElement('style');
      invStyle.textContent =
        '#inv-position{margin-top:2.5rem;padding-top:1.25rem;border-top:1px solid #21262d;}' +
        '.inv-label{font-size:0.7rem;text-transform:uppercase;letter-spacing:0.14em;' +
        'color:#8b949e;margin-bottom:0.8rem;}' +
        '.inv-row{padding:0.2rem 0;font-size:0.82rem;line-height:1.5;}' +
        '.inv-kind{color:#8b949e;font-size:0.68rem;text-transform:uppercase;' +
        'letter-spacing:0.1em;margin-right:0.45rem;display:inline-block;width:5.5rem;}' +
        '.inv-row a{color:#c9d1d9;text-decoration:none;}' +
        '.inv-row a:hover{color:#58a6ff;}' +
        'html[data-theme="light"] #inv-position{border-top-color:#d0d7de;}' +
        'html[data-theme="light"] .inv-label{color:#57606a;}' +
        'html[data-theme="light"] .inv-kind{color:#57606a;}' +
        'html[data-theme="light"] .inv-row a{color:#24292e;}' +
        'html[data-theme="light"] .inv-row a:hover{color:#0969da;}';
      document.head.appendChild(invStyle);

      var section = document.createElement('div');
      section.id = 'inv-position';
      var label = document.createElement('div');
      label.className = 'inv-label';
      label.textContent = 'in the investigation';
      section.appendChild(label);

      matchedPats.forEach(function (p) {
        var row = document.createElement('div');
        row.className = 'inv-row';
        var kind = document.createElement('span');
        kind.className = 'inv-kind';
        kind.textContent = 'pattern';
        var a = document.createElement('a');
        a.href = '/patterns.html#' + p.id;
        a.title = p.description || '';
        a.textContent = p.short || p.name;
        row.appendChild(kind);
        row.appendChild(a);
        section.appendChild(row);
      });

      matchedConvs.forEach(function (c) {
        var row = document.createElement('div');
        row.className = 'inv-row';
        var kind = document.createElement('span');
        kind.className = 'inv-kind';
        kind.textContent = 'convergence';
        var a = document.createElement('a');
        a.href = '/convergences.html#conv-' + c.id;
        a.title = c.shape || '';
        a.textContent = c.title;
        row.appendChild(kind);
        row.appendChild(a);
        section.appendChild(row);
      });

      document.body.appendChild(section);
    }).catch(function () {});
  }
})();
