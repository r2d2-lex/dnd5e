from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404
from .utilites import str2bool


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошёл активацию?')
    send_message = models.BooleanField(default=True, verbose_name='Слать сообщение о новых коментариях?')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class ClassManager(models.Manager):
    """ Создание таблицы с классами персонажей """

    def create_db(self):
        # Удаляем все записи перед созданием...
        for records_to_remove in self.all():
            records_to_remove.delete()

        for rc in CharClasses.CLASS_CHOICES:
            self.create(name=rc[0], caption=rc[1], description='Описание класса ' + rc[1])
        return


# Таблица класса персонажа
class CharClasses(models.Model):
    CLASS_CHOICES = (
        ('Варвар', "Варвар"),
        ('Бард', "Бард"),
        ('Жрец', "Жрец"),
        ('Друид', "Друид"),
        ('Воин', "Воин"),
        ('Монах', "Монах"),
        ('Паладин', "Паладин"),
        ('Следопыт', "Следопыт"),
        ('Плут', "Плут"),
        ('Чародей', "Чародей"),
        ('Колдун', "Колдун"),
        ('Волшебник', "Волшебник"),
    )
    name = models.CharField(db_index=True, choices=CLASS_CHOICES, unique=True, null=False, max_length=20,
                            verbose_name='Имя класса персонажа')
    caption = models.CharField(null=True, max_length=24, verbose_name='Caption класса')
    description = models.CharField(null=True, max_length=1024 * 64, verbose_name='Описание класса')
    char_classes = ClassManager()
    objects = models.Manager()

    @staticmethod
    def get_classes_captions():
        """
         Получение описаний классов...
         Возвращает список из двух элементов: Имя, Описание
        """
        return [(cl_name, cl_caption) for cl_name, cl_caption in CharClasses.CLASS_CHOICES]

    def __str__(self):
        return self.name


class RaceManager(models.Manager):
    # Класс модели всегда доступен управляющему классу через
    # self.model.
    def get_races(self):
        return self.values_list('name', flat=True).order_by('name')

    """ Создание таблицы с рассами персонажей """

    def create_db(self):
        # Удаляем все записи перед созданием...
        for records_to_remove in self.all():
            records_to_remove.delete()

        for rc in CharRaces.RACE_CHOICES:
            self.create(name=rc[0], caption=rc[1], description='Описание рассы ' + rc[1])
        return


class CharRaces(models.Model):
    RACE_CHOICES = (
        ('dwarf', "Дварф"),
        ('elf', "Эльф"),
        ('half', "Полурослик"),
        ('human', "Человек"),
        ('dragon', "Драконорождённый"),
        ('gnom', "Гном"),
        ('halfelf', "Полуэльф"),
        ('halfork', "Полуорк"),
        ('tifling', "Тифлинг"),
    )
    name = models.CharField(db_index=True, choices=RACE_CHOICES, unique=True, null=False, max_length=20,
                            verbose_name='Имя рассы персонажа')
    caption = models.CharField(null=True, max_length=24, verbose_name='Caption рассы')
    description = models.CharField(null=True, max_length=1024 * 64, verbose_name='Описание рассы')

    char_races = RaceManager()
    objects = models.Manager()

    @staticmethod
    def get_races_captions():
        """
         Получение описаний расс...
         Возвращает список из двух элементов: Имя рассы, Описание рассы
        """
        return [(race_name, race_caption) for race_name, race_caption in CharRaces.RACE_CHOICES]

    def __str__(self):
        return self.name


