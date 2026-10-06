# Eduforn Website Redesign

A responsive, static website redesign for Eduforn Overseas Pvt. Ltd. The project focuses on useful study-abroad discovery, clear service descriptions, source-backed guidance, accessible interactions and a maintainable SEO foundation. It is a testing preview; it is not connected to Eduforn’s production systems.

## Run locally

The source site uses plain HTML, CSS and JavaScript. No framework or package installation is needed. Start a static server from the project root:

```bash
python -m http.server 8765
```

Open <http://127.0.0.1:8765/>. For a GitHub Pages-shaped local preview, generate the repository-subpath artifact and serve the output directory:

```bash
GITHUB_REPOSITORY=Akshat-sharma03/Eduforn-website-design python scripts/build_pages.py
python -m http.server 8765 --directory dist/github-pages
```

On Windows PowerShell, set `$env:GITHUB_REPOSITORY='Akshat-sharma03/Eduforn-website-design'` before running the build. The build creates service and article pages, rewrites root paths for the project-site URL, and adds canonical metadata, social metadata, structured data, `robots.txt` and `sitemap.xml` when a GitHub repository or `PAGES_SITE_URL` is available.

## Deploy with GitHub Pages

The workflow in `.github/workflows/pages.yml` builds and deploys the site when `main` changes or when manually run. Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.

For `Akshat-sharma03/Eduforn-website-design`, the standard project site is <https://akshat-sharma03.github.io/Eduforn-website-design/>. The workflow derives the repository path automatically. A custom domain requires configuring that domain under **Settings → Pages**, setting the Actions variable `PAGES_BASE_PATH` to `/`, and setting `PAGES_SITE_URL` to the canonical origin such as `https://www.example.com` (without a trailing slash). Do not add secrets to these variables.

The workflow does not push files back into the repository. Generated pages are produced into the deployment artifact. For local source browsing, run `scripts/generate_content_pages.py` and `scripts/wire_internal_pages.py`; the normal Pages build runs these steps automatically.

## Technology

- Semantic HTML5 pages with shared page components and accessible landmarks.
- CSS3 design tokens and responsive layouts; Poppins typography; Eduforn’s supplied logo; navy, violet, teal and soft-lavender brand palette.
- Vanilla JavaScript for the mobile navigation, destination dropdown, local-only enquiry feedback, course finder and Resource Corner filters.
- Python standard-library scripts for static page generation and GitHub Pages path-aware packaging.
- GitHub Actions and GitHub Pages for deployment; no runtime server, database or build dependency.
- Unsplash photography and FlagCDN flag imagery are loaded remotely and require a network connection.

## Features

- Mobile-responsive homepage, country destination directory and nine individual destination guides.
- Course finder with destination, subject, study level and intake filters and official institution links.
- Services overview plus eight dedicated service pages: counselling, test preparation, course and institution guidance, applications, visa guidance, pre-departure, study finance, and remittance/forex.
- Resource Corner with filters and fifteen full static guides, each with a direct answer, practical checks, official references and a counselling CTA.
- Separate About, How it Works, Student Stories, Contact, New Delhi counselling, Privacy draft and Terms draft pages.
- Student-story page intentionally has no fabricated testimonials. Placeholder counsellor names and stock photographs remain clearly marked as examples and must be replaced only with approved real details before launch.
- Homepage FAQs remain at the end of the page. SDS is described as ended November 8, 2024. Canada’s generally applicable off-campus work limit is described as up to 24 hours per week during regular academic sessions for eligible students, subject to IRCC conditions.
- Forms are preview-only: JavaScript prevents submission, and no API, CRM, email service or persistent store is connected. Do not enter sensitive data in the preview.
- Shared text styles were audited for contrast across all 44 HTML pages; destination journey sections now use dark-on-light colors, while the homepage journey section retains its light-on-dark treatment. Small supporting labels and navigation metadata on light surfaces use stronger contrast.
- GitHub Pages build generates self-canonical URLs, Open Graph/Twitter metadata, Organization/WebPage/Article JSON-LD, a sitemap and crawl rules. OAI-SearchBot is allowed for search discovery; GPTBot is separately disallowed. The deployment URL should be changed to the final canonical domain before production launch.

## SEO and AI search notes

