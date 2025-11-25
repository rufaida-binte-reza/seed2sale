/* <app>/static/js/app.js  – optional polish, NOT a router */
(() => {
  // 1. Highlight current nav link
  const current = location.pathname;
  document.querySelectorAll('nav a').forEach(a => {
    if (a.getAttribute('href') === current) {
      a.classList.add('active');
    }
  });

  // 2. Auto CSRF token for fetch() posts
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
                 || document.cookie
                     .split('; ')
                     .find(row => row.startsWith('csrftoken='))
                     ?.split('=')[1];

  const safeMethods = ['GET', 'HEAD', 'OPTIONS', 'TRACE'];
  if (csrftoken) {
    document.addEventListener('submit', e => {
      const form = e.target;
      if (form.method && !safeMethods.includes(form.method.toUpperCase())) {
        if (!form.querySelector('[name=csrfmiddlewaretoken]')) {
          const input = document.createElement('input');
          input.type = 'hidden';
          input.name = 'csrfmiddlewaretoken';
          input.value = csrftoken;
          form.appendChild(input);
        }
      }
    });
  }

  // 3. Small utility: flash-message fade
  const flash = document.querySelector('.flash');
  if (flash) {
    setTimeout(() => flash.classList.add('fade-out'), 3000);
  }
})();