class SpellManager(models.Manager):
    def get_spell_names(self):
        return self.values_list('name', flat=True).order_by('name')

    def get_spell_names_choices(self):
        return tuple((choice, choice) for choice in self.get_spell_names())


    @staticmethod
    def spell_list(qs):
        spells = []
        for spell in qs:
            spells.append(spell.dict())
        return spells

    def main_search(self, form):
        """
            Вход: request - параметр запроса, form - форма
            Возвращает: find_parms - строка параметров со значениями, spells_list - queryset списка заклинаний
        """
        spells_list = self.all()
        find_parms = ''

        for name, value in form.cleaned_data.items():
            print('Key: {}, Val: {}'.format(name, value))

        name = form.cleaned_data['name']
        if name != '':
            name = name.upper()
            spells_list = spells_list.filter(name__startswith=name)
            find_parms += "&name={}".format(name)

        spell_level = form.cleaned_data['level']
        if spell_level != '':
            spells_list = spells_list.filter(level=spell_level)
            find_parms += "&level={}".format(spell_level)

        spc = form.cleaned_data['spc']
        if spc:
            spells_list = spells_list.filter(spell_classes__name=spc)
            find_parms += "&spc={}".format(spc)

        school = form.cleaned_data['school']
        if school:
            spells_list = spells_list.filter(school=school)
            find_parms += "&school={}".format(school)

        ritual = form.cleaned_data['ritual']
        if ritual:
            spells_list = spells_list.filter(is_ritual=True)
            find_parms += "&ritual={}".format("on")

        concentrate = form.cleaned_data['concentrate']
        if concentrate:
            spells_list = spells_list.filter(is_concentrate=str2bool(concentrate))
            find_parms += "&concentrate={}".format("on")
        return find_parms, spells_list


# Таблица для заклинаний
class Spell(models.Model):
    SPELL_SCHOOL_CHOICES = (
        (0, 'неизвестная'),
        (1, 'воплощение'),
        (2, 'очарование'),
        (3, 'ограждение'),
        (4, 'иллюзия'),
        (5, 'вызов'),
        (6, 'некромантия'),
        (7, 'преобразование'),
        (8, 'прорицание'),
    )

    name = models.CharField(db_index=True, unique=True, null=False, max_length=64, verbose_name='Название заклинания')
    level = models.IntegerField(verbose_name='Уровень заклинания')
    school = models.IntegerField(choices=SPELL_SCHOOL_CHOICES, default=0, verbose_name='Школа заклинания')
    comp_is_verbal = models.BooleanField(default=False, verbose_name='Вербальные требования')
    comp_is_somatic = models.BooleanField(default=False, verbose_name='Соматичесские требования')
    comp_is_material = models.BooleanField(default=False, verbose_name='Материальные компоненты')
    components = models.CharField(max_length=2048 * 64, verbose_name='Компоненты заклинания')
    distance = models.CharField(max_length=1024 * 64, verbose_name='Дистанция заклинания')
    duration = models.CharField(max_length=1024 * 64, verbose_name='Длительность заклинания')
    cast_time = models.CharField(max_length=1024 * 64, verbose_name='Время сотворения заклинания')
    is_concentrate = models.BooleanField(default=False, verbose_name='Концентрация')
    is_ritual = models.BooleanField(default=False, verbose_name='Ритуал')
    description = models.TextField(null=False, verbose_name='Описание заклинания')
    gold = models.IntegerField(null=True, verbose_name='Золото')
    spell_classes = models.ManyToManyField(CharClasses, verbose_name='Класс персонажа')
    spells = SpellManager()
    objects = models.Manager()

    def dict(self):
        obj = {
            'pk': self.pk,
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'comp_is_verbal': self.comp_is_verbal,
            'comp_is_somatic': self.comp_is_somatic,
            'comp_is_material': self.comp_is_material,
            'components': self.components,
            'distance': self.distance ,
            'duration': self.duration,
            'cast_time': self.cast_time,
            'is_concentrate': self.is_concentrate,
            'is_ritual': self.is_ritual,
            'description': self.description,
            'gold': self.gold,
        }
        return obj

    @staticmethod
    def get_spell_levels():
        max_spell_level = 10
        return [level for level in range(max_spell_level)]

    @staticmethod
    def get_spell_schools():
        return [(school_db, school_name) for school_db, school_name in Spell.SPELL_SCHOOL_CHOICES]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CharacterManager(models.Manager):
    pass


