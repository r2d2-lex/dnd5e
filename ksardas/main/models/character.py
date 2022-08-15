from django.db import models
from django.shortcuts import get_object_or_404

from .common import CharClasses
from .common import CharRaces
from .spells import Spell


class CharacterManager(models.Manager):
    pass


# Основная таблица персонажа
class CharBase(models.Model):
    owner = models.ForeignKey('AdvUser', null=False, on_delete=models.PROTECT, verbose_name='Владелец персонажа')

    # 1'st page top
    playername = models.CharField(null=True, max_length=20, verbose_name='Реальное имя персонажа')
    level = models.IntegerField(default=1, verbose_name='Уровень персонажа')
    char_history = models.CharField(default='', max_length=32, verbose_name='Предыстория')
    name = models.CharField(db_index=True, null=False, max_length=20, verbose_name='Имя персонажа')
    races = models.ManyToManyField(CharRaces, choices=CharRaces.RACE_CHOICES, max_length=20,
                                   verbose_name='Расса персонажа')
    expirence = models.IntegerField(default=0, verbose_name='Опыт персонажа')
    world_view = models.CharField(default='', max_length=32, verbose_name='Мировозрение')

    # 1st page 1 column
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
    profi_languages = models.TextField(default='', verbose_name='Прочие владения и языки')

    # 1'st page 2 column
    psv_perception = models.CharField(default='', max_length=32, verbose_name='пассивная мудрость (внимательность)')
    prof_bonus = models.IntegerField(default=0, verbose_name='Бонус мастерства')
    initiative = models.IntegerField(default=0, verbose_name='Инициатива')
    inspiration = models.IntegerField(default=0, verbose_name='Вдохновение')
    hitpoints_curr = models.IntegerField(default=0, verbose_name='Текущие хиты')
    hitpoints_temp = models.IntegerField(default=0, verbose_name='Временные хиты')
    char_classes = models.ManyToManyField(CharClasses, choices=CharClasses.CLASS_CHOICES,
                                          verbose_name='Класс персонажа')

    attacks_spellc = models.TextField(default='', verbose_name='Атаки и заклинания')
    equipment = models.TextField(default='', verbose_name='Снаряжение')
    gold_count = models.IntegerField(default=0, verbose_name='Золото персонажа')
    silver_count = models.IntegerField(default=0, verbose_name='Серебро персонажа')
    copper_count = models.IntegerField(default=0, verbose_name='Медь персонажа')

    # Base info
    armor_class = models.IntegerField(default=0, verbose_name='Класс доспеха')
    speed = models.CharField(default='', max_length=32, verbose_name='Скорость персонажа')
    hitpoints_max = models.IntegerField(default=0, verbose_name='Максимум хитов')
    hitpoints_str = models.CharField(default='', max_length=32, verbose_name='Кости хитов')

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

    # 1'st page 3 column
    pers_traits = models.TextField(default='', verbose_name='Персональные черты')
    ideals = models.TextField(default='', verbose_name='Идеалы')
    bonds = models.TextField(default='', verbose_name='Привязанности')
    flaws = models.TextField(default='', verbose_name='Пороки')
    features_traits = models.TextField(default='', verbose_name='Умения и особенности')

    # 2 page
    gender = models.BooleanField(default=True, verbose_name='Пол')
    age = models.IntegerField(default=21, verbose_name='Возраст персонажа')
    height = models.IntegerField(default=175, verbose_name='Рост персонажа')
    weight = models.IntegerField(default=60, verbose_name='Вес персонажа')
    hair = models.CharField(default='', max_length=20, verbose_name='Цвет волос')
    eyes = models.CharField(default='', max_length=20, verbose_name='Цвет глаз')
    skin = models.CharField(default='', max_length=20, verbose_name='Цвет кожы')
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='Аватар')

    # 3 page
    spells = models.ManyToManyField(Spell)

    # Special
    modified = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время модификации')

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
        app_label = 'main'
