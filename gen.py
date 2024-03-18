from datetime import date
from glob import glob
import string
import random

START = date(2024, 3, 11)


def main() -> None:
    challenges = glob('challenges/*')
    delta = (date.today() - START).days % len(challenges)
    with open(f'challenges/{delta:03}') as f:
        challenge, ruby, choice1, choice2, choice3, choice4, meaning, example, example_translation = f.read().strip().split('\n')

    choice1 = f'<button class="choice" data-correct><div>{choice1}</div></button>'
    choice2 = f'<button class="choice"><div>{choice2}</div></button>'
    choice3 = f'<button class="choice"><div>{choice3}</div></button>'
    choice4 = f'<button class="choice"><div>{choice4}</div></button>'
    choices = [choice1, choice2, choice3, choice4]
    random.shuffle(choices)
    [choice1, choice2, choice3, choice4] = choices
    meaning = ''.join(meaning)

    with open('template.html') as f:
        template = f.read()
    html = string.Template(template).substitute(template, **locals())
    with open('index.html', 'w') as f:
        f.write(html)


if __name__ == '__main__':
    main()
