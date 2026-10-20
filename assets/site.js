// Phone menu toggle and copy buttons. The site works without this file.
(function () {
  var btn = document.getElementById("menu-toggle");
  var links = document.getElementById("navlinks");
  var mq = window.matchMedia("(max-width: 60rem)");
  function sync() {
    if (!links || !btn) return;
    if (mq.matches) {
      if (btn.getAttribute("aria-expanded") !== "true") links.setAttribute("data-open", "false");
    } else {
      links.setAttribute("data-open", "true");
    }
  }
  if (btn && links) {
    btn.addEventListener("click", function () {
      var open = links.getAttribute("data-open") === "true";
      links.setAttribute("data-open", open ? "false" : "true");
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      btn.textContent = open ? "Menu" : "Close";
    });
    if (mq.addEventListener) mq.addEventListener("change", sync);
    sync();
  }

  document.querySelectorAll(".copy-btn").forEach(function (b) {
    b.addEventListener("click", function () {
      var target = document.getElementById(b.getAttribute("data-copy"));
      if (!target) return;
      var text = target.innerText;
      function done(label) { var old = b.textContent; b.textContent = label; setTimeout(function () { b.textContent = old; }, 1500); }
      function fallback() {
        var r = document.createRange(); r.selectNodeContents(target);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        done("Selected");
      }
      try {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, fallback);
      } catch (e) { fallback(); }
    });
  });
})();
