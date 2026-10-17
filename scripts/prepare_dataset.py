"""Reproduce disclosed tag-assisted labels; this is not human annotation."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Excluded after assistant title/sample review: broad advice, unrelated subject,
# or a general problem merely expressed as a language rather than language theory.
EXCLUDE = {159015, 160559, 127978, 116244, 102448, 116704, 160704,
           131363, 119711, 97836, 100644}

def main():
    posts = json.loads((ROOT / 'data/collected_posts.json').read_text(encoding='utf-8'))
    selected = []
    for label in ['algorithm', 'formal_language']:
        group = [p for p in posts if p['question_id'] not in EXCLUDE
                 and ('formal-languages' in p['tags']) == (label == 'formal_language')][:100]
        if len(group) != 100:
            raise ValueError(f'Only {len(group)} questions for {label}')
        selected.extend((p, label) for p in group)
    if len({p['text'] for p, _ in selected}) != 200:
        raise ValueError('Duplicate question text')
    with (ROOT / 'labels.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'label', 'note'])
        writer.writeheader()
        for p, label in selected:
            writer.writerow(dict(text=p['text'], label=label,
                note=f"AI pre-labeled from community tags; assistant title/sample review; student review pending; source={p['url']}"))
    with (ROOT / 'data/sources.csv').open('w', newline='', encoding='utf-8') as f:
        fields = ['row', 'question_id', 'url', 'author', 'author_url', 'license', 'tags', 'collected_at']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row, (p, _) in enumerate(selected, 1):
            writer.writerow(dict(row=row, **{k: (';'.join(p[k]) if k == 'tags' else p[k]) for k in fields[1:]}))
    print('200 unique questions: algorithm=100; formal_language=100; cold=0')

if __name__ == '__main__':
    main()
