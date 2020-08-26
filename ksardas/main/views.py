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
    spells_list_qs = None
    find_options = None

    if request.method == 'GET':
        # Ajax trip
        if request.GET.get('fspells', None):
            fspells = request.GET.get('fspells')
            print('FSPELLS:', fspells)
            return JsonResponse({ 'is_taken' : fspells })

        find_spell_form = FindSpellForm(request.GET)

        if find_spell_form.is_valid():
            find_options, spells_list_qs = Spell.spells.main_search(request, find_spell_form)
        else:
            messages.add_message(request, messages.ERROR, find_spell_form.errors)

    # Paginator
    page = request.GET.get('page')
    spells_limit_list = 8
    paginator = Paginator(spells_list_qs, spells_limit_list)
    try:
        spells_pages = paginator.page(page)
    except PageNotAnInteger:
        spells_pages = paginator.page(1)
    except EmptyPage:
        spells_pages = paginator.page(paginator.num_pages)

    # Prepare context
    context = {
                'spells': spells_pages,
                'parms': find_options,
                'charclasses': CharClasses.char_classes.get_classes_captions(),
                'spell_levels': Spell.spells.get_spell_levels(),
    }
    return render(request, 'main/find-spells.html', context)


@login_required
def edit_spell(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    context = {'spell': spell}
    return render(request, 'main/edit_spell.html', context)


@login_required
def create_character(request):
    # CharRaces.race.create_db()
    # CharClasses.char_classes.create_db()

    if request.method == 'POST':
        character_form = CreateCharForm(request.POST)
        if character_form.is_valid():
            created_character_db = character_form.create_character(request)
            return redirect('main:edit_character', name=created_character_db.name)
            #return HttpResponseRedirect(reverse('main:edit_character', kwargs={'name': char_name}))
        else:
            messages.add_message(request, messages.ERROR, character_form.errors)
            print("charform NOT VALID. ERROR:\r\n", character_form.errors)

    context = {
                'char_classes': CharClasses.char_classes.get_classes_captions(),
                'char_races': CharRaces.char_races.get_races_captions(),
               }
    return render(request, 'main/create_character.html', context)


@login_required
def delete_character(request, name):
    if request.method == 'POST':
        character_db = get_object_or_404(CharBase, owner=request.user, name=name)
        character_db.delete()
        messages.add_message(request, messages.WARNING, 'Персонаж удалён')
        return redirect(reverse('main:profile'))
    context = {'name': name}
    return render(request, 'main/delete_character.html', context)


# Редактирование персонажа
@login_required
def edit_character(request, name):
    # Загрузка персонажа
    char_base = get_object_or_404(CharBase, owner=request.user, name=name)

    if request.method == 'POST':
        # Загрузка изображения
        if bool(request.FILES.get('avatar', False)):
            avatar_form = UploadAvatarForm(request.POST, request.FILES)
            if avatar_form.is_valid():
                char_name = avatar_form.cleaned_data['name']
                char_base = get_object_or_404(CharBase, owner=request.user, name=char_name)
                char_base.avatar = avatar_form.cleaned_data['avatar']
                char_base.save(update_fields=["avatar"])
                messages.add_message(request, messages.SUCCESS, 'Аватар сохранён')
            else:
                print("avatar_form NOT VALID. ERROR:", avatar_form.errors)
                messages.add_message(request, messages.WARNING, avatar_form.errors)
            return redirect('main:edit_character', name=char_base.name)

        # Сохранение данынх в базу
        char_form = CharForm(request.POST)
        if char_form.is_valid():
            char_form.edit_character(char_base, request)
            messages.add_message(request, messages.SUCCESS, 'Изменения сохранены')
            # После сохранений в форме всегда вызывай REDIRECT!
            return redirect('main:edit_character', name=char_base.name)
        else:
            print("char_form NOT VALID. ERROR:\r\n", char_form.errors)
            messages.add_message(request, messages.WARNING, char_form.errors)

    context = {
                'form': char_base,
                'spells': Spell.spells.get_spell_names(),
                'races': CharRaces.char_races.get_races_captions(),
                'classes': CharClasses.char_classes.get_classes_captions(),
                'cur_race': char_base.get_current_race(),
                'cur_class': char_base.get_current_char_classes(),
    }
    return render(request, 'main/edit_character.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    return render(request, 'main/index.html')
