#!/usr/bin/env python3

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from main.models import MobBase
from main.utilites import get_html
import re
from bs4 import BeautifulSoup

STRING_FIELD = 0
DB_FIELD = 1
DESCRIPTION_ADD_FIELD = 2
FIELD_SKIP = 'SKIP_FIELD'
FIELD_DESCRIPTION = 'description'

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
            # input()


def print_lis(params, db):
    for param in params:
        li = param.findAll('li', recursive=False)
        if li:
            print_lis(li, db)
        else:
            search_title(param.text, db)


FIELDS = (
    ('Действия', 'actions', 0),
    ('Действия логова', FIELD_DESCRIPTION, 1),
    ('Игровой персонаж', FIELD_DESCRIPTION, 0),
    ('Источник:', 'material_source', 0),
    ('Класс доспеха:', 'armor_class', 0),
    ('Материал взят ', FIELD_SKIP, 0),
    ('Монстра добавил:', FIELD_SKIP, 0),
    ('Навыки:', 'skills', 0),
    ('Опасность:', 'danger', 0),
    ('Описание', FIELD_DESCRIPTION, 0),
    ('Реакции', 'actions', 0),
    ('Спасброски:', 'saving_throws', 0),
    ('Способности', 'abilities', 0),
    ('Скорость:', 'speed', 0),
    ('Легендарные действия', 'actions', 1),
    ('Логово', FIELD_DESCRIPTION, 1),
    ('Хиты:', 'hitpoints_max', 0),
    ('Чувства:', 'feelings', 0),
    ('Эффекты логова', FIELD_DESCRIPTION, 1),
)


def search_title(text, db):
    search_text = text.strip()
    for field in FIELDS:
        result = re.findall(field[STRING_FIELD] + '(.*)', search_text)
        if result:
            try:
                key = field[DB_FIELD]
                val = result[0].strip()
                val_pref = field[STRING_FIELD]
                descr_field = field[DESCRIPTION_ADD_FIELD]
            except IndexError as err:
                print('Error get value: {}'.format(err))
                input()
                continue

            if key == FIELD_SKIP:
                return

            if key == 'hitpoints_max' or key == 'armor_class':
                hp_ac_get(db, key, val)
                return

            if descr_field == 1:
                val = val_pref + ':\r\n' + val

            save_db(db, key, val)
            print('DB_KEY {key}, Search_KEY: {val_pref} VALUE: {val}\r\n'.format(key=key, val=val, val_pref=val_pref))
            return

    # Undifined пишем в description
    print('Undifined:::' + search_text + '\r\n')
    save_db(db, FIELD_DESCRIPTION, search_text)
    return


def hp_ac_get(db, key, val):
    if key == 'hitpoints_max':
        str_key = 'hitpoints_str'
    else:
        str_key = 'armor_class_str'
    try:
        vals = re.findall(r'(\d+)(?:\s)?(\(.*\))?', val)[0]
        vals_str = vals[0] + ' ' + vals[1]
        new_val = int(vals[0])
    except (IndexError, TypeError) as err:
        print('Error get parms: {}'.format(err))
        input()
        return
    save_db(db, key, new_val)
    save_db(db, str_key, vals_str)
    return


def check_existing_record(db, key, val):
    FIELDS_ADD = (
        'actions',
        'description'
    )

    for field_add in FIELDS_ADD:
        if key == field_add:
            existing_val = getattr(db, key)
            if existing_val:
                return existing_val + '\r\n\r\n' + val
    return


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
        try:
            print('Size: {}, Type: {}, Alignment: {}'.format(sta[0],sta[1],sta[2]))
            save_db(db, 'size', sta[0])
            save_db(db, 'mob_type', sta[1])
            save_db(db, 'world_view', sta[2])
        except IndexError as err:
            print('Error get size_type_alignment: {}'.format(err))
            input()
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
    save_val = val
    new_val = check_existing_record(db, key, save_val)
    if new_val:
        save_val = new_val

    try:
        setattr(db, key, save_val)
    except (AttributeError, TypeError) as err:
        print('Поле: {}, Значение: {}, Ошибка: {}'.format(key, save_val, err))
        input('')
    return
