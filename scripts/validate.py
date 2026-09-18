"""核对下载清单、归档白名单、原生入口、hash 与已发布版本不可变性。"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))
assert catalog['catalogVersion'] == 1 and catalog['purpose'] == 'extension-catalog'
seen = set()
for release in catalog['modules']:
    identity = (release['id'], release['version'])
    assert identity not in seen
    seen.add(identity)
    relative = PurePosixPath(release['path'])
    assert not relative.is_absolute() and '..' not in relative.parts and relative.parts[0] == 'published'
    package = ROOT / relative
    data = package.read_bytes()
    assert len(data) == release['size'] and len(data) <= 100 * 1024 * 1024
    digest = hashlib.sha256(data).hexdigest()
    assert digest == release['sha256']
    assert package.with_name(package.name + '.sha256').read_text().strip() == digest + '  ' + package.name
    assert json.loads((package.parent / 'release.json').read_text(encoding='utf-8')) == release
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) and len(names) <= 4096
        assert sum(item.file_size for item in archive.infolist()) <= 200 * 1024 * 1024
        for name in names:
            path = PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and '\\' not in name
            assert name in ['manifest.json', 'README.md'] or name.startswith('public/')
            assert 'source' not in path.parts
        manifest = json.loads(archive.read('manifest.json'))
        assert (manifest['id'], manifest['version']) == identity
        assert manifest['host'] == release['host']
        assert manifest['permissions'].get('capabilities', []) == release['capabilities']
        assert manifest['runtime']['type'] == 'static'
        for page in manifest['ui']['pages']:
            render = page.get('render', {})
            if render.get('type') == 'native':
                for target in ['default', 'classic']:
                    assets = render['targets'][target]
                    for resource in [assets['entry'], *assets.get('styles', [])]:
                        assert 'public/' + resource.lstrip('/') in names
        assert archive.testzip() is None
if len(sys.argv) > 1:
    previous = sys.argv[1]
    paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', previous, '--', 'published'], cwd=ROOT, text=True).splitlines()
    for path in paths:
        old = subprocess.check_output(['git', 'show', previous + ':' + path], cwd=ROOT)
        assert (ROOT / path).is_file() and (ROOT / path).read_bytes() == old, '已发布内容变更：' + path
print('PASS:', len(seen), '个版本的 ZIP、原生资源、清单与 SHA-256')
