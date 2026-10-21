#!/usr/bin/env python3
"""Check the published static pages without a server or third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import argparse
import html
import json
import re
import struct
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://eastlooo.github.io/tadak-legal/'

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags, self.titles, self.headings, self.schemas = [], [], [], []
        self.capture = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'title' or tag in ('h1', 'h2', 'h3') or (tag == 'script' and attrs.get('type') == 'application/ld+json'):
            self.capture = [tag, '']

    def handle_data(self, data):
        if self.capture:
            self.capture[1] += data

    def handle_endtag(self, tag):
        if self.capture and tag == self.capture[0]:
            if tag == 'title':
                self.titles.append(self.capture[1])
            elif tag == 'script':
                self.schemas.append(json.loads(self.capture[1]))
            else:
                self.headings.append((tag, self.capture[1]))
            self.capture = None

    def attrs(self, tag, **match):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in match.items())]


def check():
    errors = []
    def expect(condition, message):
        if not condition:
            errors.append(message)
    paths = sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html'))
    documents = {p: Document(p.read_text()) for p in paths}
    titles, descriptions, canonicals = [], [], []
    for p, doc in documents.items():
        rel = p.relative_to(ROOT)
        prefix = str(rel) + ': '
        expect(len(doc.titles) == 1 and len(doc.titles[0]) <= 60, prefix + 'unique title ≤60 characters')
        titles += doc.titles
        expect(len(doc.attrs('h1')) == 1, prefix + 'exactly one h1')
        levels = [int(tag[1]) for tag, _ in doc.headings]
        expect(all(b <= a + 1 for a, b in zip(levels, levels[1:])), prefix + 'heading hierarchy')
        expect(doc.attrs('html', lang='en' if rel.parts[0] == 'en' else 'ko'), prefix + 'html language')
        desc = doc.attrs('meta', name='description')
        expect(len(desc) == 1 and 0 < len(desc[0].get('content', '')) <= 155, prefix + 'description ≤155 characters')
        if desc:
            descriptions.append(desc[0]['content'])
        canonical = doc.attrs('link', rel='canonical')
        expect(len(canonical) == 1, prefix + 'canonical URL')
        if canonical:
            canonicals.append(canonical[0]['href'])
        for lang in ('ko', 'en', 'x-default'):
            alternate = doc.attrs('link', rel='alternate', hreflang=lang)
            expect(len(alternate) == 1, prefix + 'hreflang ' + lang)
            if alternate:
                target = unquote(urlsplit(alternate[0]['href']).path.removeprefix('/tadak-legal/'))
                target = ROOT / (target + 'index.html' if not target or target.endswith('/') else target)
                expect(target in documents, prefix + 'hreflang target exists')
                if target in documents and canonical:
                    expect(any(a.get('href') == canonical[0]['href'] for a in documents[target].attrs('link', rel='alternate')), prefix + 'reciprocal hreflang')
        robots = doc.attrs('meta', name='robots')
        expect(robots and 'noindex' not in robots[0].get('content', '').lower(), prefix + 'indexable')
        for property in ('og:title', 'og:description', 'og:url', 'og:image', 'og:image:width', 'og:image:height', 'og:locale'):
            expect(doc.attrs('meta', property=property), prefix + property)
        for name in ('twitter:card', 'twitter:title', 'twitter:description', 'twitter:image', 'theme-color'):
            expect(doc.attrs('meta', name=name), prefix + name)
        for relname in ('icon', 'apple-touch-icon'):
            expect(doc.attrs('link', rel=relname), prefix + relname)
        graph = [node for schema in doc.schemas for node in schema.get('@graph', [])]
        for typename in ('BreadcrumbList', 'Organization', 'WebSite'):
            expect(any(node.get('@type') == typename for node in graph), prefix + typename)
        breadcrumb = next((node for node in graph if node.get('@type') == 'BreadcrumbList'), {})
        positions = [item['position'] for item in breadcrumb.get('itemListElement', [])]
        expect(positions == list(range(1, len(positions) + 1)), prefix + 'breadcrumb positions')
        ids = [attrs['id'] for _, attrs in doc.tags if 'id' in attrs]
        expect(len(ids) == len(set(ids)), prefix + 'duplicate IDs')
        for tag, attrs in doc.tags:
            for field in ('href', 'src', 'srcset'):
                if field not in attrs:
                    continue
                value = attrs[field].split()[0]
                parsed = urlsplit(value)
                if parsed.scheme or parsed.netloc:
                    continue
                target = (p.parent / unquote(parsed.path)).resolve() if parsed.path else p
                expect(target.exists(), prefix + 'missing local asset/link: ' + value)
                if parsed.fragment and target in documents:
                    targetids = [a['id'] for _, a in documents[target].tags if 'id' in a]
                    expect(unquote(parsed.fragment) in targetids, prefix + 'missing anchor: ' + value)
            if tag == 'img':
                expect('alt' in attrs and 'width' in attrs and 'height' in attrs, prefix + 'image alt and dimensions')
        if p.stem not in ('index', 'download'):
            expect(doc.attrs('details', **{'class': 'toc-details'}), prefix + 'native collapsible TOC')
            expect(doc.attrs('div', **{'class': 'summary'}), prefix + 'summary card')
        if p.stem == 'support':
            faq = next((n for n in graph if n.get('@type') == 'FAQPage'), {})
            expect(len(faq.get('mainEntity', [])) == 4, prefix + 'four FAQ questions')
            expect(len(doc.attrs('details', **{'class': 'faq-item'})) == 4, prefix + 'four visible FAQ controls')
        if p.stem == 'download':
            expect(any(n.get('@type') == 'MobileApplication' for n in graph), prefix + 'MobileApplication schema')
    for values, label in ((titles, 'titles'), (descriptions, 'descriptions'), (canonicals, 'canonicals')):
        expect(len(values) == len(set(values)), 'Duplicate ' + label)
    for filename in ('tadak-legal-og.png', 'tadak-legal-og-en.png'):
        data = (ROOT / 'assets' / filename).read_bytes()
        expect(data[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', data[16:24]) == (1200, 630), filename + ' is 1200×630 PNG')
    for filename, size in (('favicon-32.png', 32), ('favicon-64.png', 64), ('apple-touch-icon.png', 180)):
        data = (ROOT / 'assets/app' / filename).read_bytes()
        expect(struct.unpack('>II', data[16:24]) == (size, size), filename + ' dimensions')
    xml = ET.parse(ROOT / 'sitemap.xml')
    urls = xml.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    locs = [u.findtext('{http://www.sitemaps.org/schemas/sitemap/0.9}loc') for u in urls]
    expect(set(locs) == set(canonicals), 'Sitemap exactly matches all canonical pages')
    for u in urls:
        expect(u.findtext('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod') == '2026-10-21', 'Sitemap lastmod')
        expect(len(u.findall('{http://www.w3.org/1999/xhtml}link')) == 3, 'Sitemap language alternates')
    expect(BASE + 'sitemap.xml' in (ROOT / 'robots.txt').read_text(), 'robots.txt sitemap')
    shared = ROOT.parent / 'shared/brand.css'
    if shared.exists():
        expect(shared.read_bytes() == (ROOT / 'assets/brand.css').read_bytes(), 'Shared brand tokens synchronized')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f'PASS: {len(paths)} pages; unique SEO metadata, language pairs, schemas, links, anchors, images, sitemap and shared tokens.')

def compare_content(revision):
    """Check policy prose and original IDs against a known pre-redesign revision."""
    def normalize(fragment):
        text = html.unescape(re.sub('<[^>]*>', '', fragment)).replace('`', '')
        return re.sub(r'\s+', ' ', text).strip()

    failures = []
    for p in sorted(ROOT.glob('*.html')) + sorted((ROOT / 'en').glob('*.html')):
        if p.stem in ('index', 'download'):
            continue
        rel = str(p.relative_to(ROOT))
        old = subprocess.check_output(['git', 'show', revision + ':' + rel], cwd=ROOT, text=True)
        new = p.read_text()
        article = old.split('<article class="content">', 1)[1].split('</main>', 1)[0]
        oldblocks = [normalize(x) for x in re.findall(r'<(?:p|li|td|th)\b[^>]*>.*?</(?:p|li|td|th)>', article, re.S)]
        newblocks = [normalize(x) for x in re.findall(r'<(?:p|li|td|th)\b[^>]*>.*?</(?:p|li|td|th)>', new, re.S)]
        for block in oldblocks:
            if block not in newblocks:
                failures.append(rel + ': changed or removed prose: ' + block[:100])
        oldids = set(re.findall(r'\bid="([^"]+)"', old))
        newids = set(re.findall(r'\bid="([^"]+)"', new))
        if not oldids <= newids:
            failures.append(rel + ': removed original anchors')
    if failures:
        raise SystemExit('\n'.join(failures))
    print('PASS: original policy paragraphs, lists, table cells and anchors preserved against ' + revision + '.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compare-ref', help='Optional Git revision for legal prose preservation checks')
    args = parser.parse_args()
    check()
    if args.compare_ref:
        compare_content(args.compare_ref)
