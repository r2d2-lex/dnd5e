from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import AdvUser
from .models import CharBase, CharClasses, CharRaces, Spell
from .tasks import send_verification_email
from .utilites import get_date_time


class FindSpellForm(forms.Form):
    name = forms.CharField(required=False, label='Поиск заклинания')
    ritual = forms.BooleanField(required=False, label='Поиск ритуалов')
    concentrate = forms.CharField(required=False, label='Концентрация')
    level = forms.CharField(required=False, label='Уровень заклинания')
    school = forms.CharField(required=False, label='Школа заклинания')
    spc = forms.CharField(required=False, label='Класс заклинания')


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
    components = forms.CharField(label='Компоненты заклинания', required=False)
    distance = forms.CharField(label='Дистанция заклинания')
    duration = forms.CharField(label='Длительность заклинания')
    cast_time = forms.CharField(label='Время сотворения заклинания')
    is_concentrate = forms.BooleanField(label='Концентрация')
    is_ritual = forms.BooleanField(label='Ритуал')
    description = forms.CharField(label='Описание заклинания')
    spell_classes = forms.CharField(required=False, label='Класс персонажа')


class CreateCharForm(forms.Form):
    name = forms.CharField(label='Имя персонажа')
    race = forms.ChoiceField(choices=CharRaces.RACE_CHOICES, label='Расса персонажа')
    playername = forms.CharField(label='Реальное имя персонажа')
    char_class = forms.ChoiceField(choices=CharClasses.CLASS_CHOICES, label='Класс персонажа')

    def create_character(self, request):
        create_char = CharBase(
                                name=self.cleaned_data['name'],
                                playername=self.cleaned_data['playername'],
                                owner=request.user,
                               )
        print('Расса при создании: ',self.cleaned_data['race'])
        print('Класс при создании: ',self.cleaned_data['char_class'])
        create_char.save()
        create_char.races_set(self.cleaned_data['race'])
        create_char.char_classes_set(self.cleaned_data['char_class'])
        return create_char


class CharForm(forms.Form):
    SPELL_CHOICES = Spell.spells.get_spell_names_choices()
    name = forms.CharField(label='Имя персонажа')
    char_races = forms.ChoiceField(choices=CharRaces.RACE_CHOICES, label='Расса персонажа')
    playername = forms.CharField(label='Реальное имя персонажа')
    char_classes = forms.ChoiceField(choices=CharClasses.CLASS_CHOICES, label='Класс персонажа')
    level = forms.IntegerField(label='Уровень персонажа')
    expirence = forms.IntegerField(label='Опыт персонажа')
    world_view = forms.CharField(label='Мировозрение')
    char_history = forms.CharField(label='Предыстория')
    strength = forms.IntegerField(label='Сила персонажа')
    dexterity = forms.IntegerField(label='Ловкость персонажа')
    constitution = forms.IntegerField(label='Телосложение персонажа')
    intellegence = forms.IntegerField(label='Интеллект персонажа')
    wisdom = forms.IntegerField(label='Мудрость персонажа')
    chrarisma = forms.IntegerField(label='Харизма персонажа')
    strength_modifier = forms.IntegerField()
    dexterity_modifier = forms.IntegerField()
    constitution_modifier = forms.IntegerField()
    intellegence_modifier = forms.IntegerField()
    wisdom_modifier = forms.IntegerField()
    chrarisma_modifier = forms.IntegerField()

    armor_class = forms.IntegerField(label='Класс доспеха')
    initiative = forms.IntegerField(label='Инициатива')
    speed = forms.IntegerField(label='Скорость персонажа')
    inspiration = forms.IntegerField(label='Вдохновение')
    prof_bonus = forms.IntegerField(label='Бонус мастерства')

    hitpoints_curr = forms.IntegerField(label='Текущие хиты')
    hitpoints_temp = forms.IntegerField(label='Временные хиты')
    hitpoints_max = forms.IntegerField(label='Максимум хитов')
    hitpoints_str = forms.CharField(label='Кости хитов')
    psv_perception = forms.CharField(label='пассивная мудрость (внимательность)')
    attacks_spellc = forms.CharField(label='Атаки и заклинания')
    features_traits = forms.CharField(label='Умения и особенности')
    equipment = forms.CharField(label='Снаряжение')
    profi_languages = forms.CharField(label='Прочие владения и языки')

    pers_traits = forms.CharField(max_length=32, label='Персональные черты')
    ideals = forms.CharField(max_length=32, label='Идеалы')
    bonds = forms.CharField(max_length=32, label='Привязанности')
    flaws = forms.CharField(max_length=32, label='Пороки')
    modified = forms.DateTimeField(required=False, initial=get_date_time('%Y-%m-%d %H:%M:%S'),
                                   input_formats=['%Y-%m-%d %H:%M:%S'], label='Время модификации')
    spells = forms.MultipleChoiceField(required=False, choices=SPELL_CHOICES,
                                       label='Доступные заклинания персонажа')
    char_spells = forms.MultipleChoiceField(required=False, choices=SPELL_CHOICES,
                                            label='Заклинания персонажа')

    def edit_character(self, char_qs, request):
        for form_field in self.cleaned_data.keys():
            try:
                if form_field == 'char_classes':
                    char_qs.char_classes_set(self.cleaned_data[form_field])
                elif form_field == 'char_races':
                    char_qs.races_set(self.cleaned_data[form_field])
                elif form_field == 'spells':
                    char_qs.add_spell(request, self.cleaned_data.get('spells'))
                elif form_field == 'char_spells':
                    char_qs.remove_spell(request, self.cleaned_data.get('char_spells'))
                else:
                    set_attr = getattr(char_qs, form_field)
                    print('Current: ', set_attr, 'New: ', self.cleaned_data[form_field])
                    setattr(char_qs, form_field, self.cleaned_data[form_field])

            except (AttributeError, TypeError) as err:
                print('Form_field: {} Error: {}'.format(form_field, err))
                continue
        char_qs.modified = get_date_time('%Y-%m-%d %H:%M:%S')
        char_qs.save()


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
        user.is_active = False
        user.is_activated = False

        # Celery task
        send_verification_email.delay(self.cleaned_data['email'], user.username)

        if commit:
            user.save()
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_message')
