"""Keep installed-catalog verification stable while workers finish new files."""
import json


def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def save_installed(base, batch, translations, validation):
    data = {'batch': batch, 'translations': translations, 'validation': validation}
    write_atomic(base / 'test_patch' / batch / 'translations_snapshot.json', data)
    write_atomic(base / 'test_patch/installed_translations.json', data)


def load_catalog(base, include_ready=False):
    snapshot = base / 'test_patch/installed_translations.json'
    if snapshot.exists() and not include_ready:
        data = json.loads(snapshot.read_text(encoding='utf-8'))
        return data['translations'], {'basis': 'installed snapshot', 'batch': data['batch']}
    translations = {}
    for source in sorted((base / 'translations').glob('*_ko.json')):
        for english, korean in json.loads(source.read_text(encoding='utf-8')).items():
            assert english not in translations or translations[english] == korean, english
            translations[english] = korean
    return translations, {'basis': 'completed translation files', 'batch': None}
