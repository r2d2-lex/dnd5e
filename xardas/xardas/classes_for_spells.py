"""
    Программа парсит html файл и добовляет принадлежность класса в таблицу с заклинаниями.
"""
from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import settings as app_settings
import re
import sys
import config

sys.path.append(config.KSA_PATH)
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS, DATABASES=app_settings.DATABASES)

import django

django.setup()

from main.models import Spell, CharClasses

CHAR_CLASSES = [char_class[0] for char_class in CharClasses.CLASS_CHOICES]
SPELL_BOOK = 'char_spells.html'
ERROR_LOGFILE = 'errors.txt'


def clean_html_tags(raw_html):
    clean_regexp = re.compile('<.*?>')
    return re.sub(clean_regexp, '', raw_html)


def search_current_class(search_text):
    """
    Ищет в строке название класса. Если находит возвращает.
    :param search_text:
    :return:
    """
    for search_class in CHAR_CLASSES:
        search_text = search_text.lower()
        search_class = search_class.lower()
        if re.search(search_class, search_text):
            return search_class.title()
    return None


def db_search_spell(search_text):
    """
    Ищет заклинание в БД. Если строка найдена, то возвращает QuerySet заклинания.
    :param search_text:
    :return:
    """
    req = search_text.upper()
    req = req.strip()
    req = req.strip(':')
    print('Ищем заклинание: ', req)
    try:
        return Spell.objects.get(name=req)
    except ObjectDoesNotExist as err:
        return None


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print("usage: {0} char_spells.html".format(
                sys.argv[0]))
            sys.exit()
        parse_text(sys.argv[1])
    print('exit...')


def parse_text(spell_book):
    current_class = None
    current_class_qs = None

    with open(spell_book, 'r') as f:
        rows = f.read().splitlines()

        for row in range(len(rows)):
            print('\n\nСтрока: ', row)
            print("Текущий класс: ", current_class)
            clean_text = clean_html_tags(rows[row])

            # Ищем в строке текущий класс заклинания. Если находим класс, то устанавливаем его по умолчанию,
            # получаем QuerySet и дальше читаем строки...
            search_class = search_current_class(clean_text)
            if search_class:
                print('Устанавливаю текущий класс - ', search_class)
                current_class = search_class
                try:
                    current_class_qs = CharClasses.objects.get(name=current_class)
                    continue
                except ObjectDoesNotExist as err:
                    print('Не удалось установить текущий класс {}\n'.format(current_class), err)
                    exit()

            spell_obj = db_search_spell(clean_text)
            if spell_obj:
                print('Добавляем принадлежность класса {0} в заклинание {1}'.format(current_class, clean_text))
                spell_obj.spell_classes.add(current_class_qs)
            else:
                with open(ERROR_LOGFILE, 'w') as err_file:
                    err_file.write(clean_text)
                    err_file.write('\n')
            # input()


if __name__ == '__main__':
    main()