class BaseInfo(models.Model):
    strength = models.IntegerField(default=8, verbose_name='Сила персонажа')
    dexterity = models.IntegerField(default=8, verbose_name='Ловкость персонажа')
    constitution = models.IntegerField(default=8, verbose_name='Телосложение персонажа')
    intellegence = models.IntegerField(default=8, verbose_name='Интеллект персонажа')
    wisdom = models.IntegerField(default=8, verbose_name='Мудрость персонажа')
    chrarisma = models.IntegerField(default=8, verbose_name='Харизма персонажа')

    strength_modifier = models.IntegerField(default=0, verbose_name='модификатор')
    dexterity_modifier = models.IntegerField(default=0, verbose_name='модификатор')
    constitution_modifier = models.IntegerField(default=0, verbose_name='модификатор')
    intellegence_modifier = models.IntegerField(default=0, verbose_name='модификатор')
    wisdom_modifier = models.IntegerField(default=0, verbose_name='модификатор')
    chrarisma_modifier = models.IntegerField(default=0, verbose_name='модификатор')

    armor_class = models.IntegerField(default=0, verbose_name='Класс доспеха')
    speed = models.CharField(default='', max_length=32, verbose_name='Скорость персонажа')
    hitpoints_max = models.IntegerField(default=0, verbose_name='Максимум хитов')
    hitpoints_str = models.CharField(default='', max_length=32, verbose_name='Кости хитов')
    world_view = models.CharField(default='', max_length=32, verbose_name='Мировозрение')

    skills = models.TextField(default='', verbose_name='навыки')
    acrobatics = models.CharField(default='', max_length=8, verbose_name='Акробатика(лов)')
    animal = models.CharField(default='', max_length=8, verbose_name='Уход за животными(мдр)')
    arcana = models.CharField(default='', max_length=8, verbose_name='Магия(инт)')
    athletics = models.CharField(default='', max_length=8, verbose_name='Атлетика(сил)')
    deception = models.CharField(default='', max_length=8, verbose_name='Обман(хар)')
    history = models.CharField(default='', max_length=8, verbose_name='История(инт)')
    insight = models.CharField(default='', max_length=8, verbose_name='Проницательность(мдр)')
    intimidation = models.CharField(default='', max_length=8, verbose_name='Запугивание(хар)')
    investigation = models.CharField(default='', max_length=8, verbose_name='Расследование(инт)')
    nature = models.CharField(default='', max_length=8, verbose_name='Природа(инт)')
    performance = models.CharField(default='', max_length=8, verbose_name='Выступление(хар)')
    medicine = models.CharField(default='', max_length=8, verbose_name='Медицина(мдр)')
    perception = models.CharField(default='', max_length=8, verbose_name='Внимательность(мдр.)')
    persuasion = models.CharField(default='', max_length=8, verbose_name='Убеждение(хар)')
    religion = models.CharField(default='', max_length=8, verbose_name='Религия(инт)')
    sleightofHand = models.CharField(default='', max_length=8, verbose_name='Ловкость рук(лов)')
    stealth = models.CharField(default='', max_length=8, verbose_name='Скрытность(лов)')
    survival = models.CharField(default='', max_length=8, verbose_name='Выживание(мдр)')

    saving_throws = models.TextField(default='', verbose_name='спасброски')
    st_strength = models.CharField(default='', max_length=12)
    st_dexterity = models.CharField(default='', max_length=12)
    st_constitution = models.CharField(default='', max_length=12)
    st_intellegence = models.CharField(default='', max_length=12)
    st_wisdom = models.CharField(default='', max_length=12)
    st_chrarisma = models.CharField(default='', max_length=12)
    st_strength_box = models.BooleanField(default=False)
    st_dexterity_box = models.BooleanField(default=False)
    st_constitution_box = models.BooleanField(default=False)
    st_intellegence_box = models.BooleanField(default=False)
    st_wisdom_box = models.BooleanField(default=False)
    st_chrarisma_box = models.BooleanField(default=False)

    description = models.TextField(default='', verbose_name='Описание')
    feelings = models.TextField(default='', verbose_name='чувства')
    abilities = models.TextField(default='', verbose_name='способности')
    actions = models.TextField(default='', verbose_name='действия')

    modified = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время модификации')

    class Meta:
        abstract = True


