"""Validate saved unit 5 artifacts without training again."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]

def read_csv(name):
    with (ROOT / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))

def main():
    rows = read_csv('labels.csv')
    assert len(rows) >= 200
    assert set(rows[0]) == {'text', 'label', 'note'}
    assert all(r['text'].strip() and r['note'].strip() for r in rows)
    assert len({r['text'] for r in rows}) == len(rows)
    counts = Counter(r['label'] for r in rows)
    assert set(counts) == {'algorithm', 'formal_language'}
    assert max(counts.values()) / len(rows) <= .70
    assert all('AI pre-labeled' in r['note'] for r in rows)
    assert not any(r['note'] == 'cold' for r in rows)
    rest, test = train_test_split(rows, test_size=.15, random_state=42,
                                 stratify=[r['label'] for r in rows])
    train, val = train_test_split(rest, test_size=.15 / .85, random_state=42,
                                 stratify=[r['label'] for r in rest])
    for a, b in [(train, val), (train, test), (val, test)]:
        assert not ({r['text'] for r in a} & {r['text'] for r in b})
    assert read_csv('test_split.csv') == test
    results = json.loads((ROOT / 'results.json').read_text(encoding='utf-8'))
    assert results['seed'] == 42 and results['n_test'] == len(test)
    assert results['device'] == 'cpu'
    confusion = results['confusion']
    correct = sum(confusion[label][label] for label in counts)
    assert abs(correct / len(test) - results['accuracy']) < 1e-12
    for label in counts:
        support = sum(r['label'] == label for r in test)
        assert results['per_label'][label]['support'] == support
        assert sum(confusion[label].values()) == support
    sources = read_csv('data/sources.csv')
    assert len(sources) == len(rows)
    assert all(source['url'] in row['note'] for source, row in zip(sources, rows))
    notebook = json.loads((ROOT / 'takemeter.ipynb').read_text(encoding='utf-8'))
    assert all(c.get('execution_count') is not None for c in notebook['cells'][:17] if c['cell_type'] == 'code')
    assert all(o['output_type'] != 'error' for c in notebook['cells'] for o in c.get('outputs', []))
    for name in ['config.json', 'model.safetensors', 'tokenizer_config.json']:
        assert (ROOT / 'takemeter_out/final' / name).is_file()
    manifest = dict(
        seed=42, base_model='distilbert-base-uncased', epochs=3,
        learning_rate=2e-5, batch_size=16, max_length=128,
        split_sizes=dict(train=len(train), validation=len(val), test=len(test)),
        dataset_counts=dict(counts), cold_annotations=0, student_review='pending',
        independent_criteria_authorship=False,
        sha256={name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in ['labels.csv', 'criteria.md', 'test_split.csv', 'results.json']})
    (ROOT / 'data/run_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print('PASS: 200 unique attributed texts, balanced labels, no exact split overlap,')
    print('saved test split matches seed 42, metrics match confusion/support,')
    print('unit 5 notebook cells executed, and trained weights exist locally.')
    print('PENDING: student-authored criteria, 20 cold labels, student pre-label review.')

if __name__ == '__main__':
    main()
