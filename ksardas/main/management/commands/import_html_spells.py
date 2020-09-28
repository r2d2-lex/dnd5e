"""
    Программа парсит файл полученный скриптом pdf_to_html.py и заносит заклинания в БД
"""

from django.core.management.base import BaseCommand
from main.models import Spell, CharClasses
import re



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


def parse(text):
    if 'Время накладывания:' in text or 'Дистанция:' in text or 'Компоненты:' in text or \
            'Длительность:' in text or 'Концентрация,' in text:
        text = "\r\n" + text

    if 'Мгновенная' in text or 'минуты' in text or 'минут' in text or 'раунд' in text or 'раундов' in text or \
            'часа' in text or 'часов' in text or 'час' in text or 'дней' in text or 'рассеется' in text or \
            'рассеяно' in text or ' день' in text:
        text = text + "\r\n"

    return text


def spell_filter(spell):
    line_count = 0
    spell_level = 0
    spell_school = 0
    description = ''

    sp = Spell()
    for line in spell.split('\r\n'):
        #print(line)

        if line_count == 0:
            # Поиск уровня
            spell = re.findall(r"[А-Я]{2,}", line)
            spell = ' '.join(spell)
            spell_level_search = re.search(r"\d{1}\sуровень", line)
            if spell_level_search is None:
                spell_level_search = re.search(r"Заговор", line)
                if spell_level_search is None:
                    print('Zagovor and Level not found...')
                    input("[Enter]")
                    return False
            else:
                spell_level_search = re.search(r"\d{1}", line)
                spell_level = spell_level_search[0]

            # Поиск школы(последнее слово!!!)
            line = line.rstrip()
            spell_school_search = re.findall(r"([а-я]{4,20}\.?)+$", line)

            # Поиск ритуала
            if len(spell_school_search) == 0:
                spell_school_search_ritual = re.findall(r"([а-я]{3,})\s\(ритуал\)+$", line)
                if spell_school_search_ritual:
                    spell_school = Spell.SPELL_SCHOOL_CHOICES[spell_school_search_ritual[0]]
                    sp.is_ritual = True
                else:
                    print('Ritual not found...')
                    input("[Enter]")
                    return False
            else:
                try:
                    spell_school = Spell.SPELL_SCHOOL_CHOICES[spell_school_search[0]]
                except KeyError:
                    print('Except: spell_school_search...')
                    input("[Enter]")
                    return False

            sp.name = spell
            sp.level = spell_level
            sp.school = spell_school

            print("Spell name: ", sp.name)
            print("Spell level: ", sp.level, " level")
            print("School: ", get_key(Spell.SPELL_SCHOOL_CHOICES, sp.school))
            if sp.is_ritual:
                print("Is ritual...")

        elif 'Время накладывания' in line:
            sp.cast_time = re.findall(r"Время накладывания:\s(.*)", line)[0]
            print('Cast time:', sp.cast_time)

        elif 'Дистанция' in line:
            sp.distance = re.findall(r"Дистанция:\s(.*)", line)[0]
            print('Distance:', sp.distance)

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
                    sp.components = components[0]
                    print("Components: ", sp.components)
            print("Verb:",sp.comp_is_verbal,"  Somatic:", sp.comp_is_somatic,"  Material:", sp.comp_is_material)

        elif 'Длительность' in line:
            sp.duration = re.findall(r"Длительность:\s(.*)", line)[0]
            if re.search(r"Концентрация", line):
                sp.is_concentrate = True
                print("is Concentrate...")
            print('Duration:', sp.duration)


        else:
            description += line
        line_count += 1

    sp.description = description
    print('Description: ', sp.description)
    print('___')

    sp.save()
    return True


def parse_file(html_spells_file):
    error_spells = 0
    f = open(html_spells_file, 'r')
    rows = f.read().splitlines()
    for i in range(100):
        rows.append(' ')
    print('Rows', type(rows), '  Len rows:', len(rows))
    spell = ''
    row = 0

    while row < len(rows):
        text = clean_html_tags(rows[row])
        if ' уровень,' in text or 'аговор,' in text:
            if not spell_filter(spell):
                error_spells += 1
                print('\r\nError spell...\r\n\r\n')

            spell = ''
            spell += clean_html_tags(rows[row - 1])
            spell += clean_html_tags(rows[row])
        else:
            try:
                nextstr = clean_html_tags(rows[row + 1])
            except IndexError:
                break

            if ' уровень,' in nextstr:
                pass
            elif 'аговор,' in nextstr:
                pass
            elif 'ЧАСТЬ' in nextstr:
                pass
            elif 'Page' in nextstr:
                pass
            else:
                text = parse(text)
                spell += text
        row += 1
        input()

    print('Total ERROR Spells: ', error_spells)



