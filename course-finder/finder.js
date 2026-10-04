const institutions = [
  ['Canada','Conestoga College','https://www.conestogac.on.ca/','/study-in-canada/'],['Canada','Centennial College','https://www.centennialcollege.ca/','/study-in-canada/'],['Canada','University of Northern British Columbia','https://www.unbc.ca/','/study-in-canada/'],['Canada','Langara College','https://langara.ca/','/study-in-canada/'],['Canada','Douglas College','https://www.douglascollege.ca/','/study-in-canada/'],['Canada','Durham College','https://durhamcollege.ca/','/study-in-canada/'],
  ['United States','Arizona State University','https://www.asu.edu/','/study-in-usa/'],['United States','University of Arizona','https://www.arizona.edu/','/study-in-usa/'],['United States','University of Cincinnati','https://www.uc.edu/','/study-in-usa/'],
  ['United Kingdom','Anglia Ruskin University','https://www.aru.ac.uk/','/study-in-uk/'],['United Kingdom','University of Liverpool','https://www.liverpool.ac.uk/','/study-in-uk/'],['United Kingdom','University of East London','https://www.uel.ac.uk/','/study-in-uk/'],
  ['Australia','The University of Melbourne','https://www.unimelb.edu.au/','/study-in-australia/'],['Australia','The University of Sydney','https://www.sydney.edu.au/','/study-in-australia/'],['Australia','Australian National University','https://www.anu.edu.au/','/study-in-australia/'],['Australia','The University of Queensland','https://www.uq.edu.au/','/study-in-australia/'],['Australia','UNSW Sydney','https://www.unsw.edu.au/','/study-in-australia/'],['Australia','Monash University','https://www.monash.edu/','/study-in-australia/'],
  ['Ireland','Griffith College','https://www.griffith.ie/','/study-in-ireland/'],['Ireland','Dublin Business School','https://www.dbs.ie/','/study-in-ireland/'],['Ireland','University College Dublin','https://www.ucd.ie/','/study-in-ireland/'],['Ireland','Trinity College Dublin','https://www.tcd.ie/','/study-in-ireland/'],['Ireland','University of Galway','https://www.universityofgalway.ie/','/study-in-ireland/'],
  ['New Zealand','The University of Auckland','https://www.auckland.ac.nz/','/study-in-new-zealand/'],['New Zealand','Auckland University of Technology','https://www.aut.ac.nz/','/study-in-new-zealand/'],['New Zealand','University of Canterbury','https://www.canterbury.ac.nz/','/study-in-new-zealand/'],['New Zealand','Massey University','https://www.massey.ac.nz/','/study-in-new-zealand/'],['New Zealand','University of Otago','https://www.otago.ac.nz/','/study-in-new-zealand/'],['New Zealand','Victoria University of Wellington','https://www.wgtn.ac.nz/','/study-in-new-zealand/'],
  ['Dubai','University of Dubai','https://ud.ac.ae/','/study-in-dubai/'],['Dubai','American University in Dubai','https://www.aud.edu/','/study-in-dubai/'],['Dubai','Zayed University','https://www.zu.ac.ae/','/study-in-dubai/'],['Dubai','Heriot-Watt University Dubai','https://www.hw.ac.uk/dubai/','/study-in-dubai/'],['Dubai','Middlesex University Dubai','https://www.mdx.ac.ae/','/study-in-dubai/'],
  ['Singapore','National University of Singapore','https://www.nus.edu.sg/','/study-in-singapore/'],['Singapore','Nanyang Technological University','https://www.ntu.edu.sg/','/study-in-singapore/'],['Singapore','Singapore Management University','https://www.smu.edu.sg/','/study-in-singapore/'],['Singapore','Ngee Ann Polytechnic','https://www.np.edu.sg/','/study-in-singapore/'],['Singapore','Singapore Institute of Technology','https://www.singaporetech.edu.sg/','/study-in-singapore/'],['Singapore','Singapore University of Social Sciences','https://www.suss.edu.sg/','/study-in-singapore/'],
  ['Europe','Technical University of Munich','https://www.tum.de/en/','/study-in-europe/'],['Europe','University of Bologna','https://www.unibo.it/en','/study-in-europe/'],['Europe','University of Amsterdam','https://www.uva.nl/en','/study-in-europe/'],['Europe','Sorbonne University','https://www.sorbonne-universite.fr/en','/study-in-europe/'],['Europe','University of Helsinki','https://www.helsinki.fi/en','/study-in-europe/']
];

const form = document.querySelector('#finder-form');
if (form) {
  const results = document.querySelector('#finder-results');
  const destination = form.elements.destination;
  const params = new URLSearchParams(window.location.search);
  if (params.has('destination')) destination.value = params.get('destination');

  function render() {
    const selected = destination.value;
    const matches = institutions.filter(([country]) => !selected || country === selected);
    results.replaceChildren();
    matches.forEach(([country, name, url, page]) => {
      const card = document.createElement('article');
      card.className = 'finder-card';
      const label = document.createElement('span');
      label.className = 'finder-country';
      label.textContent = country;
      const title = document.createElement('h3');
      title.textContent = name;
      const official = document.createElement('a');
      official.href = url;
      official.target = '_blank';
      official.rel = 'noopener noreferrer';
      official.textContent = 'Open official site to check courses and eligibility ↗';
      const detail = document.createElement('a');
      detail.href = page;
      detail.className = 'finder-destination-link';
      detail.textContent = `See Eduforn’s ${country} page`;
      card.append(label, title, official, detail);
      results.append(card);
    });
    document.querySelector('#results-count').textContent = `${matches.length} institution${matches.length === 1 ? '' : 's'} listed`;
    document.querySelector('#results-title').textContent = selected ? `Explore institutions in ${selected}` : 'Institutions to explore';
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const query = new URLSearchParams({
      destination: data.get('destination') || '',
      subject: data.get('subject') || '',
      level: data.get('level') || '',
      intake: data.get('intake') || ''
    });
    const cta = document.querySelector('#finder-cta');
    cta.href = `/?${query.toString()}#contact`;
    render();
    document.querySelector('#results-title').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  destination.addEventListener('change', render);
  render();
}
