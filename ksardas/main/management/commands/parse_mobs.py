#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from main.models import MobBase
from main.utilites import get_html


import re
from bs4 import BeautifulSoup

dnd_source = 'https://dungeon.su'
mob_html_group = dnd_source + '/bestiary/'


class Command(BaseCommand):
    help = 'Парсит сайт с Существами, заносит в БД'

    def parse_mobs(self):
        get_mobs()

    # def add_arguments(self, parser):
    #     parser.add_argument('site', nargs=1, type=str, help='сайт в формате https://site.com')

    def handle(self, *args, **kwargs):
        self.parse_mobs()
        print("Grab mobs from site ".format(dnd_source))


def get_mobs():
    html = get_html(mob_html_group)
    soup = BeautifulSoup(html, 'html.parser')
    if html:
        all_mobs = soup.find('ul', class_='list-of-items').findAll('li', class_='')
        print('Общее кол-во записей: {}'.format(len(all_mobs)))
        input('__________')
        for mob in all_mobs:
            mob_name = mob.find('a').text
            mob_href = mob.find('a')['href']
            print('------' * 10)
            print('Name: {}, Href: {}'.format(mob_name, mob_href))
            parse_mob(mob_name, mob_href)
            input()


def print_lis(params, db):
    for param in params:
        li = param.findAll('li', recursive=False)
        if li:
            print_lis(li, db)
        else:
            search_title(param.text, db)


def search_title(text, db):
    FIELDS = (
        ('Действия', 'actions'),
        ('Действия логова', 'description'),
        ('Игровой персонаж', 'description'),
        ('Источник:', 'material_source'),
        ('Класс доспеха:', 'armor_class'),
        ('Материал взят ', 'SKIP'),
        ('Монстра добавил:', 'SKIP'),
        ('Навыки:', 'skills'),
        ('Опасность:', 'danger'),
        ('Описание', 'description'),
        ('Реакции', 'actions'),
        ('Спасброски:', 'saving_throws'),
        ('Способности', 'abilities'),
        ('Скорость:', 'speed'),
        ('Легендарные действия', 'actions'),
        ('Логово', 'description'),
        ('Хиты:', 'hitpoints_max'),
        ('Чувства:', 'feelings'),
        ('Эффекты логова', 'description'),
    )

    FIELDS_ADD = (
        'actions',
        'description'
    )

    for field in FIELDS:
        key = ''
        val = ''
        result = re.findall(field[0]+'(.*)', text)
        if result:
            key = field[1]
            val = result[0]

            if key == 'SKIP':
                return

            if key == 'hitpoints_max' or key == 'armor_class':
                hp_ac_get(db, key, val)
                return

            for field_add in FIELDS_ADD:
                if key == field_add:
                    new_val = check_existing_val(db, key, val)
                    if new_val:
                        val = new_val
                        break

            save_db(db, key, val)
            print('Key {key}, Value: {val_pref} {val}\r\n'.format(key=key, val=val,val_pref=field[0]))
            return

    # Undifined пишем в description
    print('Undifined....' + text + '\r\n')
    return


def hp_ac_get(db, key, val):
    print('==Key {} Val: {} \r\n'.format(key, val))
    if key == 'hitpoints_max':
        str_key = 'hitpoints_str'
    else:
        str_key = 'armor_class_str'
    try:
        vals = re.findall(r'(\d+)(?:\s)?(\(.*\))?', val)[0]
        vals_str = vals[0] + ' ' + vals[1]
        new_val = int(vals[0])
    except (IndexError, TypeError) as err:
        print('Error get parms... {}'.format(err))
        input()
        return
    print('***new_val: ', new_val)
    print('***vals_str: ', vals_str, '\r\n')
    save_db(db, key, new_val)
    save_db(db, str_key, vals_str)
    return


def check_existing_val(db, key, val):
    existing_val = getattr(db, key)
    if existing_val:
        return existing_val + '\r\n\r\n' + val


def parse_stats(params, db):
    STATS = (
        ('СИЛ', 'strength'),
        ('ЛОВ', 'dexterity'),
        ('ТЕЛ', 'constitution'),
        ('ИНТ', 'intellegence'),
        ('МДР', 'wisdom'),
        ('ХАР', 'chrarisma'),
    )

    for param in params:
        stats = param.findAll('div', class_='stat')
        for stat in stats:
            key = ''
            val = ''
            two_divs = stat.findAll('div')

            for stat_element in STATS:
                try:
                    if stat_element[0] == two_divs[0].text:
                        key = stat_element[1]
                        print('Ключ: '+key)

                        # Поиск Характеристики и модификатора
                        val = re.findall(r'(\d{1,2})\s\(([+-]?\d)\)', two_divs[1].text)
                        print('Значение: ', val[0])
                        break
                except IndexError as err:
                    print('Ошибка получения характеристики: {}'.format(err))
                    input()

            save_db(db, key, int(val[0][0]))
            save_db(db, key+'_modifier', int(val[0][1]))
            print(two_divs[1].text+'\r\n')


def parse_size_type_alignment(soup, db):
    size_type_aligment = soup.find('ul', class_='params').find('li', class_='size-type-alignment', recursive=False)
    if size_type_aligment:
        sta = size_type_aligment.text.split(', ')
        print('Size: {}, Type: {}, Alignment: {}'.format(sta[0],sta[1],sta[2]))
        save_db(db, 'size', sta[0])
        save_db(db, 'mob_type', sta[1])
        save_db(db, 'world_view', sta[2])
    else:
        input('Size_Type_Alignment NOT FOUND')
    return


def parse_mob(name, link):
    html = get_html(dnd_source + link)
    soup = BeautifulSoup(html, 'html.parser')

    mob = MobBase()
    save_db(mob, 'name', name)
    parse_size_type_alignment(soup, mob)

    all_parms = soup.find('ul', class_='params').findAll('li', class_='', recursive=False)
    print_lis(all_parms, mob)
    all_parms = soup.find('ul', class_='params').findAll('li', class_='stats', recursive=False)
    parse_stats(all_parms, mob)
    all_parms = soup.find('ul', class_='params').findAll('li', class_='subsection', recursive=False)
    print_lis(all_parms, mob)

    try:
        mob.save()
    except IntegrityError:
        print('Запись {} уже в БД'.format(mob.name))

    return


def save_db(db, key, val):
    try:
        setattr(db, key, val)
    except (AttributeError, TypeError) as err:
        print('Поле: {}, Значение: {}, Ошибка: {}'.format(key, val, err))
        input('')
    return

# def main():
#     get_mobs()
#
#
# if __name__ == '__main__':
#     main()
