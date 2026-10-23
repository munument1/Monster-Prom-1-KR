"""Recompute localization coverage from original extraction IDs and translation files."""
from pathlib import Path
import argparse, collections, json, re

BASE = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--first-event', type=int)
    parser.add_argument('--last-event', type=int)
    args = parser.parse_args()
    translations = {}
    for source in sorted((BASE / 'translations').glob('*_ko.json')):
        for english, korean in json.loads(source.read_text(encoding='utf-8')).items():
            assert english not in translations or translations[english] == korean, english
            translations[english] = korean
    rows = [json.loads(line) for line in (BASE / 'extracted/dialogue_and_localized_text.jsonl').read_text(encoding='utf-8').splitlines()]
    path = BASE / 'reports/progress.json'
    progress = json.loads(path.read_text(encoding='utf-8'))
    events = collections.defaultdict(list)
    for row in rows:
        match = re.match(r'/Events/(\d+)/', row['field'])
        if row['file'] == 'level6' and row['path_id'] == 2888 and match:
            events[int(match[1])].append(row)
    translated = [row for row in rows if row['english'] in translations]
    remaining = [row for row in rows if row['english'] not in translations]
    complete = [index for index, entries in sorted(events.items()) if all(row['english'] in translations for row in entries)]
    progress.update(
        translation_sources=len(translations),
        localized_occurrences=len(rows),
        translated_localized_occurrences=len(translated),
        remaining_localized_occurrences=len(remaining),
        by_file=dict(collections.Counter(row['file'] for row in translated)),
        fully_translated_main_event_indices=complete,
        total_main_events_with_english_text=len(events),
        remaining_main_events=len(events) - len(complete),
        remaining_english_word_occurrences=sum(len(row['english'].split()) for row in remaining),
        completion_percent=round(100 * len(translated) / len(rows), 2),
    )
    if args.first_event is not None or args.last_event is not None:
        assert args.first_event is not None and args.last_event is not None
        indices = list(range(args.first_event, args.last_event + 1))
        assert indices and all(index in complete for index in indices)
        entries = [row for index in indices for row in events[index]]
        progress['latest_event_batch'] = {
            'event_indices': indices,
            'source_occurrences': len(entries),
            'unique_sources_in_batch': len({row['english'] for row in entries}),
            'choice_occurrences': sum(bool(row['context'].get('IsOptionScene')) for row in entries),
            'all_options_and_outcomes': 'translated',
        }
    path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: progress[key] for key in ['translation_sources', 'translated_localized_occurrences', 'remaining_localized_occurrences', 'remaining_english_word_occurrences', 'completion_percent', 'remaining_main_events', 'latest_event_batch']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
