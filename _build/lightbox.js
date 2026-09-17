// Lightbox for the plates: click to enlarge, click / Esc to close.
(function () {
  var imgs = document.querySelectorAll('figure.plate-frame img');
  if (!imgs.length) return;
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.innerHTML = '<figure class="plate-frame"><img alt=""><figcaption></figcaption></figure>';
  document.body.appendChild(box);
  var big = box.querySelector('img'), cap = box.querySelector('figcaption'), last = null;
  function open(img) {
    last = img;
    big.src = img.currentSrc || img.src;
    big.alt = img.alt;
    cap.textContent = img.alt.replace(/^Tavola naturalistica:\s*/, '').replace(/\.$/, '');
    box.classList.add('open');
    document.documentElement.style.overflow = 'hidden';
  }
  function close() {
    box.classList.remove('open');
    document.documentElement.style.overflow = '';
    if (last) last.focus();
  }
  imgs.forEach(function (img) {
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.addEventListener('click', function () { open(img); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img); }
    });
  });
  box.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && box.classList.contains('open')) close();
  });
})();
