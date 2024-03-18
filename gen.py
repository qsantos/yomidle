from datetime import date
from glob import glob
import string
import random

from edict.ruby import ruby_from_kanji_kana

START = date(2024, 3, 11)


def gen_challenge(challenge: str, output: str):
    with open(challenge) as f:
        challenge, choice1, choice2, choice3, choice4, meaning, example, example_translation = f.read().strip().split('\n')

    # Prepare ruby
    ruby = ruby_from_kanji_kana(challenge, choice1)

    # Prepare choices
    choice1 = f'<button class="choice" data-correct><div>{choice1}</div></button>'
    choice2 = f'<button class="choice"><div>{choice2}</div></button>'
    choice3 = f'<button class="choice"><div>{choice3}</div></button>'
    choice4 = f'<button class="choice"><div>{choice4}</div></button>'
    choices = [choice1, choice2, choice3, choice4]
    random.shuffle(choices)
    [choice1, choice2, choice3, choice4] = choices

    with open('template.html') as f:
        template = f.read()
    html = string.Template(template).substitute(template, **locals())
    with open(output, 'w') as f:
        f.write(html)


def main() -> None:
    challenges = sorted(glob('challenges/*'))
    delta = (date.today() - START).days % len(challenges)
    gen_challenge(challenges[delta], 'index.html')


if __name__ == '__main__':
    main()
