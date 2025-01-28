from django import forms


class FindSpellForm(forms.Form):
    name = forms.CharField(required=False, label='Поиск заклинания')
    ritual = forms.BooleanField(required=False, label='Поиск ритуалов')
    concentrate = forms.CharField(required=False, label='Концентрация')
    level = forms.CharField(required=False, label='Уровень заклинания')
    school = forms.CharField(required=False, label='Школа заклинания')
    spc = forms.CharField(required=False, label='Класс заклинания')


class SpellForm(forms.Form):
    name = forms.CharField(label='Название заклинания')
    level = forms.IntegerField(label='Уровень заклинания')
    school = forms.IntegerField(label='Школа заклинания')
    comp_is_verbal = forms.BooleanField(label='Вербальные требования')
    comp_is_somatic = forms.BooleanField(label='Соматичесские требования')
    comp_is_material = forms.BooleanField(label='Материальные компоненты')
    components = forms.CharField(label='Компоненты заклинания', required=False)
    distance = forms.CharField(label='Дистанция заклинания')
    duration = forms.CharField(label='Длительность заклинания')
    cast_time = forms.CharField(label='Время сотворения заклинания')
    is_concentrate = forms.BooleanField(label='Концентрация')
    is_ritual = forms.BooleanField(label='Ритуал')
    description = forms.CharField(label='Описание заклинания')
    spell_classes = forms.CharField(required=False, label='Класс персонажа')
