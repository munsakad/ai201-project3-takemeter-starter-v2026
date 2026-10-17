"""Collect complete public question text and attribution; never assign labels."""
import csv
import datetime as dt
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import time
from urllib.parse import urlencode
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]

class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {'p', 'br', 'li', 'pre', 'blockquote'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in {'p', 'li', 'pre', 'blockquote'}:
            self.parts.append('\n')

    def handle_data(self, data):
        self.parts.append(data)

def main():
    posts = {}
    for tag in ['algorithms', 'formal-languages']:
        for page in [1, 2]:
            params = dict(site='cs', tagged=tag, pagesize=100, page=page,
                          sort='votes', order='desc', filter='withbody',
                          fromdate=1535760000, todate=1792195199)
            url = 'https://api.stackexchange.com/2.3/questions?' + urlencode(params)
            with urlopen(url, timeout=90) as response:
                payload = json.load(response)
            if 'error_id' in payload:
                raise RuntimeError(payload)
            for q in payload['items']:
                parser = PlainText()
                parser.feed(q['body'])
                posts[q['question_id']] = dict(
                    question_id=q['question_id'], title=html.unescape(q['title']),
                    text=html.unescape(q['title']) + '\n\n' + ''.join(parser.parts).strip(),
                    tags=q['tags'], url=q['link'],
                    author=html.unescape(q.get('owner', {}).get('display_name', 'deleted user')),
                    author_url=q.get('owner', {}).get('link', ''),
                    license=q.get('content_license', 'CC BY-SA 4.0'),
                    collected_at=dt.datetime.now(dt.timezone.utc).isoformat(),
                    body_html=q['body'])
            time.sleep(max(1, payload.get('backoff', 0)))
    target = ROOT / 'data' / 'collected_posts.json'
    target.write_text(json.dumps(list(posts.values()), indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Saved {len(posts)} complete public questions to {target}')

if __name__ == '__main__':
    main()
