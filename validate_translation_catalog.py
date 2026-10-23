"""Validate merged translation sources, explicit grammar adaptations, and stat deltas."""
from pathlib import Path
import collections
import json
import re

BASE = Path(__file__).parent
TOKEN = re.compile(r"%[A-Za-z_][A-Za-z0-9_']*%|\[\d+\]|\[(?:/?[biusc]|n|[0-9a-fA-F]{6,8}|-)\]")
GRAMMAR_TOKENS = {'%HESHE%', '%HIMHER%', '%HISHER%', '%HIMSELFHERSELF%', '%VERB_IS_ARE%', '%VERB_SAYS_SAY%', '%VERB_WANTS_WANT%', '%VERB_MAKES_MAKE%', '%VERB_HATES_HATE%'}
GRAMMAR_TOKENS |= set(json.loads((BASE / 'translations/grammar_verb_tokens.json').read_text(encoding='utf-8')))
GRAMMAR_TOKENS |= set(json.loads((BASE / 'translations/grammar_gender_tokens.json').read_text(encoding='utf-8')))
STATS = {'SMARTS': '지능', 'BOLDNESS': '대담함', 'CREATIVITY': '창의력', 'CHARM': '매력', 'FUN': '재미', 'MONEY': '돈'}


def validate_catalog():
    translations, owners, per_file = {}, {}, {}
    for path in sorted((BASE / 'translations').glob('*_ko.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        per_file[path.name] = len(data)
        for english, korean in data.items():
            assert isinstance(english, str) and isinstance(korean, str) and korean.strip(), path
            assert '\ufffd' not in korean, (path, english)
            assert english not in translations or translations[english] == korean, (english, owners.get(english), path.name)
            translations[english], owners[english] = korean, path.name
    adaptations = json.loads((BASE / 'translations/grammar_adaptations.json').read_text(encoding='utf-8'))
    for english, item in adaptations.items():
        assert english in translations and item['reason']
        counts = item['omitted_tokens']
        assert counts and set(counts) <= GRAMMAR_TOKENS
        source = collections.Counter(TOKEN.findall(english))
        assert all(type(count) is int and count > 0 and source[token] == count for token, count in counts.items()), english
    stat_deltas = 0
    for english, korean in translations.items():
        expected = collections.Counter(token for token in TOKEN.findall(english) if token != '[n]')
        expected.subtract(adaptations.get(english, {}).get('omitted_tokens', {}))
        actual = collections.Counter(token for token in TOKEN.findall(korean) if token != '[n]')
        assert +expected == actual, ('token mismatch', owners[english], english, expected, actual)
        assert korean.count('[n]') + korean.count('\n') >= english.count('[n]') + english.count('\n'), english
        # Earlier UI/event batches sometimes express loss as "2 ... 감소".
        # New story batches use explicit signed deltas, which can be audited exactly.
        deltas = re.findall(r'([+-]\d+) (SMARTS|BOLDNESS|CREATIVITY|CHARM|FUN|MONEY)\b', english) if owners[english].startswith(('events_', 'story_')) else []
        for number, stat in deltas:
            name = STATS[stat]
            assert re.search(rf'(?:{name}(?:이|가|을|를)?\s*{re.escape(number)}|{re.escape(number)}\s*{name})', korean), ('stat mismatch', owners[english], english, korean)
            stat_deltas += 1
    return translations, {
        'unique_sources': len(translations),
        'source_files': per_file,
        'explicit_grammar_adaptations': len(adaptations),
        'signed_stat_deltas_checked': stat_deltas,
        'duplicate_source_consistency': 'passed',
        'placeholder_and_formatting_tokens': 'passed',
        'line_break_preservation': 'passed',
        'unicode_replacement_characters': 'none',
    }


if __name__ == '__main__':
    _, result = validate_catalog()
    (BASE / 'reports/translation_catalog_validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
