from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import AdvUser
from .models import CharBase, CharClasses, CharRaces
#from .models import user_registrated
import datetime


class FindSpellForm(forms.Form):
    name = forms.CharField(required=False, label='Поиск заклинания')
    ritual = forms.BooleanField(required=False, label='Поиск ритуалов')
    concentrate = forms.BooleanField(required=False, label='Концентрация')


class UploadAvatarForm(forms.Form):
    name = forms.CharField(label='Имя персонажа')
    avatar = forms.ImageField(label='Аватар персонажа')


class SpellForm(forms.Form):
    name = forms.CharField(label='Название заклинания')
    level = forms.IntegerField(label='Уровень заклинания')
    school = forms.IntegerField(label='Школа заклинания')
    comp_is_verbal = forms.BooleanField(label='Вербальные требования')
    comp_is_somatic = forms.BooleanField(label='Соматичесские требования')
    comp_is_material = forms.BooleanField(label='Материальные компоненты')
    components = forms.CharField(label='Компоненты заклинания')
    distance = forms.CharField(label='Дистанция заклинания')
    duration = forms.CharField(label='Длительность заклинания')
    cast_time = forms.CharField(label='Время сотворения заклинания')
    is_concentrate = forms.BooleanField(label='Концентрация')
    is_ritual = forms.BooleanField(label='Ритуал')
    description = forms.CharField(label='Описание заклинания')
    #gold =  = forms.IntegerField(label='Золото')
    spell_classes = forms.CharField(required=False, label='Класс персонажа')


class CreateCharForm(forms.Form):
    name = forms.CharField(label='Имя персонажа')
    race = forms.ChoiceField(choices=CharRaces.RACE_CHOICES, label='Расса персонажа')
    playername = forms.CharField(label='Реальное имя персонажа')
    char_class = forms.ChoiceField(choices=CharClasses.CLASS_CHOICES, label='Класс персонажа')


class CharForm(forms.Form):
    name = forms.CharField(label='Имя персонажа')
    race = forms.ChoiceField(choices=CharRaces.RACE_CHOICES, label='Расса персонажа')
    playername = forms.CharField(label='Реальное имя персонажа')
    char_class = forms.ChoiceField(choices=CharClasses.CLASS_CHOICES, label='Класс персонажа')
    level = forms.IntegerField(label='Уровень персонажа')
    expirence = forms.IntegerField(label='Опыт персонажа')
    strength = forms.IntegerField(label='Сила персонажа')
    dexterity = forms.IntegerField(label='Ловкость персонажа')
    constitution = forms.IntegerField(label='Телосложение персонажа')
    intellegence = forms.IntegerField(label='Интеллект персонажа')
    wisdom = forms.IntegerField(label='Мудрость персонажа')
    chrarisma = forms.IntegerField(label='Харизма персонажа')
    modified = forms.DateTimeField(required=False, initial=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                   input_formats=['%Y-%m-%d %H:%M:%S'], label='Время модификации')
    #spells = forms.ModelMultipleChoiceField(queryset=Spell.objects.all())
    spells = forms.CharField(required=False, label='Доступные заклинания персонажа')
    char_spells = forms.CharField(required=False, label='Заклинания персонажа')


class CreateCharViewForm(ModelForm):
    class Meta:
        model = CharBase
        fields = ('name',
                 'races',
                 'playername',
                 'level',
                 'expirence',
                 'strength',
                 'dexterity',
                 'constitution',
                 'intellegence',
                 'wisdom',
                 'chrarisma',
                 'char_classes',
                  )


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адерс эл. почты')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_message')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают',
                                  code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # default is false
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        # user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_message')
