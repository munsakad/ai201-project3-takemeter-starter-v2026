"""Execute unit 5 notebook code cells in order using this Python environment.

Usage from the repo root: .venv/Scripts/python.exe -X utf8 scripts/run_notebook.py
Preserves executed cell outputs and saves the actual trained model locally.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ.setdefault('HF_HOME', str(ROOT / '.cache/huggingface'))
os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
path = ROOT / 'takemeter.ipynb'
notebook = json.loads(path.read_text(encoding='utf-8'))
scope = {'__name__': '__main__'}
count = 0
try:
    for index, cell in enumerate(notebook['cells']):
        if index > 16:
            break
        if cell['cell_type'] != 'code':
            continue
        count += 1
        cell['execution_count'] = count
        output = io.StringIO()
        print(f'Running notebook cell {index}...', flush=True)
        try:
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                exec(compile(''.join(cell['source']), f'takemeter.ipynb:cell{index}', 'exec'), scope)
        finally:
            cell['outputs'] = [{'output_type': 'stream', 'name': 'stdout', 'text': output.getvalue().splitlines(keepends=True)}]
            print(output.getvalue(), flush=True)
    scope['trainer'].save_model(str(ROOT / 'takemeter_out/final'))
    scope['tokenizer'].save_pretrained(str(ROOT / 'takemeter_out/final'))
    print('Saved trained model and tokenizer locally in takemeter_out/final.')
finally:
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
