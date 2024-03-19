import re
import unittest

from .furigana import match_from_kanji_kana

anki_part_regex = re.compile(r'(\S+?)(?:\[(.*?)\])?')


def ruby_from_match(match):
    """Transform a kanji-kana match into HTML <ruby> tags

    For instance, for [('牛', 'ぎゅう'), ('肉', 'にく')], it returns
    '<ruby>牛<rt>ぎゅう</rt>肉<rt>にく</rt></ruby>'.
    """
    def _():
        ruby_open = False
        last_was_kana = False
        for kanji, kana in match:
            if kanji == kana:
                yield kana
            else:
                if last_was_kana and ruby_open:
                    yield '</ruby>'
                    ruby_open = False
                if not ruby_open:
                    yield '<ruby>'
                    ruby_open = True
                yield '{}<rt>{}</rt>'.format(kanji, kana)
            last_was_kana = kanji == kana
        if ruby_open:
            yield '</ruby>'
    return ''.join(_())


def ruby_from_kanji_kana(kanji, kana):
    matches = list(match_from_kanji_kana(kanji, kana))
    return ruby_from_match(matches[0])


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