The Pages build regenerates the authored pages, wires internal links, then creates a clean deploy snapshot under `dist/github-pages/`. It applies the GitHub Pages repository subpath to root-relative asset and navigation URLs, so nested pages continue to load when served from `/<repository>/`.

SEO work included in the build and content:

- Distinct, descriptive titles and meta descriptions, a single clear page topic, semantic page landmarks and crawlable static URLs across the homepage, destination, service, company, course-finder and article pages.
- Self-referencing canonical URLs based on the configured Pages site URL and base path, plus Open Graph and Twitter summary metadata for sharing.
- JSON-LD for the organization and each web page; article pages are identified as `Article`. This describes visible page content and is not a promise of a rich result.
- A generated XML sitemap that lists public HTML pages and excludes pages marked `noindex`; generated `robots.txt` allows general crawling and OAI-SearchBot, and separately disallows GPTBot.
- Internal links among destination guides, services, course discovery and relevant Resource Corner guides. The guides use answer-first headings, practical context, and primary government or institution references where applicable.
- Draft Privacy and Terms pages are marked `noindex` and left out of the sitemap pending business/legal review.
- The shared navigation and internal pages use real, dedicated routes, including for service and destination details, rather than relying on homepage-only anchors.

AI engine optimization (AEO) uses these same discoverability foundations: readable HTML, clear page purpose, concise answers, consistent organization identity, source attribution, and structured metadata that helps parsers understand page relationships. `OAI-SearchBot` is allowed so OpenAI search can discover public pages; `GPTBot` is separately disallowed. These controls do not guarantee crawling, citations, rankings or inclusion in AI answers. Keep content factual and updated, and do not present Eduforn as an immigration authority.

For Canada content, the site states that the Student Direct Stream ended on November 8, 2024, and that eligible students may generally work off campus up to 24 hours per week during regular academic sessions, subject to permit and IRCC conditions. Readers are directed to current official IRCC guidance. Immigration rules, institution offerings and eligibility can change; verify all claims against the linked primary source before publication. Before production, configure the canonical site URL and base path, verify the domain in Search Console and Bing Webmaster Tools, review redirects and contact details, and obtain approval for the Privacy and Terms pages.


## Project tree

```text
.
├── .github/workflows/pages.yml                  # GitHub Pages Actions workflow
├── assets/
│   └── eduforn-logo.webp                        # Supplied Eduforn logo
├── about/index.html                             # Company overview
├── contact/index.html                           # Contact information and local-only form preview
├── course-finder/
│   ├── index.html                                # Course and institution discovery
│   └── finder.js                                 # Finder filters and local preference handoff
├── destinations/index.html                      # Destination directory
├── how-it-works/index.html                      # Planning journey
├── privacy/index.html                            # Privacy notice draft for business review
├── resource-corner/
│   ├── index.html                                # Topic directory and filters
│   ├── filters.js                                # Destination, intent and text filters
│   └── articles/<slug>/index.html                # 15 standalone study-abroad guides
├── scripts/
│   ├── build_pages.py                            # Path-aware deploy build, SEO metadata, sitemap/robots
│   ├── generate_content_pages.py                 # Service, resource and company page generation
│   └── wire_internal_pages.py                   # Internal navigation and card URLs
├── services/
│   ├── index.html                                # Services directory
│   └── <service-slug>/index.html                 # Eight service detail pages
├── student-stories/index.html                   # Consent-first, no fabricated stories
├── study-abroad-consultants-in-new-delhi/        # New Delhi office and contact page
├── study-in-*/index.html                         # Nine destination guides
├── terms/index.html                              # Terms draft for business review
├── enhancements.css                              # Page components and mobile refinements
├── index.html                                    # Homepage, FAQs and preview enquiry form
├── main.js                                       # Shared navigation and local-only form behavior
├── styles.css                                    # Shared visual system and responsive styles
└── README.md                                     # Project setup, features and deployment notes
```

The synced design-system reference in `sources/` is intentionally excluded from the deploy artifact and must remain a read-only project input. `dist/` is generated and ignored by Git.

## Before production

Eduforn should verify service scope and fees, business contact details, staff profile names/credentials/photos, any student stories and consent, university/course information, privacy and terms drafts, canonical domain, analytics/cookies, and all immigration guidance. The preview makes no admissions, visa, funding or service-outcome guarantees.
