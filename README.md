# Eduforn Website Redesign

A responsive, static redesign preview for Eduforn Overseas. It keeps the supplied Eduforn identity, adds destination and service discovery, and provides locally working browsing tools for course planning and resources.

> This is a local redesign preview. The enquiry forms do not transmit data and the project has not been connected to Eduforn's production systems. Confirm all business, staff, course and immigration details before public launch.

## Run locally

No framework, package manager, build command or server-side runtime is required. From the project root, start any static file server. For example:

```bash
python -m http.server 8765
```

Then open <http://127.0.0.1:8765/>. If Python is unavailable, any static web server that serves this folder at its root will work. The source keeps root-based routes for simple local development; the Pages packaging script rewrites them in the generated copy for repository subpaths.

## GitHub Pages deployment

This repository is a static site and does not need a framework build. The included GitHub Actions workflow packages the files and deploys them to GitHub Pages whenever `main` is updated, or when the workflow is started manually.

1. Push this repository to GitHub and confirm that `main` is the default branch.
2. In **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
3. For `Akshat-sharma03/Eduforn-website-design`, GitHub's project-site URL is `https://akshat-sharma03.github.io/Eduforn-website-design/`. The workflow derives `/Eduforn-website-design/` automatically and rewrites internal page, image, CSS, and JavaScript paths in the generated artifact. The checked-in source remains unchanged.
4. Open **Actions**, wait for **Deploy static site to GitHub Pages** to complete, and use the URL shown in the `github-pages` deployment environment.

To publish at the root of an account domain, the repository must be named `<account>.github.io` under that account. For a separately configured custom domain, set the repository Actions variable `PAGES_BASE_PATH` to `/` and configure the domain under **Settings → Pages**. Leave this variable unset for a normal project site; the workflow then derives the repository subpath. Do not put secrets in this variable.

To preview the generated artifact locally, run `python scripts/build_pages.py --base-path /Eduforn-website-design/` and serve `dist/github-pages/` as the web root. For a root-domain artifact, use `python scripts/build_pages.py --base-path /`. The build excludes local references and instructions and writes a `.nojekyll` marker for static asset publishing.

## Tech stack

- HTML5 pages, using semantic landmarks, headings, forms and navigation.
- CSS3 with shared design tokens, responsive grids, fluid sizing, tablet/mobile breakpoints and reduced-motion support. Layout rules adapt from compact 280px viewports through wide desktop displays; browser zoom and device text scaling remain available.
- Vanilla JavaScript for the mobile menu, destination and services dropdowns, local-only form feedback, course-finder filtering, and Resource Corner filters.
- No framework, package manager, or site runtime dependency. A Python standard-library script prepares the GitHub Pages artifact; GitHub Actions handles deployment.
- External media: Unsplash photography and FlagCDN country-flag images. A network connection is needed for those remote images.

## Features

- Eduforn-branded homepage with destination cards and country flags.
- Nine destination pages: Australia, Canada, Dubai, Europe, Ireland, New Zealand, Singapore, United Kingdom and United States.
- Responsive destinations and services navigation, switching to a scrollable compact menu for tablet and phone widths.
- Responsive layouts for phones, tablets, laptops and wide screens, with narrow-screen text wrapping, flexible form controls, stacked content and a scrollable mobile navigation panel.
- Services directory reflecting services described on Eduforn's public website.
- Course and institution finder with destination filters and preference capture for subject, study level and intake. Institution links point to official provider websites. The filters do not guarantee active program availability, admission eligibility or a current Eduforn partnership.
- Counsellor profile layout with clearly identified sample names and illustrative licensed stock portraits. Staff details, credentials, language skills, destination coverage and image consent require confirmation before publication.
- Student-story area reserved for verified stories shared with student consent.
- Resource Corner with 15 browsable topics, destination/intent/search filters and four first-wave full articles. Eleven topics are marked as briefs for later editorial development.
- Article author/reviewer metadata, official references and counselling calls to action.
- New Delhi counselling page using the office details published by Eduforn; call ahead to confirm appointment availability and hours.
- Homepage FAQ, footer contact links, skip links and local-only callback form feedback.

