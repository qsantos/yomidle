#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import random
import re
import string
import unittest

anki_part_regex = re.compile(r'([^[ ]+)(?:\[(.*?)\])?')
START = date(2024, 3, 11)


def kanji_from_anki_furigana(s: str) -> str:
    ret = []
    for match in anki_part_regex.finditer(s):
        ret.append(match.group(1))
    return ''.join(ret)


def kana_from_anki_furigana(s: str) -> str:
    ret = []
    for match in anki_part_regex.finditer(s):
        ret.append(match.group(2) or match.group(1))
    return ''.join(ret)


def ruby_from_anki_furigana(s: str) -> str:
    ret = []
    ret.append('<ruby>')
    for match in anki_part_regex.finditer(s):
        ret.append(match.group(1))
        ret.append('<rt>')
        ret.append(match.group(2) or '')
        ret.append('</rt>')
    ret.append('</ruby>')
    return ''.join(ret)


class TestFromAnkiFurigana(unittest.TestCase):
    def test_ruby(self):
        self.assertEqual(
            ruby_from_anki_furigana('今日[きょう]の プレゼンテーション、 御[ご]苦[く]労[ろう]様[さま]でした。'),
            '<ruby>今日<rt>きょう</rt>の<rt></rt>プレゼンテーション、<rt></rt>御<rt>ご</rt>苦<rt>く</rt>労<rt>ろう</rt>様<rt>さま</rt>でした。<rt></rt></ruby>',
        )

    def test_kanji(self):
        self.assertEqual(
            kanji_from_anki_furigana('今日[きょう]の プレゼンテーション、 御[ご]苦[く]労[ろう]様[さま]でした。'),
            '今日のプレゼンテーション、御苦労様でした。',
        )

    def test_kana(self):
        self.assertEqual(
            kana_from_anki_furigana('今日[きょう]の プレゼンテーション、 御[ご]苦[く]労[ろう]様[さま]でした。'),
            'きょうのプレゼンテーション、ごくろうさまでした。',
        )


def gen_challenge(input: Path, output: Path):
    with open(input) as f:
        key, distractor1, distractor2, distractor3, meaning, example, example_translation = f.read().strip().split('\n')

    # Prepare challenge (kanji only)
    challenge = kanji_from_anki_furigana(key)

    # Prepare ruby for key
    key_ruby = ruby_from_anki_furigana(key)

    # Prepare choices
    key_kana = kana_from_anki_furigana(key)
    choice1 = f'<button class="choice" data-correct><div>{key_kana}</div></button>'
    choice2 = f'<button class="choice"><div>{distractor1}</div></button>'
    choice3 = f'<button class="choice"><div>{distractor2}</div></button>'
    choice4 = f'<button class="choice"><div>{distractor3}</div></button>'
    choices = [choice1, choice2, choice3, choice4]
    random.shuffle(choices)
    [choice1, choice2, choice3, choice4] = choices

    # Prepare ruby for example
    example = ruby_from_anki_furigana(example)

    with open('template.html') as f:
        template = f.read()
    html = string.Template(template).substitute(**locals())
    with open(output, 'w') as f:
        f.write(html)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    dest = Path('public')
    challenges = sorted(Path('challenges').glob('*'))
    if args.all:
        dest.mkdir(exist_ok=True)
        for challenge in challenges:
            output = dest / (challenge.name + '.html')
            print(output)
            gen_challenge(challenge, output)
    else:
        output = dest / 'index.html'
        print(output)
        delta = (date.today() - START).days % len(challenges)
        gen_challenge(challenges[delta], output)


if __name__ == '__main__':
    main()
