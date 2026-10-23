"""Prepare deduplicated editable JSON jobs and import completed jobs as translations."""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import re

BASE = Path(__file__).parent
CATALOG = BASE / 'extracted/dialogue_and_localized_text.jsonl'


def catalog():
    return [json.loads(line) for line in CATALOG.read_text(encoding='utf-8').splitlines()]


def translations():
    result = {}
    for path in sorted((BASE / 'translations').glob('*_ko.json')):
        for english, korean in json.loads(path.read_text(encoding='utf-8')).items():
            assert english not in result or result[english] == korean, english
            result[english] = korean
    return result


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def prepare(args):
    done = translations()
    unique = collections.OrderedDict()
    for row in catalog():
        match = re.match(r'/Events/(\d+)/', row['field'])
        if row['file'] != 'level6' or row['path_id'] != 2888 or not match:
            continue
        index = int(match[1])
        if not args.first_event <= index <= args.last_event or row['english'] in done:
            continue
        occurrence = {
            'id': row['id'], 'event_index': index,
            'event_name': row['context'].get('EventName', ''),
            'speaker': row['context'].get('WhoSpeaksNPC', ''),
            'is_choice': bool(row['context'].get('IsOptionScene')),
        }
        if row['english'] not in unique:
            unique[row['english']] = {'english': row['english'], 'korean': '', 'occurrences': []}
        unique[row['english']]['occurrences'].append(occurrence)
    jobs, current, words = [], [], 0
    for entry in unique.values():
        size = len(entry['english'].split())
        if current and words + size > args.words:
            jobs.append((current, words))
            current, words = [], 0
        current.append(entry)
        words += size
    if current:
        jobs.append((current, words))
    folder = BASE / 'extracted' / f'work_json_{args.first_event}_{args.last_event}'
    assert not folder.exists(), f'Refusing to overwrite existing work: {folder}'
    digest = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    manifest = {'catalog_sha256': digest, 'first_event': args.first_event, 'last_event': args.last_event,
                'unique_untranslated_strings': len(unique), 'source_occurrences': sum(len(x['occurrences']) for x in unique.values()),
                'word_budget_per_job': args.words, 'jobs': []}
    for index, (entries, count) in enumerate(jobs, 1):
        job_id = f'story_{args.first_event}_{args.last_event}_{index:03d}'
        event_indices = [o['event_index'] for entry in entries for o in entry['occurrences']]
        summary = {'id': job_id, 'unique_strings': len(entries), 'english_words': count,
                   'first_event': min(event_indices), 'last_event': max(event_indices)}
        write_json(folder / f'{job_id}.json', {'schema_version': 1, 'target_language': 'ko',
                   'catalog_sha256': digest, 'summary': summary, 'entries': entries})
        manifest['jobs'].append(summary)
    write_json(folder / 'manifest.json', manifest)
    # Public summary contains counts only; untranslated game text stays local.
    write_json(BASE / 'reports/translation_queue.json', manifest)
    print(json.dumps({'folder': str(folder.resolve()), 'jobs': len(jobs),
          'unique_untranslated_strings': len(unique), 'source_occurrences': manifest['source_occurrences']}, indent=2))


def import_job(args):
    job = json.loads(Path(args.path).read_text(encoding='utf-8'))
    assert job['schema_version'] == 1 and job['target_language'] == 'ko'
    assert job['catalog_sha256'] == hashlib.sha256(CATALOG.read_bytes()).hexdigest(), 'Extraction changed'
    name = job['summary']['id']
    assert re.fullmatch(r'story_[0-9_]+', name)
    destination = BASE / 'translations' / f'{name}_ko.json'
    assert not destination.exists(), f'Refusing to overwrite {destination}'
    originals = {row['id']: row for row in catalog()}
    existing, result = translations(), {}
    assert len(job['entries']) == job['summary']['unique_strings'], 'Job entry count changed'
    for entry in job['entries']:
        english, korean = entry['english'], entry['korean']
        assert isinstance(korean, str) and korean.strip(), f'Untranslated: {english}'
        assert entry['occurrences']
        for occurrence in entry['occurrences']:
            assert originals[occurrence['id']]['english'] == english, occurrence['id']
        assert english not in result or result[english] == korean
        assert english not in existing or existing[english] == korean, f'Existing translation conflict: {english}'
        result[english] = korean
    # This command imports data only. The normal validator gates game injection.
    write_json(destination, result)
    print(f'Imported {len(result)} unique strings to {destination}')


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='action', required=True)
    prepare_parser = sub.add_parser('prepare')
    prepare_parser.add_argument('--first-event', type=int, required=True)
    prepare_parser.add_argument('--last-event', type=int, default=976)
    prepare_parser.add_argument('--words', type=int, default=9000)
    import_parser = sub.add_parser('import')
    import_parser.add_argument('path')
    args = parser.parse_args()
    if args.action == 'prepare':
        assert 0 <= args.first_event <= args.last_event and args.words > 0
        prepare(args)
    else:
        import_job(args)


if __name__ == '__main__':
    main()