## Project tree

```text
.
├── README.md
├── .gitignore                             # Keeps synced source references and build output out of Git
├── .github/
│   └── workflows/
│       └── pages.yml                      # Builds and deploys through GitHub Pages Actions
├── scripts/
│   └── build_pages.py                     # Creates a base-path-aware Pages artifact
├── index.html                             # Homepage, destinations, trust, services entry, FAQ and contact form
├── styles.css                             # Shared design system and core responsive styles
├── enhancements.css                       # Additional page components and mobile refinements
├── main.js                                # Navigation and local-only enquiry behavior
├── assets/
│   └── eduforn-logo.webp                  # Supplied Eduforn logo
├── course-finder/
│   ├── index.html                         # Course/institution finder page
│   └── finder.js                          # Destination filtering and preference handoff
├── resource-corner/
│   ├── index.html                         # Topic directory and filters
│   ├── filters.js                         # Search, destination and intent filtering
│   └── articles/
│       ├── canada-pal-tal/index.html      # PAL/TAL guide
│       ├── canada-study-permit-after-sds/index.html
│       ├── ielts-vs-pte/index.html
│       └── university-shortlist/index.html
├── services/
│   └── index.html                         # Services overview
├── study-abroad-consultants-in-new-delhi/
│   └── index.html                         # New Delhi counselling page
├── study-in-australia/index.html
├── study-in-canada/index.html
├── study-in-dubai/index.html
├── study-in-europe/index.html
├── study-in-ireland/index.html
├── study-in-new-zealand/index.html
├── study-in-singapore/index.html
├── study-in-uk/index.html
└── study-in-usa/index.html
```

### Responsive layout notes

The shared styles use fluid containers and type sizing, then adjust navigation, grids, cards, forms, hero sections and footer columns at tablet and phone widths. The four full Resource Corner articles include the same accessible menu button as the other pages. A `prefers-reduced-motion` override respects the visitor's system setting. Validate representative pages at phone, tablet and desktop sizes before each release; device-specific browser rendering and remotely hosted Unsplash/FlagCDN media still depend on the visitor's browser and network.

The project mirror also has `sources/Eduforn Design System Showcase w logo.png`, a synced design-reference file. It is kept locally and excluded from the Git repository; the supplied production logo used by the site is in `assets/`.

## Content accuracy notes

- Institution pages and links are research starting points. Confirm course availability, current entry requirements and any Eduforn representation relationship with the institution and Eduforn.
- Counsellor names are placeholders, not staff biographies. Replace them with verified roles, qualifications, supported destinations and languages before launch.
- Student names, quotes and outcomes are not shown without verification and consent.
- Canada information links directly to current IRCC guidance. Rules can change; users should confirm their own eligibility and conditions with IRCC.
- Resource Corner has four full guides and eleven briefs. Assign an accountable author and qualified reviewer, verify claims and dates, and update each article before treating it as finished editorial content.

## Possible next upgrades

1. Replace sample counsellor profiles with verified staff details, approved photos and language/destination coverage.
2. Connect the callback form to Eduforn's approved CRM or enquiry endpoint, with consent, privacy notice, spam controls and clear success/failure states.
3. Add a maintained course catalogue or provider API so subject, level and intake filters can return verified programs and entry links.
4. Expand and review the remaining eleven articles; add editorial ownership, update reminders, destination/intent taxonomy and structured article metadata.
5. Add approved student stories with written consent and documented outcome verification.
6. Add analytics and conversion measurement with a privacy-conscious consent approach.
7. Add automated accessibility, link, responsive and performance checks; optimize and self-host approved images and fonts.
8. Pin GitHub Actions to reviewed full commit SHAs and enable automated action updates.
9. Confirm the repository name, Pages URL and any custom-domain setup before enabling deployment.

## Release readiness

Before a public launch, verify all content with Eduforn, replace placeholders, review privacy and consent language, test the complete mobile navigation and forms, check outbound links, and confirm the intended GitHub Pages base URL. The enquiry form is a local preview interaction; it does not send or store submissions. The local source and preview remain separate from the live website.
