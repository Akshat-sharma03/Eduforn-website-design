#!/usr/bin/env python3
"""Point site navigation and directory cards to their dedicated static pages."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROUTES = {
    "How to shortlist universities abroad: a step-by-step checklist": "university-shortlist",
    "IELTS vs PTE for studying abroad: how to choose": "ielts-vs-pte",
    "Skills for English SELT: what students should check before booking": "selt-english-test-booking",
    "Canada study permit after SDS: what changed for students?": "canada-study-permit-after-sds",
    "Canada PAL or TAL: when a study permit applicant may need one": "canada-pal-tal",
    "Can international students work in Canada while studying?": "canada-off-campus-work-hours",
    "US F-1 student visa: steps after getting accepted": "us-f1-student-visa",
    "UK Student visa checklist: documents and application basics": "uk-student-visa-checklist",
    "Australia Subclass 500 student visa: what to prepare": "australia-subclass-500",
    "New Zealand Fee Paying Student Visa: eligibility and evidence": "new-zealand-fee-paying-student-visa",
    "Ireland long-stay study visa: how to prepare your application": "ireland-long-stay-study-visa",
    "Singapore Student’s Pass: who needs one and how to apply": "singapore-students-pass",
    "Study in Dubai: student residence visa routes to understand": "study-in-dubai-student-visa",
    "Study in Europe: compare countries, courses and funding options": "study-in-europe-country-comparison",
    "Study abroad scholarships and education loans: how to research safely": "study-abroad-scholarships-education-loans",
}

SERVICES = {
    "Career and study counselling": "career-study-counselling",
    "English and language test preparation": "test-preparation",
    "Course and institution guidance": "course-institution-guidance",
    "Application support": "application-support",
    "Visa guidance": "visa-guidance",
    "Pre-departure support": "pre-departure-support",
    "Study finance guidance": "study-finance-guidance",
    "Remittance and forex": "remittance-forex",
}

SERVICE_MENU = '''<div class="services-panel" id="services-panel"><p>HOW EDUFORN CAN HELP</p><a href="/services/career-study-counselling/">Career and study counselling</a><a href="/services/test-preparation/">IELTS, PTE, SELT and language training</a><a href="/services/course-institution-guidance/">Course and institution guidance</a><a href="/services/application-support/">Application support</a><a href="/services/visa-guidance/">Visa guidance</a><a href="/services/pre-departure-support/">Pre-departure support</a><a href="/services/study-finance-guidance/">Study finance guidance</a><a href="/services/remittance-forex/">Remittance and forex</a><a class="service-panel-all" href="/services/">See all services <span aria-hidden="true">↗</span></a></div>'''

def wire_resource_cards(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    pattern = re.compile(r'<article class="resource-card".*?</article>', re.S)
    def replace(match: re.Match[str]) -> str:
        block = match.group(0)
        title_match = re.search(r"<h3>(.*?)</h3>", block, re.S)
        if not title_match:
            return block
        title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1)))
        slug = ROUTES.get(title)
        if not slug:
            return block
        block = re.sub(r'<a href="[^"]*">', f'<a href="/resource-corner/articles/{slug}/">', block, count=1)
        # Turn the card action into an explicit reading action.
        block = re.sub(r'(<a href="/resource-corner/articles/[^\"]+">).*?(<span aria-hidden="true">↗</span></a>)', r'\1Read this guide \2', block, count=1, flags=re.S)
        return block
    path.write_text(pattern.sub(replace, source), encoding="utf-8")

def wire_services(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    pattern = re.compile(r'<article class="service-card".*?</article>', re.S)
    def replace(match: re.Match[str]) -> str:
        block = match.group(0)
        title_match = re.search(r"<h3>(.*?)</h3>", block, re.S)
        title = html.unescape(re.sub(r"<[^>]+>", "", title_match.group(1))) if title_match else ""
        slug = SERVICES.get(title)
        if not slug:
            return block
        block = re.sub(r'<a href="[^"]*">', f'<a href="/services/{slug}/">', block, count=1)
        block = re.sub(r'(<a href="/services/[^\"]+">).*?(<span>↗</span></a>)', r'\1Learn about this service \2', block, count=1, flags=re.S)
        return block
    path.write_text(pattern.sub(replace, source), encoding="utf-8")

def main() -> None:
    for path in ROOT.rglob("*.html"):
        if "sources" in path.parts or "dist" in path.parts:
            continue
        source = path.read_text(encoding="utf-8")
        if path.parent.name.startswith("study-in-") and "enhancements.css" not in source:
            source = source.replace('<link rel="stylesheet" href="../styles.css">', '<link rel="stylesheet" href="../styles.css"><link rel="stylesheet" href="../enhancements.css">', 1)
        if "fonts.googleapis.com/css2?family=Poppins" not in source:
            font_links = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">'
            source = source.replace("</head>", font_links + "</head>", 1)
        source = source.replace('href="/#destinations"', 'href="/destinations/"')
        source = source.replace('href="/#contact"', 'href="/contact/"')
        source = source.replace('href="/#support"', 'href="/services/"').replace('href="#support"', 'href="/services/"')
        source = source.replace('href="/#journey"', 'href="/how-it-works/"')
        source = source.replace('href="/#stories"', 'href="/student-stories/"')
        source = source.replace('href="/resource-corner/#canada"', 'href="/resource-corner/articles/canada-study-permit-after-sds/"')
        source = source.replace('href="/resource-corner/#english-tests"', 'href="/resource-corner/articles/ielts-vs-pte/"')
        source = source.replace('href="/resource-corner/#shortlist"', 'href="/resource-corner/articles/university-shortlist/"')
        # Services dropdown: direct links replace old overview-page anchor links.
        source = source.replace('href="/services/#counselling"', 'href="/services/career-study-counselling/"')
        source = source.replace('href="/services/#test-preparation"', 'href="/services/test-preparation/"')
        source = source.replace('href="/services/#applications"', 'href="/services/application-support/"')
        source = source.replace('href="/services/#pre-departure"', 'href="/services/pre-departure-support/"')
        source = re.sub(r'<div class="services-panel" id="services-panel">.*?</div>', SERVICE_MENU, source, flags=re.S)
        path.write_text(source, encoding="utf-8")
    wire_resource_cards(ROOT / "resource-corner" / "index.html")
    wire_services(ROOT / "services" / "index.html")

    # Add dedicated pages to global navs that previously linked into homepage sections.
    for path in ROOT.rglob("*.html"):
        if "sources" in path.parts or "dist" in path.parts:
            continue
        source = path.read_text(encoding="utf-8")
        nav_match = re.search(r'<nav\b[^>]*id="primary-nav".*?</nav>', source, re.S)
        if nav_match:
            nav = nav_match.group(0)
            for label in ("New Delhi", "Our support", "How it works", "Student stories"):
                nav = re.sub(rf'<a href="[^"]+">{re.escape(label)}</a>', "", nav)
            nav_links = [
                ("/destinations/", "Destinations directory"),
                ("/about/", "About"),
                ("/contact/", "Contact"),
            ]
            missing = ''.join(f'<a href="{route}">{label}</a>' for route, label in nav_links if f'href="{route}"' not in nav)
            if missing:
                nav = nav.replace("</nav>", missing + "</nav>")
            source = source[:nav_match.start()] + nav + source[nav_match.end():]
        if "<footer" in source:
            footer = source[source.index("<footer"):]
            if "mailto:info@eduforn.com" not in footer:
                footer = re.sub(r'(<a[^>]+href="mailto:enquiry@eduforn\.com"[^>]*>.*?</a>)', r'\1<a href="mailto:info@eduforn.com">info@eduforn.com</a>', footer, count=1, flags=re.S)
            if "/privacy/" not in footer:
                footer = footer.replace('</div><div><h3>Get in touch</h3>', '<a href="/about/">About Eduforn</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy notice draft</a><a href="/terms/">Terms draft</a></div><div><h3>Get in touch</h3>', 1)
            extra_footer_links = [
                ("/how-it-works/", "How it works"),
                ("/student-stories/", "Student stories"),
                ("/study-abroad-consultants-in-new-delhi/", "New Delhi counselling"),
            ]
            for route, label in extra_footer_links:
                if f'href="{route}"' not in footer:
                    footer = footer.replace('</div><div><h3>Get in touch</h3>', f'<a href="{route}">{label}</a></div><div><h3>Get in touch</h3>', 1)
            source = source[:source.index("<footer")] + footer
        path.write_text(source, encoding="utf-8")

if __name__ == "__main__":
    main()
