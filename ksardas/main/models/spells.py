from django.db import models
# from ksardas.main.utilites import str2bool

from .common import CharClasses


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
            # spells_list = spells_list.filter(is_concentrate=str2bool(concentrate))
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
            'distance': self.distance,
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
        app_label = 'main'

