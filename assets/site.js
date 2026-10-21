/* Native links/details work without JavaScript; enhance navigation and printing. */
(function () {
  'use strict';
  var header = document.querySelector('.site-header');
  var menu = document.querySelector('.nav-toggle');
  function setMenu(open) {
    if (!header || !menu) return;
    header.classList.toggle('nav-open', open);
    menu.setAttribute('aria-expanded', String(open));
    var icon = menu.querySelector('span');
    if (icon) icon.textContent = open ? '−' : '＋';
  }
  if (menu) {
    menu.addEventListener('click', function () { setMenu(menu.getAttribute('aria-expanded') !== 'true'); });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menu.focus();
      }
    });
    header.querySelectorAll('.site-nav a').forEach(function (link) {
      link.addEventListener('click', function () { setMenu(false); });
    });
  }
  var toc = document.querySelector('.toc-details');
  if (toc) {
    var desktop = window.matchMedia('(min-width: 901px)');
    function syncToc() { toc.open = desktop.matches; }
    syncToc();
    if (desktop.addEventListener) desktop.addEventListener('change', syncToc);
    else desktop.addListener(syncToc);
    toc.querySelector('summary').addEventListener('click', function (event) {
      if (desktop.matches) event.preventDefault();
    });
    toc.addEventListener('click', function (event) {
      var link = event.target.closest('a[href^="#"]');
      if (!link || desktop.matches) return;
      toc.open = false;
      var section = document.getElementById(link.hash.slice(1));
      if (section) {
        section.setAttribute('tabindex', '-1');
        section.focus({ preventScroll: true });
      }
    });
    if ('IntersectionObserver' in window) {
      var links = Array.prototype.slice.call(toc.querySelectorAll('a[href^="#"]'));
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (link) {
            if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
          });
        });
      }, { rootMargin: '-5% 0px -65% 0px', threshold: 0 });
      links.forEach(function (link) {
        var section = document.getElementById(link.hash.slice(1));
        if (section) observer.observe(section);
      });
    }
  }
  var printButton = document.querySelector('.print-button');
  if (printButton) printButton.addEventListener('click', function () { window.print(); });
  var closedFaqs = [];
  window.addEventListener('beforeprint', function () {
    closedFaqs = Array.prototype.slice.call(document.querySelectorAll('.faq-item:not([open])'));
    closedFaqs.forEach(function (item) { item.open = true; });
  });
  window.addEventListener('afterprint', function () {
    closedFaqs.forEach(function (item) { item.open = false; });
    closedFaqs = [];
  });
})();
