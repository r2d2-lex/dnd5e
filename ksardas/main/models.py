from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import Signal
from django.shortcuts import get_object_or_404
from .utilites import send_activation_notification, str2bool

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


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

    # Новый управляющий класс модели
    char_races = RaceManager()
    # Управляющий класс по умолчанию теперь нужно определять явно
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

    def main_search(self, request, form=None):
        """
            Вход: request - параметр запроса, form - фор
            Возвращает: find_parms - строка параметров со значениями, spells_list - queryset списка заклинаний
        """
        spells_list = self.all()
        find_parms = ''

        # name = form.cleaned_data['name']
        name = request.GET.get("name", '')
        if name != '':
            name = name.upper()
            spells_list = spells_list.filter(name__icontains=name)
            find_parms += "&name={}".format(name)

        if str2bool(request.GET.get("ritual", False)):
            print('Include ritual')
            spells_list = spells_list.filter(is_ritual=True)
            find_parms += "&ritual={}".format("on")

        if str2bool(request.GET.get("concentrate", False)):
            print('Include concentrate')
            spells_list = spells_list.filter(is_concentrate=True)
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

    name = models.CharField(db_index=True, unique=True, null=False, max_length=20, verbose_name='Название заклинания')
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


# Основная таблица персонажа
class CharBase(models.Model):
    owner = models.ForeignKey('AdvUser', null=False, on_delete=models.PROTECT, verbose_name='Владелец персонажа')
    name = models.CharField(db_index=True, unique=True, null=False, max_length=20, verbose_name='Имя персонажа')

    races = models.ManyToManyField(CharRaces, choices=CharRaces.RACE_CHOICES, max_length=20,
                                   verbose_name='Расса персонажа')
    playername = models.CharField(null=True, max_length=20, verbose_name='Реальное имя персонажа')
    level = models.IntegerField(null=False, default=1, verbose_name='Уровень персонажа')
    expirence = models.IntegerField(null=False, default=0, verbose_name='Опыт персонажа')
    strength = models.IntegerField(null=False, default=8, verbose_name='Сила персонажа')
    dexterity = models.IntegerField(null=False, default=8, verbose_name='Ловкость персонажа')
    constitution = models.IntegerField(null=False, default=8, verbose_name='Телосложение персонажа')
    intellegence = models.IntegerField(null=False, default=8, verbose_name='Интеллект персонажа')
    wisdom = models.IntegerField(null=False, default=8, verbose_name='Мудрость персонажа')
    chrarisma = models.IntegerField(null=False, default=8, verbose_name='Харизма персонажа')
    modified = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время модификации')
    spells = models.ManyToManyField(Spell)

    prof_bonus = models.IntegerField(null=True, default=0, verbose_name='Бонус мастерства')
    armor_class = models.IntegerField(null=True, default=0, verbose_name='Броня персонажа')
    speed = models.IntegerField(null=True, default=0, verbose_name='Скорость персонажа')
    initiative = models.IntegerField(null=True, default=0, verbose_name='Инициатива')
    inspiration = models.IntegerField(null=True, default=0, verbose_name='Вдохновение')
    hitpoints_max = models.IntegerField(null=True, default=0, verbose_name='Максимальое здоровье')
    hitpoints_curr = models.IntegerField(null=True, default=0, verbose_name='Текущее здоровье')
    hitpoints_temp = models.IntegerField(null=True, default=0, verbose_name='Временные очки здоровья')

    char_classes = models.ManyToManyField(CharClasses, choices=CharClasses.CLASS_CHOICES,
                                          verbose_name='Класс персонажа')
    world_view = models.IntegerField(null=True, default=0, verbose_name='Мировозрение')
    gender = models.BooleanField(default=True, verbose_name='Пол')
    age = models.IntegerField(null=True, default=21, verbose_name='Возраст персонажа')
    height = models.IntegerField(null=True, default=175, verbose_name='Рост персонажа')
    weight = models.IntegerField(null=True, default=60, verbose_name='Вес персонажа')
    hair = models.CharField(null=True, max_length=20, verbose_name='Цвет волос')
    eyes = models.CharField(null=True, max_length=20, verbose_name='Цвет глаз')
    skin = models.CharField(null=True, max_length=20, verbose_name='Цвет кожы')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='Аватар')

    pers_traits = models.CharField(null=True, max_length=20, verbose_name='Персональные черты')
    ideals = models.CharField(null=True, max_length=20, verbose_name='Идеалы')
    bonds = models.CharField(null=True, max_length=20, verbose_name='Привязанности')
    flaws = models.CharField(null=True, max_length=20, verbose_name='Пороки')
    char_history = models.TextField(default='', verbose_name='История персонажа')

    gold_count = models.IntegerField(null=True, default=0, verbose_name='Золото персонажа')
    silver_count = models.IntegerField(null=True, default=0, verbose_name='Серебро персонажа')
    copper_count = models.IntegerField(null=True, default=0, verbose_name='Медь персонажа')

    char = CharacterManager()
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        # Удаление аватара
        super().delete(*args, **kwargs)

    def add_spell(self, request, form):
        if 'do_addspell' in request.POST:
            spell = form.cleaned_data['spells']
            if spell != '':
                add_spell = get_object_or_404(Spell, name=spell)
                self.spells.add(add_spell)
                return True
        return False

    def remove_spell(self, request):
        if 'do_delspell' in request.POST:
            # Требуется проверка?
            char_spells = request.POST.getlist('char_spells')
            for spell in char_spells:
                remove_spell = get_object_or_404(Spell, name=spell)
                self.spells.remove(remove_spell)

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
