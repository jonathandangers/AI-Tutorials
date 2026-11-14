/* Animated loop figure in Module 06. Needs GSAP, loaded just before this file. */
(function () {
  var fig = document.getElementById('wf2d');
  if (typeof gsap === 'undefined') return;
  fig.classList.remove('static');
  var svg = document.getElementById('wf-svg');
  var playBtn = document.getElementById('wf-play');
  var nextBtn = document.getElementById('wf-next');
  var nowEl = document.getElementById('wf-now');
  var chips = Array.prototype.slice.call(fig.querySelectorAll('.beats button'));
  var BEATS = [
    { h: 'Read the current state.', p: 'Open a new chat. Give it the project description, the current state, and any reference files this stage needs.' },
    { h: 'Work one stage.', p: 'Draft, critique, revise. Only this stage, only in this chat.' },
    { h: 'You approve.', p: 'Nothing leaves the chat until you would stand behind it.' },
    { h: 'Save to the home.', p: 'The approved output goes in, and the current state is updated.' },
    { h: 'Close the chat.', p: 'The home has everything worth keeping. The next stage starts in a new chat.' }
  ];
  var INTRO = { h: 'Set up once.', p: 'The project description says what you are making: goals, audience, requirements, and what done looks like. Reference files sit beside it. The plan becomes the current state.' };
  /* beat starts within one loop; the gaps are pauses between beats */
  var OFF = [0, 2.2, 4.8, 6.8, 8.7, 10.4];
  var SPEED = 0.8;
  var segs = [{ t: 0, b: -1 }], L1 = [];
  var stopAt = 0, shown = -2;
  var tl = gsap.timeline({ paused: true, onUpdate: sync });

  function pop(sel, at, from, later) {
    tl.fromTo(sel, { scale: from || 0.5, opacity: 0, transformOrigin: '50% 50%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2)', immediateRender: !later }, at);
  }
  function draw(id, head, at, dur, later) {
    tl.fromTo(id, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, ease: 'power1.inOut', immediateRender: !later }, at);
    if (head) { tl.set(head, { opacity: 0 }, at); tl.to(head, { opacity: 1, duration: 0.12 }, at + dur - 0.08); }
  }
  function lab(sel, at) { tl.fromTo(sel, { opacity: 0, y: 5 }, { opacity: 1, y: 0, duration: 0.3 }, at); }

  /* starting state */
  tl.set('#o0,#o1,#o2,#chat,#gate,#foot,#rdh,#xbh,#l1,#l2,#l2b,#l3,#l4,#l5,#l5b', { opacity: 0 }, 0);
  tl.set('#ck0,#ck1,#ck2', { scale: 0, transformOrigin: '50% 50%' }, 0);
  tl.set('#rd,#xa,#xb,#gcheck', { strokeDashoffset: 1 }, 0);
  pop('#home', 0.1, 0.85); pop('#brief', 0.6); pop('#refs', 1.1); pop('#state', 1.6);
  var LOOP0 = 3.4;

  function loop(i, at, k) {
    var first = i === 0, chipCx = 170 + 98 * i + 44, j;
    for (j = 0; j < 5; j++) { segs.push({ t: at + OFF[j] * k, b: j }); if (first) L1.push(at + OFF[j] * k); }
    if (first) L1.push(at + OFF[5] * k);
    /* 1 read */
    if (!first) tl.to('#chat', { opacity: 0, duration: 0.2 }, at - 0.2);
    tl.set('#ct0,#ct1,#ct2', { opacity: 0 }, at);
    tl.set('#ct' + i, { opacity: 1 }, at);
    tl.set('#dr0,#dr1,#dr2', { scaleX: 0, transformOrigin: '0% 50%' }, at);
    tl.set('#gcheck', { strokeDashoffset: 1 }, at);
    if (!first) tl.set('#xa,#xb', { strokeDashoffset: 1 }, at);
    if (!first) tl.set('#xbh', { opacity: 0 }, at);
    pop('#chat', at, 0.7, !first);
    draw('#rd', '#rdh', at + 0.45 * k, 0.6 * k, !first);
    if (first) lab('#l1', at + 0.6);
    tl.set('#tok', { attr: { cx: 92, cy: 143 }, opacity: 1 }, at + 0.45 * k);
    tl.to('#tok', { attr: { cx: 170, cy: 192 }, duration: 0.4 * k, ease: 'power2.inOut' }, at + 0.45 * k);
    tl.to('#tok', { attr: { cy: 316 }, duration: 0.6 * k, ease: 'power2.in' }, at + 0.85 * k);
    tl.to('#tok', { opacity: 0, duration: 0.12 }, at + 1.45 * k);
    if (first) {
      /* reference files are pulled once, quietly */
      tl.set('#tok2', { attr: { cx: 378, cy: 98 }, opacity: 0.7 }, at + 0.6);
      tl.to('#tok2', { attr: { cx: 170, cy: 192 }, duration: 0.55, ease: 'power2.inOut' }, at + 0.6);
      tl.to('#tok2', { attr: { cy: 316 }, duration: 0.55, ease: 'power2.in' }, at + 1.15);
      tl.to('#tok2', { opacity: 0, duration: 0.12 }, at + 1.7);
    }
    /* 2 work: write, strike one line back, rewrite */
    var w = at + OFF[1] * k;
    if (first) { lab('#l2', w); lab('#l2b', w + 0.05); }
    tl.fromTo('#chr', { strokeDashoffset: 0 }, { strokeDashoffset: -90, duration: 2.0 * k, ease: 'none', immediateRender: first }, w);
    tl.to('#dr0', { scaleX: 1, duration: 0.35 * k }, w + 0.1 * k);
    tl.to('#dr1', { scaleX: 1, duration: 0.35 * k }, w + 0.45 * k);
    tl.to('#dr2', { scaleX: 1, duration: 0.3 * k }, w + 0.8 * k);
    tl.to('#dr1', { scaleX: 0.25, duration: 0.25 * k, ease: 'power2.in' }, w + 1.2 * k);
    tl.to('#dr1', { scaleX: 1, duration: 0.4 * k }, w + 1.5 * k);
    /* 3 approve: the output waits at the gate */
    var a = at + OFF[2] * k;
    tl.to('#gate', { opacity: 1, duration: 0.2 }, first ? a : at);
    if (first) lab('#l3', a + 0.5);
    draw('#xa', null, a, 0.4 * k, !first);
    tl.set('#doc', { x: 302.5, y: 304, opacity: 1 }, a);
    tl.to('#doc', { y: 276, duration: 0.45 * k, ease: 'power2.out' }, a);
    tl.to('#gate', { scale: 1.3, duration: 0.2 * k, yoyo: true, repeat: 1, transformOrigin: '50% 50%' }, a + 0.7 * k);
    tl.to('#gcheck', { strokeDashoffset: 0, duration: 0.3 * k }, a + 0.9 * k);
    /* 4 save: output lands, the state gets its check */
    var s = at + OFF[3] * k;
    if (first) lab('#l4', s + 0.2);
    draw('#xb', '#xbh', s, 0.45 * k, !first);
    tl.to('#doc', { y: 196, duration: 0.45 * k, ease: 'power2.inOut' }, s);
    tl.to('#doc', { x: chipCx - 7.5, y: 133, duration: 0.35 * k, ease: 'power2.inOut' }, s + 0.45 * k);
    tl.to('#doc', { opacity: 0, duration: 0.12 }, s + 0.8 * k);
    pop('#o' + i, s + 0.75 * k);
    tl.to('#ck' + i, { scale: 1, duration: 0.3, ease: 'back.out(4)' }, s + 1.0 * k);
    tl.to('#state', { scale: 1.07, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: '50% 50%' }, s + 1.0 * k);
    /* 5 close */
    var c = at + OFF[4] * k;
    if (first) { lab('#l5', c); lab('#l5b', c + 0.05); }
    tl.to('#chat', { opacity: 0.32, scale: 0.96, duration: 0.6 * k, ease: 'power2.inOut', transformOrigin: '50% 50%' }, c + 0.15 * k);
    return at + OFF[5] * k;
  }
  var e1 = loop(0, LOOP0, 1);
  var e2 = loop(1, e1 + 0.4, 0.85);
  var e3 = loop(2, e2 + 0.4, 0.85);
  tl.to('#foot', { opacity: 1, duration: 0.4 }, e3 - 0.3);
  tl.to({}, { duration: 0.6 }, e3);
  var END = tl.duration();
  tl.timeScale(SPEED);
  var bounds = segs.map(function (g) { return g.t; }).concat([END]);

  function beatAt(x) { var b = -1; for (var i = 0; i < segs.length; i++) if (x >= segs[i].t - 0.0005) b = segs[i].b; return b; }
  function sync() {
    var x = tl.time();
    if (!tl.paused() && x >= stopAt - 0.0005) { tl.pause(); tl.time(stopAt); x = stopAt; }
    var b = beatAt(Math.max(0, x - 0.01));
    if (b !== shown) {
      shown = b;
      var d = b < 0 ? INTRO : BEATS[b];
      nowEl.innerHTML = '<strong>' + (b < 0 ? '' : '<span class="n">' + (b + 1) + '</span>') + d.h + '</strong>' + d.p;
      chips.forEach(function (c, j) { if (j === b) c.setAttribute('aria-current', 'step'); else c.removeAttribute('aria-current'); });
    }
    playBtn.textContent = !tl.paused() ? 'Pause' : (x >= END - 0.01 ? 'Replay' : 'Play');
  }
  function run(from, to) { stopAt = to; tl.pause(); tl.time(from); tl.play(); sync(); }
  function jump(to) { tl.pause(); tl.time(to - 0.001); shown = -2; sync(); }
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  playBtn.addEventListener('click', function () {
    if (!tl.paused()) { tl.pause(); sync(); }
    else run(tl.time() >= END - 0.01 ? 0 : tl.time(), END);
  });
  nextBtn.addEventListener('click', function () {
    var from = tl.time() >= END - 0.01 ? 0 : tl.time(), to = END;
    for (var i = 0; i < bounds.length; i++) if (bounds[i] > from + 0.02) { to = bounds[i]; break; }
    if (reduce) jump(to); else run(from, to);
  });
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var i = +c.getAttribute('data-step');
      if (reduce) jump(L1[i + 1]); else run(L1[i], L1[i + 1]);
    });
  });

  /* rests on the full picture; plays once when it scrolls into view */
  tl.time(END); stopAt = END; sync();
  if (!reduce && window.IntersectionObserver) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); setTimeout(function () { if (tl.paused() && tl.time() >= END - 0.01) run(0, END); }, 900); }
    }, { threshold: 0.5 });
    io.observe(svg);
  }
})();
