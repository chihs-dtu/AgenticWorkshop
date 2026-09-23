#!/usr/bin/env python3
"""Show safe DTU limits, or update one context value with explicit approval.

No network, model calls, credential output, server changes or global edits.
"""
import argparse
import json
from pathlib import Path
import tempfile
import os


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', choices=['gptoss', 'mistral', 'qwen36', 'qwen38'])
    parser.add_argument('--context', type=int, choices=[8192, 16384, 32768])
    parser.add_argument('--server-max', type=int, help='Organiser-confirmed running server limit, not checkpoint capacity')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    path = root / 'opencode.json'
    if path.is_symlink():
        parser.error('Refusing a symlinked configuration; ask an organiser.')
    original = path.read_bytes()
    try:
        config = json.loads(original)
        models = config['providers']['dtu']['models']
        safe = {name: {k: models[name]['limit'][k] for k in ('context', 'output')}
                for name in ('gptoss', 'mistral', 'qwen36', 'qwen38')}
        if any(type(v) is not int or v <= 0 for limits in safe.values() for v in limits.values()):
            raise ValueError('Invalid limits')
    except (ValueError, KeyError, TypeError):
        parser.error('Expected workshop v2 JSON with numeric limits; no changes made. Ask an organiser.')
    if args.context is None:
        print(json.dumps({'kind': 'project_client_budgets',
                          'server_capacity': 'NOT CHECKED: these are not live server limits',
                          'models': safe}, indent=2))
        return
    if not args.model:
        parser.error('--model is required for a change')
    old = safe[args.model]['context']
    if args.context <= safe[args.model]['output']:
        parser.error('Context must leave room for input as well as the output allowance')
    if args.context > old and (args.server_max is None or args.context > args.server_max):
        parser.error('An increase needs an organiser-confirmed --server-max at least as large as the requested budget')
    if args.context == old:
        print(f'{args.model}: unchanged at {old}')
        return
    config['providers']['dtu']['models'][args.model]['limit']['context'] = args.context
    # Parse again to confirm that this is the sole semantic change.
    checked = json.loads(json.dumps(config))
    checked['providers']['dtu']['models'][args.model]['limit']['context'] = old
    if checked != json.loads(original):
        parser.error('Unexpected change; refusing to save')
    if path.read_bytes() != original:
        parser.error('Configuration changed during the check; retry after reviewing it')
    fd, temp_name = tempfile.mkstemp(prefix='.halp-context-', dir=root)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            handle.write(json.dumps(config, indent=2) + '\n')
        os.chmod(temp_name, path.stat().st_mode & 0o777)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    print(f'{args.model}: context {old} -> {args.context}; all other settings preserved. Reopen the project in OpenCode.')


if __name__ == '__main__':
    main()
