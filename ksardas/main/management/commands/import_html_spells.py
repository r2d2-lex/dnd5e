"""
    Программа парсит файл полученный скриптом pdf_to_html.py и заносит заклинания в БД
"""

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from main.models import Spell, CharClasses
import re

SPELL_SCHOOL = {v: k for k, v in Spell.SPELL_SCHOOL_CHOICES}
SPELL_NAME_STRING = 0
SPELL_LEVEL_STRING = 1


class Command(BaseCommand):
    help = 'Парсит файл полученный скриптом pdf_to_html.py и заносит заклинания в БД'

    def import_html_spells(self, filename):
        parse_file(filename)

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str, help='html файл с заклинаниями')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename'][0]
        print(filename)
        self.import_html_spells(filename)
        print("Import spells finish")


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def clean_html_tags(raw_html):
    clean_regexp = re.compile('<.*?>')
    return re.sub(clean_regexp, '', raw_html)


def insert_carry(text):
    """
        Вставляет переносы после или перед словами определёнными в списке
    """
    carry_before_words = (
        'Время накладывания:',
        'Дистанция:',
        'Компоненты:',
        'Длительность:',
        'Концентрация,',
    )
    for word in carry_before_words:
        if word in text:
            text = "\r\n" + text

    carry_after_words = (
        'Мгновенная',
        'минуты',
        'минут',
        'раунд',
        'раундов',
        'часа',
        'часов',
        'час',
        'дней',
        'дня',
        'рассеется',
        'рассеяно',
        ' день',
        'Особая',
    )
    for word in carry_after_words:
        if word in text:
            text = text + "\r\n"
    return text


def spell_filter(spell_strings):
    """
        Парсит строку с опсиманием заклинания. 1 строка - имя заклинания, 2 строка - уровень заклинания
        В случае успеха сохраняет заклинание в БД и возвращает True.
    :param spell_strings:
    :return: True if success else False
    """
    line_index = 0
    spell_level = 0
    spell_school = 0
    description = ''

    sp = Spell()
    for line in spell_strings.split('\r\n'):

        if line_index == SPELL_NAME_STRING:
            try:
                spell = re.findall(r"[А-Я]+.*(?<![ \t])", line)[0]
            except IndexError:
                print('Не найдено имя заклинания...')
                input()
                return False
            sp.name = spell
            print('Имя заклинания: ', spell)

            # if line.isupper():
            #     line = line.strip()
            #     sp.name = line
            #     print("Имя заклинания: ", sp.name)
            # else:
            #     return False

        elif line_index == SPELL_LEVEL_STRING:
            spell_level_search = re.search(r"\d\sуровень", line)
            if spell_level_search is None:
                spell_level_search = re.search(r"Заговор", line)
                if spell_level_search is None:
                    print('Заговор и уровень на найдены...')
                    input()
                    return False
            else:
                spell_level_search = re.search(r"\d", line)
                try:
                    spell_level = spell_level_search[0]
                except IndexError:
                    print('Уровень заклинания не найден')
                    input()

            # Поиск школы(последнее слово!!!)
            line = line.rstrip()
            spell_school_search = re.findall(r"([а-я]{4,20}\.?)+$", line)

            # Поиск ритуала
            if len(spell_school_search) == 0:
                spell_school_search_ritual = re.findall(r"([а-я]{3,})\s\(ритуал\)+$", line)
                if spell_school_search_ritual:
                    try:
                        spell_school = SPELL_SCHOOL[spell_school_search_ritual[0]]
                    except IndexError:
                        print('Школа заклинания не найдена')
                        input()
                    sp.is_ritual = True
                else:
                    print('Ритуал не найден...')
                    input("[Enter]")
                    return False
            else:
                try:
                    # int
                    spell_school = SPELL_SCHOOL[spell_school_search[0]]
                except KeyError:
                    print('Школа заклинания не найдена...')
                    input("[Enter]")
                    return False

            sp.level = spell_level
            sp.school = spell_school

            print(r'Уровень заклинания: {}'.format(sp.level))
            print("Школа: ", get_key(SPELL_SCHOOL, sp.school))
            if sp.is_ritual:
                print("Можно использовать как ритуал...")

        elif 'Время накладывания' in line:
            try:
                sp.cast_time = re.findall(r"Время накладывания:\s(.*)", line)[0]
            except IndexError:
                print('Время накладывания не найдено')
                input()
            print('Время накладывания:', sp.cast_time)

        elif 'Дистанция' in line:
            try:
                sp.distance = re.findall(r"Дистанция:\s(.*)", line)[0]
            except IndexError:
                print('Дистанция не найдена')
                input()
            print('Дистанция:', sp.distance)

        elif 'Компоненты' in line:
            comp_is_verbal = re.search(r"В", line)
            if comp_is_verbal: sp.comp_is_verbal = True
            comp_is_somatic = re.search(r"С", line)
            if comp_is_somatic: sp.comp_is_somatic = True
            comp_is_material = re.search(r"М", line)
            if comp_is_material:
                sp.comp_is_material = True
                components = re.findall(r"\((.*)\)", line)
                if components:
                    try:
                        sp.components = components[0]
                    except IndexError:
                        print('Компоненты не найдены...')
                        input()
                    print("Компоненты: ", sp.components)
            print("Вербальный:", sp.comp_is_verbal, "  Соматический:", sp.comp_is_somatic, "  Материальный:", sp.comp_is_material)

        elif 'Длительность' in line:
            try:
                sp.duration = re.findall(r"Длительность:\s+(.*)", line)[0]
            except IndexError:
                print('Не найдена длительность заклинания')
                input()

            if re.search(r"Концентрация", line):
                sp.is_concentrate = True
                print("Требуется концентрация...")
            print('Длительность:', sp.duration)

        else:
            description += line
        line_index += 1

    sp.description = description.strip()
    print('Описание: ', sp.description)

    try:
        pass
        # sp.save()
    except IntegrityError:
        print('Заклинание {} уже в БД'.format(sp.name))
    print('___\r\n')
    return True


def parse_file(html_spells_file):

    def skip_words():
        SKIP_WORDS = ('Page', 'ЧАСТЬ',)
        nonlocal text
        for word in SKIP_WORDS:
            if word in text:
                return True
        return False

    # Есть ли заклинание
    def check_spell_contains():
        nonlocal error_spells
        nonlocal spell
        if not spell_filter(spell):
            error_spells += 1

    error_spells = 0
    with open(html_spells_file, 'r') as file_descriptor:
        strings = file_descriptor.read().splitlines()

    print('Количество строк: ', len(strings))
    spell = ''
    string_index = 0

    while string_index < len(strings):
        try:
            text = clean_html_tags(strings[string_index])
        except IndexError:
            break

        # 'Уровень' или 'Заговор' - строка тригер перед которой стоит имя заклинания.
        # Только так желательно искать спелл...
        if ' уровень,' in text or 'аговор,' in text:
            check_spell_contains()
            try:
                spell_name = clean_html_tags(strings[string_index - 1])
            except IndexError:
                break
            if spell_name.isupper():
                spell = ''
                spell += spell_name+'\r\n'
                spell += text+'\r\n'
        elif skip_words():
            pass
        elif text.isupper():
            pass
        else:
            text = insert_carry(text)
            spell += text
        string_index += 1
    else:
        check_spell_contains()

    print('Total ERROR Spells: ', error_spells)
