from django.db import models


class MobBase(models.Model):
    name = models.CharField(db_index=True, unique=True, max_length=255, verbose_name='Имя моба')
    size = models.CharField(default='', max_length=255, verbose_name='Размер')
    mob_type = models.CharField(default='', max_length=255, verbose_name='тип')
    danger = models.CharField(default='', max_length=32, verbose_name='опасность')
    material_source = models.CharField(default='', max_length=255, verbose_name='источник материала')
    armor_class_str = models.CharField(default='', max_length=255, verbose_name='описание доспеха')
    description = models.TextField(default='', verbose_name='Описание')
    feelings = models.TextField(default='', verbose_name='чувства')
    abilities = models.TextField(default='', verbose_name='способности')
    actions = models.TextField(default='', verbose_name='действия')

    # class BaseInfo
    # 1'st page top
    world_view = models.CharField(default='', max_length=32, verbose_name='Мировозрение')

    # 1'st page 1 column
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

    # 1'st page 2 column
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

    modified = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время модификации')

    class Meta:
        app_label = 'main'
