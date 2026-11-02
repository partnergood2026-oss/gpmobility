"""Static search-readiness checks; does not contact or submit to search engines."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
PUBLIC = ('index', 'about', 'business', 'courier', 'driver', 'transfer')
BASE = 'https://gpmobility.kr'

class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
    def attrs(self, tag):
        return [a for t, a in self.tags if t == tag]

class SearchIndexingTests(unittest.TestCase):
    def setUp(self):
        self.docs = {n: Document((DIST / (n + '.html')).read_text()) for n in PUBLIC}
        self.urls = [BASE + ('/' if n == 'index' else '/' + n) for n in PUBLIC]
    def test_all_html_classified(self):
        self.assertEqual({p.stem for p in DIST.glob('*.html')}, set(PUBLIC) | {'404'})
    def test_public_pages_indexable(self):
        for name, doc in self.docs.items():
            with self.subTest(page=name):
                self.assertEqual([m.get('content') for m in doc.attrs('meta') if m.get('name') == 'robots'], ['index,follow'])
    def test_canonicals_and_og_urls(self):
        for (name, doc), expected in zip(self.docs.items(), self.urls):
            with self.subTest(page=name):
                self.assertEqual([a.get('href') for a in doc.attrs('link') if a.get('rel') == 'canonical'], [expected])
                self.assertEqual([a.get('content') for a in doc.attrs('meta') if a.get('property') == 'og:url'], [expected])
    def test_sitemap_exact_public_urls(self):
        root = ET.parse(DIST / 'sitemap.xml').getroot()
        self.assertEqual(root.tag, '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
        urls = [x.text for x in root.findall('{*}url/{*}loc')]
        self.assertCountEqual(urls, self.urls)
        self.assertEqual(len(urls), len(set(urls)))
    def test_robots_public_allowed_and_sitemap(self):
        robots = RobotFileParser()
        robots.parse((DIST / 'robots.txt').read_text().splitlines())
        self.assertEqual(robots.site_maps(), [BASE + '/sitemap.xml'])
        for agent in ('Googlebot', 'Yeti', '*'):
            for url in self.urls + [BASE + '/assets/logo.png', BASE + '/style.css', BASE + '/app.js']:
                with self.subTest(agent=agent, url=url):
                    self.assertTrue(robots.can_fetch(agent, url))
    def test_error_page_noindex(self):
        doc = Document((DIST / '404.html').read_text())
        self.assertEqual([m.get('content') for m in doc.attrs('meta') if m.get('name') == 'robots'], ['noindex,follow'])
        self.assertFalse(any(a.get('rel') == 'canonical' for a in doc.attrs('link')))
    def test_internal_links_use_public_canonical_paths(self):
        paths = {urlsplit(u).path for u in self.urls}
        for name, doc in self.docs.items():
            for a in doc.attrs('a'):
                href = a.get('href', '')
                if href.startswith('/'):
                    with self.subTest(page=name, href=href):
                        self.assertIn(urlsplit(href).path, paths)
    def test_local_assets_exist(self):
        for name, doc in self.docs.items():
            for tag, attrs in doc.tags:
                src = attrs.get('src') if tag in ('img', 'script') else attrs.get('href') if tag == 'link' and attrs.get('rel') in ('stylesheet', 'icon') else None
                if src and src.startswith('/'):
                    with self.subTest(page=name, src=src):
                        self.assertTrue((DIST / src.lstrip('/')).is_file())
    def test_phone_ctas_preserved(self):
        for name, doc in self.docs.items():
            phones = [a['href'] for a in doc.attrs('a') if a.get('href', '').startswith('tel:')]
            with self.subTest(page=name):
                self.assertGreaterEqual(len(phones), 4)
                self.assertEqual(set(phones), {'tel:15551103'})
    def test_no_function_or_header_override(self):
        self.assertFalse((DIST / '_worker.js').exists())
        self.assertFalse((ROOT / 'functions').exists())
        for filename in ('_headers', '_redirects'):
            self.assertFalse((DIST / filename).exists())

if __name__ == '__main__':
    unittest.main()
