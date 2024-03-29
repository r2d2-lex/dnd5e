from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import AdvUser
from .models import CharBase, CharClasses, CharRaces, Spell
from .tasks import send_verification_email
from .utilites import get_date_time, resize_image


class FindSpellForm(forms.Form):
    name = forms.CharField(required=False, label='Поиск заклинания')
    ritual = forms.BooleanField(required=False, label='Поиск ритуалов')
    concentrate = forms.CharField(required=False, label='Концентрация')
    level = forms.CharField(required=False, label='Уровень заклинания')
    school = forms.CharField(required=False, label='Школа заклинания')
    spc = forms.CharField(required=False, label='Класс заклинания')


class UploadIconForm(forms.Form):
    avatar = forms.ImageField(required=False, label='Аватар персонажа')
    allies_and_org_symbol = forms.ImageField(required=False, label='Символ')

    def upload_icon(self, request, char_base: CharBase, messages, image_field: str, sizes: tuple):
        if self.is_valid():
            try:
                image = resize_image(self.cleaned_data[image_field], sizes[0], image_field)
                if image_field == 'avatar':
                    char_base.avatar = image
                if image_field == 'allies_and_org_symbol':
                    char_base.allies_and_org_symbol = image
                char_base.save(update_fields=[image_field])
                messages.add_message(request, messages.SUCCESS, 'Изображение сохранено')
            except (IndexError, KeyError):
                messages.add_message(request, messages.WARNING, 'upload_icon: Ошибка дынных')
        else:
            print("IconForm not valid! ERROR:", self.errors)
            messages.add_message(request, messages.WARNING, self.errors)


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
        print('Расса при создании: ', self.cleaned_data['race'])
        print('Класс при создании: ', self.cleaned_data['char_class'])
        create_char.save()
        create_char.races_set(self.cleaned_data['race'])
        create_char.char_classes_set(self.cleaned_data['char_class'])
        return create_char


