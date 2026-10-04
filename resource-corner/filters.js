const resourceFilters = document.querySelector('#resource-filters');
if (resourceFilters) {
  const cards = [...document.querySelectorAll('.resource-card')];
  const count = document.createElement('p');
  count.className = 'resource-result-count';
  count.setAttribute('aria-live', 'polite');
  resourceFilters.insertAdjacentElement('afterend', count);

  const destinationFor = (label) => {
    if (label.includes('CANADA')) return 'Canada';
    if (label.includes('UNITED STATES')) return 'United States';
    if (label.includes('UNITED KINGDOM')) return 'United Kingdom';
    if (label.includes('AUSTRALIA')) return 'Australia';
    if (label.includes('IRELAND')) return 'Ireland';
    if (label.includes('NEW ZEALAND')) return 'New Zealand';
    if (label.includes('DUBAI')) return 'Dubai';
    if (label.includes('SINGAPORE')) return 'Singapore';
    if (label.includes('EUROPE')) return 'Europe';
    return '';
  };
  const intentFor = (text, label) => {
    if (label.includes('ENGLISH TESTS') || /IELTS|PTE|SELT|test preparation/i.test(text)) return 'tests';
    if (/scholarship|education loan|funding/i.test(text)) return 'funding';
    if (/visa|study permit|student.?s pass|PAL\/TAL|SDS|off-campus work/i.test(text)) return 'visa';
    return 'planning';
  };
  const fullGuides = [
    { match: 'shortlist universities abroad', url: '/resource-corner/articles/university-shortlist/' },
    { match: 'ielts vs pte', url: '/resource-corner/articles/ielts-vs-pte/' },
    { match: 'study permit after sds', url: '/resource-corner/articles/canada-study-permit-after-sds/' },
    { match: 'canada pal or tal', url: '/resource-corner/articles/canada-pal-tal/' }
  ];
  const records = cards.map((card) => {
    const label = card.querySelector('.resource-card-top span')?.textContent.toUpperCase() || '';
    const text = card.textContent;
    card.dataset.destination = destinationFor(label);
    card.dataset.intent = intentFor(text, label);
    const guide = fullGuides.find((item) => text.toLowerCase().includes(item.match));
    const status = document.createElement('span');
    status.className = `resource-stage-pill${guide ? ' is-published' : ''}`;
    status.textContent = guide ? 'Full guide · official references' : 'Topic brief · full guide in progress';
    card.querySelector('.resource-card-top')?.insertAdjacentElement('afterend', status);
    if (guide) {
      const readLink = document.createElement('a');
      readLink.className = 'resource-read-link';
      readLink.href = guide.url;
      readLink.textContent = 'Read the full guide →';
      const cta = card.querySelector(':scope > a:last-of-type');
      if (cta) card.insertBefore(readLink, cta);
      else card.append(readLink);
    }
    return { card, text: text.toLowerCase() };
  });

  function filterResources() {
    const destination = resourceFilters.elements.destination.value;
    const intent = resourceFilters.elements.intent.value;
    const query = resourceFilters.elements.search.value.trim().toLowerCase();
    let visible = 0;
    records.forEach(({ card, text }) => {
      const show = (!destination || card.dataset.destination === destination) && (!intent || card.dataset.intent === intent) && (!query || text.includes(query));
      card.hidden = !show;
      if (show) visible += 1;
    });
    count.textContent = `${visible} of ${cards.length} guides shown`;
  }

  resourceFilters.addEventListener('input', filterResources);
  resourceFilters.addEventListener('change', filterResources);
  filterResources();
}
