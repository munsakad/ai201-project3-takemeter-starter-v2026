"""Run the notebook's actual training functions for Part 2, preserving Unit 5.

Usage: python scripts/run_testing.py --label before
       python scripts/run_testing.py --label after --max-length 256
"""
import argparse
import ast
import gc
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', choices=['before', 'after'], required=True)
    parser.add_argument('--max-length', type=int, default=128)
    args = parser.parse_args()
    if args.max_length <= 0:
        parser.error('max-length must be positive')
    os.chdir(ROOT)
    os.environ.setdefault('HF_HOME', str(ROOT / '.cache/huggingface'))
    os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
    out = ROOT / f'results_three_seeds_{args.label}.json'
    if out.exists():
        parser.error(f'{out.name} already exists; preserve this evidence before rerunning')
    notebook = json.loads((ROOT / 'takemeter.ipynb').read_text(encoding='utf-8'))
    scope = {'__name__': '__testing__'}
    # Reuse imports, constants and function definitions without executing the
    # notebook's single-run training or overwriting results.json/test_split.csv.
    for index in (2, 6, 8, 12, 14, 16):
        tree = ast.parse(''.join(notebook['cells'][index]['source']))
        if index in (12, 14, 16):
            tree.body = [node for node in tree.body if isinstance(
                node, (ast.Import, ast.ImportFrom, ast.FunctionDef))]
        exec(compile(tree, f'takemeter.ipynb:cell{index}', 'exec'), scope)
    scope['MAX_LENGTH'] = args.max_length
    results = []
    for seed in (42, 7, 2024):
        tr, va, te = scope['split_dataset'](scope['df'], seed)
        trainer, tokenizer = scope['train_model'](
            tr, va, scope['LABELS'], seed, scope['EPOCHS'],
            scope['LEARNING_RATE'], scope['BATCH_SIZE'], scope['BASE_MODEL'], quiet=True)
        result = scope['evaluate'](trainer, tokenizer, te, scope['LABELS'], seed=seed)
        result.update(device=scope['DEVICE'], device_name=scope['DEVICE_NAME'],
                      torch_version=scope['torch'].__version__, max_length=args.max_length,
                      epochs=scope['EPOCHS'], learning_rate=scope['LEARNING_RATE'],
                      batch_size=scope['BATCH_SIZE'], base_model=scope['BASE_MODEL'],
                      labels_sha256=hashlib.sha256((ROOT / 'labels.csv').read_bytes()).hexdigest(),
                      test_text_sha256=hashlib.sha256(json.dumps(te['text'].tolist(),
                          ensure_ascii=False).encode('utf-8')).hexdigest())
        results.append(result)
        # Save partial progress truthfully if a later seed fails.
        out.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
        print(f"Saved {args.label} seed {seed}: accuracy {result['accuracy']:.4f}", flush=True)
        del trainer, tokenizer
        gc.collect()


if __name__ == '__main__':
    main()