class CharForm(forms.Form):
    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page TOP ) -------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    char_classes = forms.ChoiceField(choices=CharClasses.CLASS_CHOICES, label='Класс персонажа')
    level = forms.IntegerField(label='Уровень персонажа')
    char_history = forms.CharField(required=False, label='Предыстория')
    playername = forms.CharField(label='Реальное имя персонажа')
    character_name = forms.CharField(label='Имя персонажа')
    char_races = forms.ChoiceField(choices=CharRaces.RACE_CHOICES, label='Расса персонажа')
    world_view = forms.CharField(required=False, label='Мировозрение')
    expirence = forms.IntegerField(label='Опыт персонажа')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 1 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #

    # -------------------- (( ХАРАКТЕРИСТИКИ )) ------------------------------------------------------
    strength = forms.IntegerField(label='Сила персонажа')
    strength_modifier = forms.IntegerField()
    dexterity = forms.IntegerField(label='Ловкость персонажа')
    dexterity_modifier = forms.IntegerField()
    constitution = forms.IntegerField(label='Телосложение персонажа')
    constitution_modifier = forms.IntegerField()
    intellegence = forms.IntegerField(label='Интеллект персонажа')
    intellegence_modifier = forms.IntegerField()
    wisdom = forms.IntegerField(label='Мудрость персонажа')
    wisdom_modifier = forms.IntegerField()
    chrarisma = forms.IntegerField(label='Харизма персонажа')
    chrarisma_modifier = forms.IntegerField()

    inspiration = forms.IntegerField(label='Вдохновение')
    prof_bonus = forms.IntegerField(label='Бонус мастерства')

    # -------------------- (( СПАСБРОСКИ )) ----------------------------------------------------------
    st_strength_box = forms.BooleanField(required=False)
    st_dexterity_box = forms.BooleanField(required=False)
    st_constitution_box = forms.BooleanField(required=False)
    st_intellegence_box = forms.BooleanField(required=False)
    st_wisdom_box = forms.BooleanField(required=False)
    st_chrarisma_box = forms.BooleanField(required=False)

    # -------------------- (( НАВЫКИ )) ---------------------------------------------------------------
    acrobatics_box = forms.BooleanField(required=False)
    animal_box = forms.BooleanField(required=False)
    arcana_box = forms.BooleanField(required=False)
    athletics_box = forms.BooleanField(required=False)
    deception_box = forms.BooleanField(required=False)
    history_box = forms.BooleanField(required=False)
    insight_box = forms.BooleanField(required=False)
    intimidation_box = forms.BooleanField(required=False)
    investigation_box = forms.BooleanField(required=False)
    nature_box = forms.BooleanField(required=False)
    performance_box = forms.BooleanField(required=False)
    medicine_box = forms.BooleanField(required=False)
    perception_box = forms.BooleanField(required=False)
    persuasion_box = forms.BooleanField(required=False)
    religion_box = forms.BooleanField(required=False)
    sleight_of_hand_box = forms.BooleanField(required=False)
    stealth_box = forms.BooleanField(required=False)
    survival_box = forms.BooleanField(required=False)

    psv_perception = forms.CharField(required=False, label='пассивная мудрость (внимательность)')
    prof_and_languages = forms.CharField(required=False, label='Прочие владения и языки')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 2 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    armor_class = forms.IntegerField(label='Класс доспеха')
    initiative = forms.IntegerField(label='Инициатива')
    speed = forms.IntegerField(label='Скорость персонажа')

    hit_points_curr = forms.IntegerField(label='Текущие хиты')
    hit_points_max = forms.IntegerField(label='Максимум хитов')

    hit_points_temp = forms.IntegerField(label='Временные хиты')

    hit_dice = forms.CharField(required=False, label='Кости хитов')

    # -------------------- (( Спасброски от смерти )) ----------------------------------------------------
    st_succ_death_box1 = forms.BooleanField(required=False)
    st_succ_death_box2 = forms.BooleanField(required=False)
    st_succ_death_box3 = forms.BooleanField(required=False)
    st_fail_death_box1 = forms.BooleanField(required=False)
    st_fail_death_box2 = forms.BooleanField(required=False)
    st_fail_death_box3 = forms.BooleanField(required=False)

    attacks_and_spell_casting = forms.CharField(required=False, label='Атаки и заклинания')

    equipment = forms.CharField(required=False, label='Снаряжение')
    gold_count = forms.IntegerField(label='Золото персонажа')
    silver_count = forms.IntegerField(label='Серебро персонажа')
    copper_count = forms.IntegerField(label='Медь персонажа')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 1st page 3 column ) --------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    pers_traits = forms.CharField(required=False, max_length=32, label='Персональные черты')
    ideals = forms.CharField(required=False, max_length=32, label='Идеалы')
    bonds = forms.CharField(required=False, max_length=32, label='Привязанности')
    flaws = forms.CharField(required=False, max_length=32, label='Пороки')
    features_traits = forms.CharField(required=False, label='Умения и особенности')

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page TOP) ----------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    # name
    age = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)

    eyes = forms.CharField(required=False)
    skin = forms.CharField(required=False)
    hair = forms.CharField(required=False)

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page 1st column) ---------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    # avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', verbose_name='Аватар')
    char_backstory = forms.CharField(required=False)

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 2 page 2 column) ------------------------------------------ #
    # ------------------------------------------------------------------------------------------------ #
    allies_and_org = forms.CharField(required=False)
    allies_and_org_symbol_name = forms.CharField(required=False)
    # allies_and_org_symbol = models.ImageField(null=True, blank=True, upload_to='symbols/', verbose_name='Символ')
    additional_features_traits = forms.CharField(required=False)
    treasure = forms.CharField(required=False)

    # ------------------------------------------------------------------------------------------------ #
    # ---------------------------------- ( 3 page ) -------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------ #
    spell_casting_ability = forms.CharField(required=False)
    spell_save_dc = forms.CharField(required=False)
    spell_attack_bonus = forms.CharField(required=False)

    SPELL_CHOICES = Spell.spells.get_spell_names_choices()
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
                    print(f'form_field: {form_field} Current: {set_attr} New: {self.cleaned_data[form_field]}')
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
