"""Verify paired trial evidence and recompute metrics from confusion counts."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    before, after = [json.loads((ROOT / f'results_three_seeds_{label}.json').read_text())
                     for label in ('before', 'after')]
    data_hash = hashlib.sha256((ROOT / 'labels.csv').read_bytes()).hexdigest()
    for runs in (before, after):
        assert [r['seed'] for r in runs] == [42, 7, 2024], 'Incomplete or duplicate trials'
        for r in runs:
            assert r['labels_sha256'] == data_hash, 'Labels changed'
            matrix = r['confusion']
            total = sum(sum(row.values()) for row in matrix.values())
            assert total == r['n_test'] == 30
            assert abs(sum(matrix[l][l] for l in matrix) / total - r['accuracy']) < 1e-12
            for label, metrics in r['per_label'].items():
                tp = matrix[label][label]
                actual = sum(matrix[label].values())
                predicted = sum(row[label] for row in matrix.values())
                assert metrics['support'] == actual
                assert abs(metrics['f1'] - 2 * tp / (actual + predicted)) < 1e-12
    for b, a in zip(before, after):
        for key in ('seed', 'test_text_sha256', 'labels_sha256', 'epochs',
                    'learning_rate', 'batch_size', 'base_model', 'device', 'torch_version'):
            assert b[key] == a[key], f'Unexpected change: {key}'
        assert b['max_length'] == 128 and a['max_length'] == 256
    baseline = json.loads((ROOT / 'baseline_results.json').read_text())
    import csv
    with (ROOT / 'test_split.csv').open(encoding='utf-8', newline='') as f:
        posts = list(csv.DictReader(f))
    assert baseline['held_out'] and baseline['used_definitions']
    assert [(r['text'], r['gold']) for r in baseline['predictions']] == [(r['text'], r['label']) for r in posts]
    assert len(posts) == baseline['n'] == 30
    assert baseline['scores']['accuracy'] == sum(r['gold'] == r['predicted'] for r in baseline['predictions']) / 30
    print('PASS: six trials, recomputed metrics, frozen labels, paired splits, one setting change, same-post baseline')


if __name__ == '__main__':
    main()
