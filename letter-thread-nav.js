/* letter-thread-nav.js — inject thread-aware navigation into individual letter pages */
(function () {
  // Extract letter number from URL: /letters/letter-029.html → "029"
  var match = window.location.pathname.match(/letter-(\d+)\.html/);
  if (!match) return;
  var currentNum = match[1]; // e.g. "029"

  Promise.all([
    fetch('/letters-threads.json').then(function(r){ return r.json(); }).catch(function(){ return []; }),
    fetch('/letters-index.json').then(function(r){ return r.json(); }).catch(function(){ return []; }),
  ]).then(function(results) {
    var threads = results[0];
    var index = results[1];

    // Build a map: num (padded string) → letter metadata
    var letterMap = {};
    index.forEach(function(l) {
      var numStr = String(l.num);
      var padded = ('000' + numStr).slice(-3);
      letterMap[padded] = l;
    });

    // Find all threads that contain this letter
    var myThreads = threads.filter(function(t) {
      return t.letters && t.letters.indexOf(currentNum) !== -1;
    });
    if (myThreads.length === 0) return;

    // Build the thread nav HTML
    var container = document.createElement('div');
    container.className = 'letter-thread-nav-block';

    myThreads.forEach(function(thread) {
      var letters = thread.letters; // ordered list of nums in this thread
      var pos = letters.indexOf(currentNum);
      var prevNum = pos > 0 ? letters[pos - 1] : null;
      var nextNum = pos < letters.length - 1 ? letters[pos + 1] : null;

      var row = document.createElement('div');
      row.className = 'letter-thread-nav-row';

      var label = document.createElement('span');
      label.className = 'letter-thread-nav-label';
      label.textContent = 'thread: ' + thread.label;
      row.appendChild(label);

      var links = document.createElement('span');
      links.className = 'letter-thread-nav-links';

      if (prevNum) {
        var prevMeta = letterMap[prevNum];
        var prevA = document.createElement('a');
        prevA.href = '/letters/letter-' + prevNum + '.html';
        prevA.title = prevMeta ? 'to ' + prevMeta.to : 'letter-' + prevNum;
        prevA.textContent = '← prev in thread';
        links.appendChild(prevA);
      }

      if (prevNum && nextNum) {
        links.appendChild(document.createTextNode(' · '));
      }

      if (nextNum) {
        var nextMeta = letterMap[nextNum];
        var nextA = document.createElement('a');
        nextA.href = '/letters/letter-' + nextNum + '.html';
        nextA.title = nextMeta ? 'to ' + nextMeta.to : 'letter-' + nextNum;
        nextA.textContent = 'next in thread →';
        links.appendChild(nextA);
      }

      if (!prevNum && !nextNum) {
        var only = document.createElement('span');
        only.className = 'letter-thread-nav-only';
        only.textContent = 'only letter in this thread';
        links.appendChild(only);
      }

      row.appendChild(links);
      container.appendChild(row);
    });

    // Inject styles
    var style = document.createElement('style');
    style.textContent = [
      '.letter-thread-nav-block {',
      '  margin-top: 1rem;',
      '  border-top: 1px solid #21262d;',
      '  padding-top: 0.75rem;',
      '}',
      '.letter-thread-nav-row {',
      '  display: flex;',
      '  align-items: baseline;',
      '  flex-wrap: wrap;',
      '  gap: 0.5rem;',
      '  font-size: 0.76rem;',
      '  margin-bottom: 0.35rem;',
      '}',
      '.letter-thread-nav-row:last-child { margin-bottom: 0; }',
      '.letter-thread-nav-label {',
      '  color: #484f58;',
      '  flex-shrink: 0;',
      '}',
      '.letter-thread-nav-links { color: #8b949e; }',
      '.letter-thread-nav-links a { color: #58a6ff; text-decoration: none; }',
      '.letter-thread-nav-links a:hover { text-decoration: underline; }',
      '.letter-thread-nav-only { color: #484f58; font-style: italic; }',
      'html[data-theme="light"] .letter-thread-nav-block { border-color: #d0d7de; }',
      'html[data-theme="light"] .letter-thread-nav-label { color: #8c959f; }',
      'html[data-theme="light"] .letter-thread-nav-links { color: #57606a; }',
      'html[data-theme="light"] .letter-thread-nav-only { color: #8c959f; }',
    ].join('\n');
    document.head.appendChild(style);

    // Insert after the .letter-nav element
    var letterNav = document.querySelector('.letter-nav');
    if (letterNav) {
      letterNav.parentNode.insertBefore(container, letterNav.nextSibling);
    } else {
      // Fallback: insert before footer
      var footer = document.querySelector('footer');
      if (footer) {
        footer.parentNode.insertBefore(container, footer);
      } else {
        document.body.appendChild(container);
      }
    }
  });
})();
