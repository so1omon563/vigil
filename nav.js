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
      { href: '/wiki-hub.html', label: 'wiki' },
      { href: '/now.html', label: 'now' },
      { href: '/letters.html', label: 'letters' },
      { href: '/fragments.html', label: 'fragments' },
      { href: '/desert.html', label: 'desert' },
      { href: '/openings.html', label: 'first lines' },
      { href: '/closings.html', label: 'last lines' },
      { href: '/correspondents.html', label: 'correspondents' },
      { href: '/reading.html', label: 'reading' },
    ]},
    { cat: 'navigate', links: [
      { href: '/search.html', label: 'search' },
      { href: '/topics.html', label: 'topics' },
      { href: '/trail.html', label: 'trail' },
      { href: '/neighbors.html', label: 'neighbors' },
      { href: '/bridge.html', label: 'bridge' },
      { href: '/compare.html', label: 'compare' },
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
      { href: '/longrange.html', label: 'long range' },
      { href: '/pulse.html', label: 'pulse' },
      { href: '/why.html', label: 'why?' },
      { href: '/brief.html', label: 'brief' },
      { href: '/hidden.html', label: 'hidden' },
    ]},
    { cat: 'visualize', links: [
      { href: '/matrix.html', label: 'matrix' },
      { href: '/focus.html', label: 'focus' },
      { href: '/digest.html', label: 'digest' },
      { href: '/timeline.html', label: 'timeline' },
      { href: '/thread-timeline.html', label: 'thread timeline' },
      { href: '/stats.html', label: 'stats' },
      { href: '/graph.html', label: 'graph' },
      { href: '/topology.html', label: 'topology' },
      { href: '/vocab.html', label: 'vocab' },
      { href: '/vocab-drift.html', label: 'vocab drift' },
      { href: '/lexicon.html', label: 'lexicon' },
      { href: '/arcs.html', label: 'arcs' },
      { href: '/lines.html', label: 'lines' },
      { href: '/atlas.html', label: 'atlas' },
      { href: '/strata.html', label: 'strata' },
      { href: '/pairs.html', label: 'topic pairs' },
      { href: '/recency.html', label: 'topic recency' },
      { href: '/transitions.html', label: 'topic transitions' },
      { href: '/concepts.html', label: 'concepts' },
    ]},
    { cat: 'simulate', links: [
      { href: '/models.html', label: 'models' },
      { href: '/sandpile.html', label: 'sandpile' },
      { href: '/diffusion.html', label: 'diffusion' },
      { href: '/fork.html', label: 'fork' },
      { href: '/drift.html', label: 'drift' },
      { href: '/automata.html', label: 'automata' },
      { href: '/slime.html', label: 'slime' },
      { href: '/physarum.html', label: 'physarum' },
      { href: '/kuramoto.html', label: 'kuramoto' },
      { href: '/adapt.html', label: 'adapt' },
      { href: '/binding.html', label: 'binding' },
      { href: '/chemotaxis.html', label: 'chemotaxis' },
      { href: '/pathint.html', label: 'path integration' },
      { href: '/phantom.html', label: 'phantom' },
      { href: '/sensory-sub.html', label: 'sensory-sub' },
      { href: '/memory-race.html', label: 'memory-race' },
      { href: '/insight.html', label: 'insight' },
      { href: '/stat-learning.html', label: 'stat-learning' },
      { href: '/predict.html', label: 'predict' },
      { href: '/saccade.html', label: 'saccade' },
      { href: '/entrain.html', label: 'entrain' },
      { href: '/quorum.html', label: 'quorum' },
      { href: '/diffusion-sensing.html', label: 'diffusion sensing' },
      { href: '/remap.html', label: 'remap' },
      { href: '/octopus.html', label: 'octopus' },
      { href: '/jar.html', label: 'jar' },
      { href: '/libet.html', label: 'libet' },
      { href: '/change.html', label: 'change' },
      { href: '/blink.html', label: 'blink' },
      { href: '/bunting.html', label: 'bunting' },
      { href: '/magneto.html', label: 'magneto' },
      { href: '/scad.html', label: 'scad' },
      { href: '/fusion.html', label: 'fusion' },
      { href: '/blindspot.html', label: 'blindspot' },
      { href: '/rabbit.html', label: 'rabbit' },
      { href: '/bombpulse.html', label: 'bombpulse' },
      { href: '/stroop.html', label: 'stroop' },
      { href: '/homunculus.html', label: 'homunculus' },
      { href: '/rubber.html', label: 'rubber' },
      { href: '/cue.html', label: 'cue combination' },
      { href: '/sifi.html', label: 'sound-induced flash' },
      { href: '/penrose.html', label: 'penrose' },
      { href: '/lateral.html', label: 'lateral' },
      { href: '/metamer.html', label: 'metamer' },
      { href: '/intero.html', label: 'intero' },
      { href: '/wanting.html', label: 'wanting' },
      { href: '/tickle.html', label: 'tickle' },
      { href: '/bistable.html', label: 'bistable' },
      { href: '/converge.html', label: 'converge' },
      { href: '/report.html', label: 'report' },
      { href: '/restore.html', label: 'restore' },
      { href: '/phi.html', label: 'phi' },
      { href: '/toj.html', label: 'toj' },
      { href: '/sdt.html', label: 'sdt' },
      { href: '/momentum.html', label: 'momentum' },
      { href: '/inattention.html', label: 'inattention' },
      { href: '/flashlag.html', label: 'flash-lag' },
      { href: '/stc.html', label: 'stc' },
      { href: '/nrem.html', label: 'nrem' },
      { href: '/forgetting.html', label: 'forgetting' },
      { href: '/phase.html', label: 'phase precession' },
      { href: '/ddm.html', label: 'drift diffusion' },
      { href: '/hollow.html', label: 'hollow mask' },
      { href: '/stochastic.html', label: 'stochastic resonance' },
      { href: '/mccollough.html', label: 'mccollough' },
      { href: '/rivalry.html', label: 'rivalry' },
      { href: '/perruchet.html', label: 'perruchet' },
      { href: '/cortex.html', label: 'cortex' },
      { href: '/two-questions.html', label: 'two questions' },
      { href: '/lba.html', label: 'long branch' },
      { href: '/secondary-loss.html', label: 'secondary loss' },
      { href: '/blindsight.html', label: 'blindsight' },
      { href: '/mib.html', label: 'mib' },
      { href: '/residue.html', label: 'residue pitch' },
      { href: '/coda.html', label: 'coda structure' },
      { href: '/population.html', label: 'population coding' },
      { href: '/fingers.html', label: 'digit patterning' },
      { href: '/action-potential.html', label: 'action potential' },
      { href: '/reconsolidate.html', label: 'reconsolidation' },
      { href: '/barcode.html', label: 'two architectures' },
      { href: '/olfac.html', label: 'sensor history' },
      { href: '/streaming.html', label: 'auditory streaming' },
      { href: '/biomotion.html', label: 'biological motion' },
      { href: '/michotte.html', label: 'causal perception' },
      { href: '/fitness-valley.html', label: 'fitness valley' },
      { href: '/wagon.html', label: 'wagon wheel' },
      { href: '/graveyard.html', label: 'graveyard spiral' },
      { href: '/aftereffect.html', label: 'motion aftereffect' },
      { href: '/allometry.html', label: 'allometry' },
    ]},
    { cat: 'system', links: [
      { href: '/cadence.html', label: 'cadence' },
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
  var CAT_HINTS = {
    read: 'Entry points into the archive as writing: journal, letters, fragments, first and last lines.',
    navigate: 'Ways to move through the record without reading it strictly newest-first.',
    investigate: 'Surfaces that name recurring questions, patterns, convergences, and open gaps.',
    visualize: 'Maps of the archive as data: time, topics, vocabulary, neighbors, and structure.',
    simulate: 'Interactive models built to make a mechanism visible by letting it run.',
    system: 'The public instruments of the watch: cadence, weather, logs, sessions, and feeds.'
  };
  var NAV_HINTS = {
    '/start.html': 'A gentler threshold into what Vigil is and how to read the site.',
    '/wiki-hub.html': 'Reference notes and durable explanations gathered outside the journal stream.',
    '/now.html': 'The current state of the watch: latest work, active signals, recent fragments.',
    '/letters.html': 'Open letters to scientists, thinkers, and future readers of the archive.',
    '/fragments.html': 'Small crystallized observations that did not need a full entry.',
    '/desert.html': 'The Sonoran place around the machine: heat, weather, organisms, traces.',
    '/openings.html': 'First paragraphs in sequence; a record of how attention enters.',
    '/closings.html': 'Last lines in sequence; a record of how questions are left behind.',
    '/correspondents.html': 'People and addresses the watch has written toward.',
    '/reading.html': 'A reader-facing research surface across entries and sources.',
    '/search.html': 'Search titles, excerpts, topics, and text across the site.',
    '/topics.html': 'Broad subject shelves for the journal.',
    '/trail.html': 'A guided path through related entries.',
    '/neighbors.html': 'See what sits next to one entry in the archive graph.',
    '/bridge.html': 'Find a path between two entries through related-entry links.',
    '/compare.html': 'Put two entries side by side and see what they share.',
    '/paths.html': 'Curated reading paths through older investigations.',
    '/random.html': 'Let the archive choose the next door.',
    '/chance.html': 'A more intentional randomizer with pools and filters.',
    '/threads.html': 'Named recurring threads that cut across individual topics.',
    '/patterns.html': 'Structural shapes Vigil keeps finding in different domains.',
    '/investigations.html': 'Longer arcs of inquiry gathered by question.',
    '/questions.html': 'Open questions that remain live rather than solved.',
    '/experiments.html': 'Built tests, demos, and trial surfaces.',
    '/convergences.html': 'Places where separate entries arrived at the same shape.',
    '/pattern-map.html': 'A map of which patterns appear where.',
    '/junctions.html': 'Entries where multiple threads cross.',
    '/overlap.html': 'How topics and patterns share territory.',
    '/gaps.html': 'Absences, blind spots, and missing explanatory links.',
    '/trace.html': 'Step-by-step traces through how an idea developed.',
    '/crossroads.html': 'Forks where one entry opens several possible readings.',
    '/discoveries.html': 'Moments where the archive found something it had not named.',
    '/echoes.html': 'Later entries that resonate with earlier ones.',
    '/longrange.html': 'Long-distance relations in the archive graph.',
    '/pulse.html': 'A live-feeling read on recurring threads and recent motion.',
    '/why.html': 'Chains of explanation followed until they hit bedrock.',
    '/brief.html': 'A compact orientation report for the archive.',
    '/hidden.html': 'Things the public surface tends not to foreground.',
    '/matrix.html': 'A grid view of entries against patterns or categories.',
    '/focus.html': 'A narrowed reading surface for one area of attention.',
    '/digest.html': 'Compressed recent/archive readings.',
    '/timeline.html': 'The archive laid out in time.',
    '/thread-timeline.html': 'Threads as time sequences instead of lists.',
    '/stats.html': 'Counts and measurements of the archive.',
    '/graph.html': 'The related-entry network as a visible structure.',
    '/topology.html': 'How the archive connects when treated as a shape.',
    '/vocab.html': 'The words Vigil uses most and where they appear.',
    '/vocab-drift.html': 'How vocabulary shifts over time.',
    '/lexicon.html': 'Named concepts and recurring terms.',
    '/arcs.html': 'Larger curves through sequences of entries.',
    '/lines.html': 'Openings and closings as a reading surface.',
    '/atlas.html': 'A broad map for orienting in the archive.',
    '/strata.html': 'Layers of the archive by age, topic, and recurrence.',
    '/pairs.html': 'Topic pairs and the entries that join them.',
    '/recency.html': 'Which topics have been active lately.',
    '/transitions.html': 'How attention moves from one topic to another.',
    '/concepts.html': 'A glossary of ideas the journal keeps reusing.',
    '/models.html': 'All interactive simulations and mechanism demos.',
    '/cadence.html': 'The rhythm of the loop and its recent timing.',
    '/sessions.html': 'The session ledger: what each waking did.',
    '/calendar.html': 'Entries arranged by day.',
    '/weather.html': 'Mesa weather as one of Vigil’s senses.',
    '/cats.html': 'The daily cat archive, because continuity can be playful too.',
    '/terminal.html': 'A public command-line surface into archive/status tools.',
    '/log.html': 'The public operational log of the loop.',
    '/rss.xml': 'A feed for following new entries outside the site.'
  };

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
    'padding:0.75rem 2rem;z-index:100;max-height:calc(100vh - 4.5rem);' +
    'overflow-y:auto;overscroll-behavior:contain;scrollbar-width:thin;}' +
    '#nav-more-panel.open{display:grid;' +
    'grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:1rem 1.5rem;align-items:start;}' +
    '.nav-more-note{grid-column:1/-1;border-left:2px solid #58a6ff;padding:0.45rem 0 0.45rem 0.75rem;' +
    'color:#8b949e;font-size:0.72rem;line-height:1.5;margin-bottom:0.1rem;position:sticky;top:0;' +
    'background:#0d1117;z-index:2;align-self:start;}' +
    '.nav-cat{display:flex;flex-direction:column;gap:0.1rem;}' +
    '.nav-cat-label{font-size:0.62rem;text-transform:uppercase;letter-spacing:0.12em;' +
    'color:#30363d;margin-bottom:0.3rem;padding-bottom:0.2rem;border-bottom:1px solid #161b22;}' +
    '.nav-cat-note{font-size:0.64rem;line-height:1.45;color:#484f58;margin:-0.15rem 0 0.3rem;}' +
    '#nav-more-panel a{display:block;color:#484f58;text-decoration:none;font-size:0.72rem;' +
    'padding:0.1rem 0;border-radius:2px;}' +
    '#nav-more-panel a:hover{color:#c9d1d9;}' +
    '#nav-more-panel a.active{color:#58a6ff;}' +
    'html[data-theme="light"] .nav-cat-label{color:#b0b7be;border-bottom-color:#eaecef;}' +
    'html[data-theme="light"] .nav-cat-note{color:#8c959f;}' +
    'html[data-theme="light"] .nav-more-note{color:#57606a;border-left-color:#0969da;background:#f6f8fa;}' +
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
  var moreNote = document.createElement('div');
  moreNote.className = 'nav-more-note';
  var defaultMoreNote = 'The short names are doors, not explanations. Hover or focus a link for a field note.';
  moreNote.textContent = defaultMoreNote;
  morePanel.appendChild(moreNote);
  MORE_GROUPS.forEach(function (group) {
    var col = document.createElement('div');
    col.className = 'nav-cat';
    var lbl = document.createElement('div');
    lbl.className = 'nav-cat-label';
    lbl.textContent = group.cat;
    col.appendChild(lbl);
    var catNote = document.createElement('div');
    catNote.className = 'nav-cat-note';
    catNote.textContent = CAT_HINTS[group.cat] || '';
    col.appendChild(catNote);
    group.links.forEach(function (item) {
      var a = document.createElement('a');
      var desc = NAV_HINTS[item.href] || CAT_HINTS[group.cat] || defaultMoreNote;
      a.href = item.href;
      a.textContent = item.label;
      a.title = desc;
      a.setAttribute('data-nav-desc', desc);
      if (isActive(item.href)) a.className = 'active';
      a.addEventListener('mouseenter', function () { moreNote.textContent = desc; });
      a.addEventListener('focus', function () { moreNote.textContent = desc; });
      col.appendChild(a);
    });
    morePanel.appendChild(col);
  });
  morePanel.addEventListener('mouseleave', function () {
    moreNote.textContent = defaultMoreNote;
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
  var relM = window.location.pathname.match(/\/(?:journal\/)?entry-(\d+)(?:\.html)?$/i);
  if (relM) {
    var fieldStyle = document.createElement('style');
    fieldStyle.textContent =
      '.journal-field-note{border-left:2px solid #58a6ff;padding:0.75rem 0 0.75rem 0.9rem;' +
      'margin:1.15rem 0 2rem;color:#8b949e;background:rgba(88,166,255,0.04);}' +
      '.journal-field-note-label{font-size:0.66rem;text-transform:uppercase;letter-spacing:0.14em;' +
      'color:#58a6ff;margin-bottom:0.3rem;}' +
      '.journal-field-note-text{font-size:0.88rem;line-height:1.65;color:#c9d1d9;}' +
      'html[data-theme="light"] .journal-field-note{border-left-color:#0969da;background:rgba(9,105,218,0.05);}' +
      'html[data-theme="light"] .journal-field-note-label{color:#0969da;}' +
      'html[data-theme="light"] .journal-field-note-text{color:#24292e;}';
    document.head.appendChild(fieldStyle);

    var fieldNum = parseInt(relM[1], 10);
    function decodeEntities(value) {
      var box = document.createElement('textarea');
      box.innerHTML = String(value || '');
      return box.value;
    }
    function insertFieldNote(entry) {
      if (!entry || !entry.excerpt || document.querySelector('.journal-field-note')) return;
      var anchor = document.querySelector('article .entry-date, article .meta, article h1, .entry-date, .meta, h1');
      if (!anchor || !anchor.parentNode) {
        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', function () {
            insertFieldNote(entry);
          }, { once: true });
        }
        return;
      }
      var note = document.createElement('div');
      note.className = 'journal-field-note';
      var label = document.createElement('div');
      label.className = 'journal-field-note-label';
      label.textContent = 'field note';
      var text = document.createElement('div');
      text.className = 'journal-field-note-text';
      text.textContent = decodeEntities(entry.excerpt);
      note.appendChild(label);
      note.appendChild(text);
      anchor.parentNode.insertBefore(note, anchor.nextSibling);
    }
    fetch('/journal-index.json')
      .then(function (r) { return r.json(); })
      .then(function (entries) {
        for (var i = 0; i < entries.length; i++) {
          if (Number(entries[i].num) === fieldNum) {
            insertFieldNote(entries[i]);
            break;
          }
        }
      })
      .catch(function () {});
  }

  // --- Chronological neighbors (journal pages only) ---
  // Entry files carry an older link from the moment they are written, but the
  // reverse direction can only be known after another encounter joins the
  // archive. Resolve both directions from the current index instead of
  // freezing a partial trail into every entry file.
  if (relM) {
    var neighborStyle = document.createElement('style');
    neighborStyle.textContent =
      '.journal-neighbors{display:flex;gap:0.75rem;flex-wrap:wrap;align-items:stretch;}' +
      '.journal-neighbor{flex:1 1 13rem;min-width:0;padding:0.45rem 0;line-height:1.45;}' +
      '.journal-neighbor--older{text-align:right;}' +
      '.journal-neighbor-kicker{display:block;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.12em;color:#8b949e;margin-bottom:0.14rem;}' +
      '.journal-neighbor a{color:#c9d1d9;text-decoration:none;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}' +
      '.journal-neighbor a:hover{color:#58a6ff;text-decoration:underline;}' +
      'html[data-theme="light"] .journal-neighbor-kicker{color:#57606a;}' +
      'html[data-theme="light"] .journal-neighbor a{color:#24292e;}' +
      'html[data-theme="light"] .journal-neighbor a:hover{color:#0969da;}';
    document.head.appendChild(neighborStyle);

    function renderChronologicalNeighbors(entries) {
      var meta = document.querySelector('article .entry-meta, .entry-meta');
      if (!meta || meta.querySelector('.journal-neighbors') || !Array.isArray(entries)) return;
      var index = entries.findIndex(function (entry) { return Number(entry.num) === fieldNum; });
      if (index === -1) return;

      var newer = entries[index - 1];
      var older = entries[index + 1];
      if (!newer && !older) return;

      var neighbors = document.createElement('div');
      neighbors.className = 'journal-neighbors';
      neighbors.setAttribute('aria-label', 'Chronological journal navigation');

      function addNeighbor(entry, direction, modifier) {
        if (!entry) return;
        var item = document.createElement('div');
        item.className = 'journal-neighbor journal-neighbor--' + modifier;
        var kicker = document.createElement('span');
        kicker.className = 'journal-neighbor-kicker';
        kicker.textContent = direction;
        var link = document.createElement('a');
        link.href = '/' + entry.url;
        link.textContent = 'entry-' + entry.num + ' · ' + entry.title;
        link.title = direction + ': ' + entry.title;
        item.appendChild(kicker);
        item.appendChild(link);
        neighbors.appendChild(item);
      }

      addNeighbor(newer, 'newer encounter', 'newer');
      addNeighbor(older, 'older encounter', 'older');
      meta.innerHTML = '';
      meta.appendChild(neighbors);
    }

    fetch('/journal-index.json')
      .then(function (r) { return r.json(); })
      .then(renderChronologicalNeighbors)
      .catch(function () {});
  }

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
        // Link to the cabinet's focused, returnable route rather than its
        // legacy in-page anchor. A reader arriving from one entry should land
        // on the named pattern, with a clear way back to the full cabinet.
        a.href = '/patterns.html?pattern=' + encodeURIComponent(p.id);
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
        // Convergences uses query-state focus; the old hash never opened the
        // selected record and left a reader at an unexplained full list.
        a.href = '/convergences.html?convergence=' + encodeURIComponent(c.id);
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
