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

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page TOP ) -------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    char_classes = models.ManyToManyField(CharClasses, choices=CharClasses.CLASS_CHOICES,
                                          verbose_name='Класс персонажа')
    level = models.IntegerField(default=1, verbose_name='Уровень персонажа')
    char_history = models.CharField(default='', max_length=32, verbose_name='Предыстория')
    playername = models.CharField(null=True, max_length=20, verbose_name='Реальное имя персонажа')
    name = models.CharField(db_index=True, null=False, max_length=20, verbose_name='Имя персонажа')
    races = models.ManyToManyField(CharRaces, choices=CharRaces.RACE_CHOICES, max_length=20,
                                   verbose_name='Расса персонажа')
    world_view = models.CharField(default='', max_length=32, verbose_name='Мировозрение')
    expirence = models.IntegerField(default=0, verbose_name='Опыт персонажа')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 1 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #

    # -------------------- (( ХАРАКТЕРИСТИКИ )) ------------------------------------------------------
    strength = models.IntegerField(default=8, verbose_name='Сила персонажа')
    strength_modifier = models.IntegerField(default=0, verbose_name='Модификатор силы')
    dexterity = models.IntegerField(default=8, verbose_name='Ловкость персонажа')
    dexterity_modifier = models.IntegerField(default=0, verbose_name='Модификатор ловкости')
    constitution = models.IntegerField(default=8, verbose_name='Телосложение персонажа')
    constitution_modifier = models.IntegerField(default=0, verbose_name='Модификатор телосложения')
    intellegence = models.IntegerField(default=8, verbose_name='Интеллект персонажа')
    intellegence_modifier = models.IntegerField(default=0, verbose_name='Модификатор интеллекта')
    wisdom = models.IntegerField(default=8, verbose_name='Мудрость персонажа')
    wisdom_modifier = models.IntegerField(default=0, verbose_name='Модификатор мудрости')
    chrarisma = models.IntegerField(default=8, verbose_name='Харизма персонажа')
    chrarisma_modifier = models.IntegerField(default=0, verbose_name='Модификатор харизмы')

    inspiration = models.IntegerField(default=0, verbose_name='Вдохновение')
    prof_bonus = models.IntegerField(default=0, verbose_name='Бонус мастерства')

    # -------------------- (( СПАСБРОСКИ )) ----------------------------------------------------------
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

    # -------------------- (( НАВЫКИ )) ---------------------------------------------------------------
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
    sleight_of_hand = models.CharField(default='', max_length=8, verbose_name='Ловкость рук(лов)')
    stealth = models.CharField(default='', max_length=8, verbose_name='Скрытность(лов)')
    survival = models.CharField(default='', max_length=8, verbose_name='Выживание(мдр)')

    acrobatics_box = models.BooleanField(default=False)
    animal_box = models.BooleanField(default=False)
    arcana_box = models.BooleanField(default=False)
    athletics_box = models.BooleanField(default=False)
    deception_box = models.BooleanField(default=False)
    history_box = models.BooleanField(default=False)
    insight_box = models.BooleanField(default=False)
    intimidation_box = models.BooleanField(default=False)
    investigation_box = models.BooleanField(default=False)
    nature_box = models.BooleanField(default=False)
    performance_box = models.BooleanField(default=False)
    medicine_box = models.BooleanField(default=False)
    perception_box = models.BooleanField(default=False)
    persuasion_box = models.BooleanField(default=False)
    religion_box = models.BooleanField(default=False)
    sleight_of_hand_box = models.BooleanField(default=False)
    stealth_box = models.BooleanField(default=False)
    survival_box = models.BooleanField(default=False)

    psv_perception = models.CharField(default='', max_length=32, verbose_name='пассивная мудрость (восприятие)')
    prof_and_languages = models.TextField(default='', verbose_name='Прочие владения и языки')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 2 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    armor_class = models.IntegerField(default=0, verbose_name='Класс доспеха')
    initiative = models.IntegerField(default=0, verbose_name='Инициатива')
    speed = models.CharField(default='', max_length=32, verbose_name='Скорость персонажа')

    hit_points_curr = models.IntegerField(default=0, verbose_name='Текущие хиты')
    hit_points_max = models.IntegerField(default=0, verbose_name='Максимум хитов')

    hit_points_temp = models.IntegerField(default=0, verbose_name='Временные хиты')

    hit_dice = models.CharField(default='', max_length=8, verbose_name='Кости хитов')
    hit_dice_total = models.CharField(default='', max_length=8, verbose_name='Кости хитов макс.')

    # -------------------- (( Спасброски от смерти )) ----------------------------------------------------
    st_succ_death_box1 = models.BooleanField(default=False)
    st_succ_death_box2 = models.BooleanField(default=False)
    st_succ_death_box3 = models.BooleanField(default=False)
    st_fail_death_box1 = models.BooleanField(default=False)
    st_fail_death_box2 = models.BooleanField(default=False)
    st_fail_death_box3 = models.BooleanField(default=False)

    attacks_and_spell_casting = models.TextField(default='', verbose_name='Атаки и заклинания')

    equipment = models.TextField(default='', verbose_name='Снаряжение')
    gold_count = models.IntegerField(default=0, verbose_name='Золото персонажа')
    silver_count = models.IntegerField(default=0, verbose_name='Серебро персонажа')
    copper_count = models.IntegerField(default=0, verbose_name='Медь персонажа')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 3 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    pers_traits = models.TextField(default='', verbose_name='Персональные черты')
    ideals = models.TextField(default='', verbose_name='Идеалы')
    bonds = models.TextField(default='', verbose_name='Привязанности')
    flaws = models.TextField(default='', verbose_name='Пороки')
    features_traits = models.TextField(default='', verbose_name='Умения и особенности')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page TOP) ----------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    # name
    age = models.IntegerField(default=21, verbose_name='Возраст персонажа')
    height = models.IntegerField(default=175, verbose_name='Рост персонажа')
    weight = models.IntegerField(default=60, verbose_name='Вес персонажа')

    eyes = models.CharField(default='', max_length=20, verbose_name='Цвет глаз')
    skin = models.CharField(default='', max_length=20, verbose_name='Цвет кожы')
    hair = models.CharField(default='', max_length=20, verbose_name='Цвет волос')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page 1st column) ---------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='Аватар')
    char_backstory = models.TextField(default='', verbose_name='Предыстория персонажа')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page 2 column) ------------------------------------------ #
    # ------------------------------------------------------------------------------------------------ #
    allies_and_org = models.TextField(default='', verbose_name='Альянсы и организации')
    allies_and_org_symbol_name = models.CharField(default='', max_length=24, verbose_name='Название символа')
    allies_and_org_symbol = models.ImageField(null=True, blank=True, upload_to='symbols/', verbose_name='Символ')
    additional_features_traits = models.TextField(default='', verbose_name='Дополнительные особенности и черты')
    treasure = models.TextField(default='', verbose_name='Сокровища')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 3 page ) -------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    # name + char_classes
    spell_casting_ability = models.CharField(default='', max_length=12, verbose_name='Характеристика заклинателя')
    spell_save_dc = models.CharField(default='', max_length=12, verbose_name='DC спасброска от заклинания')
    spell_attack_bonus = models.CharField(default='', max_length=12, verbose_name='Бонус к атаке заклинанием')
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

    def get_current_race(self) -> str:
        cur_race = ''
        for cr in self.races.all():
            cur_race = cr.name
            break
        return cur_race

    def get_current_class(self) -> str:
        cur_class = ''
        for cc in self.char_classes.all():
            cur_class = cc.name
            break
        return cur_class

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