# Основная таблица персонажа
class CharBase(BaseInfo):
    owner = models.ForeignKey('AdvUser', null=False, on_delete=models.PROTECT, verbose_name='Владелец персонажа')
    playername = models.CharField(null=True, max_length=20, verbose_name='Реальное имя персонажа')
    name = models.CharField(db_index=True, null=False, max_length=20, verbose_name='Имя персонажа')
    races = models.ManyToManyField(CharRaces, choices=CharRaces.RACE_CHOICES, max_length=20,
                                   verbose_name='Расса персонажа')

    expirence = models.IntegerField(default=0, verbose_name='Опыт персонажа')
    level = models.IntegerField(default=1, verbose_name='Уровень персонажа')
    spells = models.ManyToManyField(Spell)

    prof_bonus = models.IntegerField(default=0, verbose_name='Бонус мастерства')
    initiative = models.IntegerField(default=0, verbose_name='Инициатива')
    inspiration = models.IntegerField(default=0, verbose_name='Вдохновение')
    hitpoints_curr = models.IntegerField(default=0, verbose_name='Текущие хиты')
    hitpoints_temp = models.IntegerField(default=0, verbose_name='Временные хиты')
    char_classes = models.ManyToManyField(CharClasses, choices=CharClasses.CLASS_CHOICES,
                                          verbose_name='Класс персонажа')

    gender = models.BooleanField(default=True, verbose_name='Пол')
    age = models.IntegerField(default=21, verbose_name='Возраст персонажа')
    height = models.IntegerField(default=175, verbose_name='Рост персонажа')
    weight = models.IntegerField(default=60, verbose_name='Вес персонажа')
    hair = models.CharField(default='', max_length=20, verbose_name='Цвет волос')
    eyes = models.CharField(default='', max_length=20, verbose_name='Цвет глаз')
    skin = models.CharField(default='', max_length=20, verbose_name='Цвет кожы')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='Аватар')

    pers_traits = models.CharField(default='', max_length=32, verbose_name='Персональные черты')
    ideals = models.CharField(default='', max_length=32, verbose_name='Идеалы')
    bonds = models.CharField(default='', max_length=32, verbose_name='Привязанности')
    flaws = models.CharField(default='', max_length=32, verbose_name='Пороки')
    char_history = models.TextField(default='', verbose_name='Предыстория')

    gold_count = models.IntegerField(default=0, verbose_name='Золото персонажа')
    silver_count = models.IntegerField(default=0, verbose_name='Серебро персонажа')
    copper_count = models.IntegerField(default=0, verbose_name='Медь персонажа')

    char = CharacterManager()
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        # Удаление аватара
        super().delete(*args, **kwargs)

    def add_spell(self, request, spells):
        if 'do_addspell' in request.POST:
            for spell in spells:
                self.spells.add(get_object_or_404(Spell, name=spell))

    def remove_spell(self, request, spells):
        if 'do_delspell' in request.POST:
            for spell in spells:
                self.spells.remove(get_object_or_404(Spell, name=spell))

    def races_set(self, races):
        self.races.set([get_object_or_404(CharRaces, name=races)])

    def char_classes_set(self, char_classes):
        self.char_classes.set([get_object_or_404(CharClasses, name=char_classes)])

    def get_current_race(self):
        cur_race = False
        for cr in self.races.all():
            cur_race = cr.name
            break
        return cur_race

    def get_current_char_classes(self):
        cur_class = []
        for cc in self.char_classes.all():
            cur_class.append(cc.name)
        cur_class = cur_class[0] if len(cur_class) > 0 else "unknown"
        return cur_class

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-modified']


class MobBase(BaseInfo):
    name = models.CharField(db_index=True,unique=True, max_length=255, verbose_name='Имя моба')
    size = models.CharField(default='', max_length=255, verbose_name='Размер')
    mob_type = models.CharField(default='', max_length=255, verbose_name='тип')
    danger = models.CharField(default='', max_length=32, verbose_name='опасность')
    material_source = models.CharField(default='', max_length=255, verbose_name='источник материала')
    armor_class_str = models.CharField(default='', max_length=255, verbose_name='описание доспеха')
