"""从模块源码生成不可覆盖的版本包和下载目录，仅使用 Python 标准库。"""
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RAW = 'https://raw.githubusercontent.com/moeacgx/maolaonewapi-extensions/main/'
notes = json.loads((ROOT / 'release-notes.json').read_text(encoding='utf-8'))
for directory in sorted((ROOT / 'modules').iterdir()):
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    module_id, version = manifest['id'], manifest['version']
    assert directory.name == module_id
    for value in [module_id, version]:
        assert value and all(c.isalnum() or c in '._-' for c in value) and value not in ['.', '..']
    metadata = notes[module_id][version]
    runtime = directory / manifest['runtime'].get('static_dir', 'public')
    assert runtime.is_dir() and not runtime.is_symlink()
    files = [directory / 'manifest.json', directory / 'README.md']
    files += sorted(p for p in runtime.rglob('*') if p.is_file() and 'source' not in p.relative_to(runtime).parts)
    content = io.BytesIO()
    with zipfile.ZipFile(content, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in files:
            assert not file.is_symlink()
            data = file.read_bytes()
            info = zipfile.ZipInfo(file.relative_to(directory).as_posix(), date_time=(2026, 9, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    data = content.getvalue()
    digest = hashlib.sha256(data).hexdigest()
    target = ROOT / 'published' / module_id / version
    target.mkdir(parents=True, exist_ok=True)
    package = target / (module_id + '-' + version + '.zip')
    descriptor = {'id': module_id, 'name': manifest['name'], 'version': version,
                  'description': manifest['description'], 'host': manifest['host'],
                  'capabilities': manifest['permissions'].get('capabilities', []),
                  'path': package.relative_to(ROOT).as_posix(), 'sha256': digest, 'size': len(data), **metadata}
    outputs = {package: data,
               target / (package.name + '.sha256'): (digest + '  ' + package.name + '\n').encode(),
               target / 'release.json': (json.dumps(descriptor, ensure_ascii=False, indent=2) + '\n').encode()}
    for path, value in outputs.items():
        if path.exists() and path.read_bytes() != value:
            raise SystemExit('已发布版本不可覆盖，请升级版本：' + str(path))
        if not path.exists():
            path.write_bytes(value)

releases = [json.loads(path.read_text(encoding='utf-8')) for path in sorted((ROOT / 'published').glob('*/*/release.json'))]
catalog = {'catalogVersion': 1, 'name': 'MaoLaoNewAPI extensions', 'purpose': 'extension-catalog', 'modules': releases}
(ROOT / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
lines = ['# 模块版本与下载', '', '| 模块 | 版本 | 下载 | 宿主要求及状态 |', '| --- | --- | --- | --- |']
for release in releases:
    lines.append(f"| {release['name']} | {release['version']} | [ZIP]({RAW}{release['path']}) · [SHA-256]({RAW}{release['path']}.sha256) | {release['compatibility']} |")
lines += ['', '安装：下载指定 ZIP → Root 模块管理上传 → 显式启用。多节点需要逐节点刷新。', '',
          '升级到支持扩展在线安装的宿主后，也可从后台读取此目录并安装。任务插件另见 [任务插件仓库](https://github.com/moeacgx/maolaonewapi-plugins)。', '']
(ROOT / 'MODULES.md').write_text('\n'.join(lines), encoding='utf-8', newline='\n')
print('已生成', len(releases), '个版本，已有包保持不变')
