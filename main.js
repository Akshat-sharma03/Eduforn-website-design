const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.primary-nav');

if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    menuButton.querySelector('.sr-only').textContent = expanded ? 'Open navigation' : 'Close navigation';
    navigation.classList.toggle('is-open', !expanded);
  });
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.querySelector('.sr-only').textContent = 'Open navigation';
      navigation.classList.remove('is-open');
    }
  });
}

document.querySelectorAll('.nav-destinations').forEach((wrapper) => {
  const toggle = wrapper.querySelector('button[aria-controls]');
  const panel = document.getElementById(toggle.getAttribute('aria-controls'));
  if (!toggle || !panel) return;
  const closePanel = () => {
    toggle.setAttribute('aria-expanded', 'false');
    panel.hidden = true;
  };
  toggle.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!isOpen));
    panel.hidden = isOpen;
  });
  panel.addEventListener('click', (event) => {
    if (event.target.closest('a')) closePanel();
  });
  document.addEventListener('click', (event) => {
    if (!wrapper.contains(event.target)) closePanel();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closePanel();
  });
});

const requestedDestination = new URLSearchParams(window.location.search).get('destination');
if (requestedDestination) {
  const destinationSelect = document.querySelector('select[name="destination"]');
  if (destinationSelect) destinationSelect.value = requestedDestination;
}

document.querySelectorAll('.local-form').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const response = form.querySelector('.form-response');
    if (response) response.textContent = 'Thanks — the form interaction works in this preview, but no enquiry was sent. The production form needs Eduforn’s approved connection.';
  });
});

const coursePrefs = new URLSearchParams(window.location.search);
if (coursePrefs.has('subject') || coursePrefs.has('level') || coursePrefs.has('intake')) {
  const response = document.querySelector('#contact .form-response');
  if (response) {
    const summary = [coursePrefs.get('subject') || 'subject undecided', coursePrefs.get('level') || 'level undecided', `intake ${coursePrefs.get('intake') || 'undecided'}`].join('; ');
    response.textContent = `Course finder preferences: ${summary}. This preview has not sent an enquiry.`;
  }
}

