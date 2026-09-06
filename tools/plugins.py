#!/usr/bin/env python3
"""Add the plugin repositories and install the plugins this UI expects.

Usage: plugins.py <jellyfin-url> <api-key> <plugins.json>

The API key is taken from the command line and used only against the server
you name. Nothing is written to disk.
"""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

GREEN, YELLOW, RED, OFF = '\033[32m', '\033[33m', '\033[31m', '\033[0m'


def ok(m):   print(f'  {GREEN}✓{OFF} {m}')
def warn(m): print(f'  {YELLOW}!{OFF} {m}')
def bad(m):  print(f'  {RED}✗{OFF} {m}')


def call(base, key, path, method='GET', body=None):
    url = base.rstrip('/') + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={'X-Emby-Token': key,
                                          'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw.strip() else None


def main():
    base, key, manifest = sys.argv[1], sys.argv[2], sys.argv[3]
    cfg = json.load(open(manifest, encoding='utf-8'))

    try:
        installed = {p['Name'] for p in call(base, key, '/Plugins')}
    except urllib.error.HTTPError as e:
        bad(f'cannot reach Jellyfin ({e.code}). Check the URL and API key.')
        return 1
    except Exception as e:
        bad(f'cannot reach Jellyfin: {e}')
        return 1

    # Merge our repositories into whatever is already configured, matching on
    # URL so re-running never duplicates a row and never drops the user's own.
    current = call(base, key, '/Repositories') or []
    have = {r.get('Url') for r in current}
    added = [r for r in cfg['repositories'] if r['Url'] not in have]
    if added:
        call(base, key, '/Repositories', 'POST', current + added)
        ok(f'added {len(added)} plugin repositor{"y" if len(added) == 1 else "ies"}')
    else:
        ok('plugin repositories already configured')

    want = cfg['required']
    todo = [n for n in want if n not in installed]
    if not todo:
        ok(f'all {len(want)} required plugins already installed')
        return 0

    failed = []
    for name in todo:
        try:
            call(base, key, '/Packages/Installed/' + urllib.parse.quote(name), 'POST')
            ok(f'installing {name}')
        except Exception as e:
            failed.append(name)
            warn(f'{name}: {e}')

    if failed:
        warn('install these by hand in Dashboard > Plugins > Catalogue: ' + ', '.join(failed))
    print()
    warn('restart Jellyfin to finish plugin installation, then re-run install.sh')
    return 0


if __name__ == '__main__':
    sys.exit(main())
