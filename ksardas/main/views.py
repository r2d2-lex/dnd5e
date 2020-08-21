from django.core.signing import BadSignature
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404, JsonResponse

from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .forms import CharForm, CreateCharForm
from .forms import CreateCharViewForm
from .forms import FindSpellForm
from .forms import ChangeUserInfoForm
from .forms import RegisterUserForm
from .forms import UploadAvatarForm
from .models import AdvUser, CharBase, CharClasses, CharRaces, Spell
from .utilites import signer
import datetime

from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# Операции с учётной записью пользователя
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменён'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_login_url(self):
        return super().get_login_url()


class BBLoginView(LoginView):
    template_name = 'main/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()
    return render(request, template)


@login_required
def profile(request):
    print("Current account: ", request.user)
    chars = CharBase.objects.filter(owner=request.user)
    return render(request, 'main/profile.html', {'chars': chars})


# Операции с персонажем
# Создание персонажа
class CharCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'main/create_char_view.html'
    form_class = CreateCharViewForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Персонаж создан'
    model = CharBase

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super().form_valid(form)


# Просмотр персонажа
@login_required
def view_character(request, name):
    print("Current char: ", name)
    ch = get_object_or_404(CharBase, name=name)
    return render(request, 'main/character.html', {'char': ch})


# Все заклинания
from django.db.models import Q
@login_required
def find_spells(request):
    char_classes = CharClasses.charclass.get_classes_captions()
    spell_levels = Spell.spells.get_spell_levels()

    if request.method == 'GET':
        # Ajax trip
        if request.GET.get('fspells', None):
            fspells = request.GET.get('fspells')
            print('FSPELLS:', fspells)
            return JsonResponse({ 'is_taken' : fspells })

        find_spell_form = FindSpellForm(request.GET)

        if find_spell_form.is_valid():
            find_parms, spells_list = Spell.spells.main_search(request, find_spell_form)
        else:
            messages.add_message(request, messages.ERROR, find_spell_form.errors)

    paginator = Paginator(spells_list, 8)
    page = request.GET.get('page')
    try:
        spells_pages = paginator.page(page)
    except PageNotAnInteger:
        spells_pages = paginator.page(1)
    except EmptyPage:
        spells_pages = paginator.page(paginator.num_pages)

    # Prepare context
    context = {'spells': spells_pages, 'parms': find_parms, 'charclasses': char_classes, 'spell_levels': spell_levels}
    return render(request, 'main/find-spells.html', context)


@login_required
def edit_spell(request, id):
    spell = get_object_or_404(Spell, id=id)
    context = {'spell': spell}
    return render(request, 'main/edit_spell.html', context)


@login_required
def create_character(request):
    # CharRaces.race.create_db()
    # CharClasses.charclass.create_db()

    if request.method == 'POST':
        charform = CreateCharForm(request.POST)
        if charform.is_valid():
            char_name = charform.cleaned_data['name']
            create_char = CharBase(name=char_name, playername=charform.cleaned_data['playername'], owner=request.user)
            print(charform.cleaned_data['race'])
            print(charform.cleaned_data['char_class'])
            create_char.save()
            # Можно добавлять только после сохранения
            create_char.races_set(charform.cleaned_data['race'])
            create_char.char_classes_set(charform.cleaned_data['char_class'])
            return HttpResponseRedirect(reverse('main:edit_character', kwargs={'name': char_name}))
        else:
            messages.add_message(request, messages.ERROR, charform.errors)
            print("charform NOT VALID. ERROR:\r\n", charform.errors)

    char_classes = CharClasses.char_classes.get_classes_captions()
    char_races = CharRaces.char_races.get_races_captions()
    context = {'char_classes': char_classes, 'char_races': char_races}
    return render(request, 'main/create_character.html', context)


@login_required
def delete_character(request, name):
    if request.method == 'POST':
        charbase = get_object_or_404(CharBase, owner=request.user, name=name)
        charbase.delete()
        messages.add_message(request, messages.WARNING, 'Персонаж удалён')
        return redirect(reverse('main:profile'))
    context = {'name': name}
    return render(request, 'main/delete_character.html', context)


# Редактирование персонажа
@login_required
def edit_character(request, name):
    # Загрузка изображения
    if bool(request.FILES.get('avatar', False)):
        if request.method == 'POST':
            avatar_form = UploadAvatarForm(request.POST, request.FILES)
            if avatar_form.is_valid():
                char_name = avatar_form.cleaned_data['name']
                charbase = get_object_or_404(CharBase, owner=request.user, name=char_name)
                charbase.avatar = avatar_form.cleaned_data['avatar']
                charbase.save(update_fields=["avatar"])
                messages.add_message(request, messages.SUCCESS, 'Аватар сохранён')
            else:
                print("avatar_form NOT VALID. ERROR:", avatar_form.errors)
                messages.add_message(request, messages.WARNING, avatar_form.errors)

    # Сохранение данынх в базу
    elif request.method == 'POST':
        charform = CharForm(request.POST)
        print("\r\n*\r\n", request.POST, "\r\n*\r\n")
        if charform.is_valid():
            name = charform.cleaned_data['name']
            charbase = get_object_or_404(CharBase, owner=request.user, name=name)
            charbase.name = charform.cleaned_data['name']
            charbase.playername = charform.cleaned_data['playername']
            charbase.level = charform.cleaned_data['level']
            charbase.expirence = charform.cleaned_data['expirence']
            charbase.strength = charform.cleaned_data['strength']
            charbase.dexterity = charform.cleaned_data['dexterity']
            charbase.constitution = charform.cleaned_data['constitution']
            charbase.intellegence = charform.cleaned_data['intellegence']
            charbase.wisdom = charform.cleaned_data['wisdom']
            charbase.chrarisma = charform.cleaned_data['chrarisma']
            charbase.modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            charbase.races_set(charform.cleaned_data['race'])
            charbase.char_classes_set(charform.cleaned_data['char_class'])

            # добавление заклинаний и удаления заклинаний
            charbase.add_spell(request, charform)
            charbase.remove_spell(request)

            charbase.save()
            messages.add_message(request, messages.SUCCESS, 'Изменения сохранены')
        else:
            print("charform NOT VALID. ERROR:\r\n", charform.errors)
            messages.add_message(request, messages.WARNING, charform.errors)

    # Загрузка персонажа
    charbase_qs = get_object_or_404(CharBase, owner=request.user, name=name)

    # Загрузка имён спеллов
    spells_name = Spell.spells.get_spell_names()
    char_classes = CharClasses.char_classes.get_classes_captions()
    char_races = CharRaces.char_races.get_races_captions()

    # Получаем текущую рассу
    cur_race = charbase_qs.get_current_race()
    # Получаем текущий класс(пока только один)
    cur_class = charbase_qs.get_current_char_classes()

    print('Current RACE:', cur_race, '  Current CLASS:', cur_class)

    context = {'form': charbase_qs, 'spells': spells_name, 'races': char_races, 'classes': char_classes,
               'cur_race': cur_race, 'cur_class': cur_class}
    return render(request, 'main/edit_character.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    return render(request, 'main/index.html')
