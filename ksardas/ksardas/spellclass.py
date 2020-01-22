from django.conf import settings
from django.db import models
import settings as app_settings
import re, sys
import config

sys.path.append(config.KSA_PATH)

settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)

import django
django.setup()

from main.models import Spell, CharClasses


CHAR_CLASSES = ['Бард', 'Волшебник', 'Друид', 'Жрец', 'Колдун', 'Паладин', 'Следопыт', 'Чародей']


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def add_classes(char_class):
    for cc in char_class:
        CharClasses.objects.create(name=cc)
    return


def search_current_class(search_class):
    for word in CHAR_CLASSES:
        ch = search_class.lower()
        wr = word.lower()
        if re.search(wr, ch) is not None:
            return word
    return None

def main():
    current_class = 'Бард'
    char_class = CharClasses.objects.get(name=current_class)

    f = open('cspells.html', 'r')
    rows = f.read().splitlines()
    row = 0
    err_file = open('errors.txt', 'w')

    while row < len(rows):
        text = cleanhtml(rows[row])
        sc = search_current_class(text)
        if sc:
            print("Current class: ",sc)
            current_class = sc
            char_class = CharClasses.objects.get(name=current_class)

        req = text.upper()
        req = req.strip()
        req = req.strip(':')
        print('TEXT: ',req)

        spell_obj = None
        try:
            spell_obj = Spell.objects.get(name=req)
        except:
            pass

        if spell_obj:
            spell_obj.spell_classes.add(char_class)
        else:
            err_file.write(req)
            err_file.write('\n')
        row += 1
    err_file.close()


if __name__ == '__main__':
    main()