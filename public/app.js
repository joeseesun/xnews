
(function () {
  try {
    var t = localStorage.getItem('xn.theme');
    if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
  } catch (e) {}

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var themeBtn = document.getElementById('theme-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        var cur = document.documentElement.dataset.theme;
        var next;
        if (cur === 'dark') next = 'light';
        else if (cur === 'light') next = 'dark';
        else next = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark';
        document.documentElement.dataset.theme = next;
        try { localStorage.setItem('xn.theme', next); } catch (e) {}
      });
    }
    var menu = document.getElementById('menu-btn');
    var scrim = document.getElementById('scrim');
    function close() {
      document.body.classList.remove('drawer-open');
      if (menu) menu.setAttribute('aria-expanded', 'false');
    }
    if (menu) {
      menu.addEventListener('click', function () {
        var open = document.body.classList.toggle('drawer-open');
        menu.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
    if (scrim) scrim.addEventListener('click', close);
  });
})();
