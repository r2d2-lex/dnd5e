from django.core.signing import BadSignature
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404

from django.urls import reverse_lazy
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .forms import CharForm
from .forms import CreateCharForm
from .forms import ChangeUserInfoForm
from .forms import RegisterUserForm
from .models import AdvUser, CharBase, Spell
from .utilites import signer
import datetime


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

    #
    # template = loader.get_template('main/profile.html')
    # chars = CharBase.objects.all()
    # context = {'chars': chars}
    # return HttpResponse(template.render(context, request=request))
    #


# Операции с персонажем
# Создание персонажа
class CharCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'main/create_character.html'
    form_class = CreateCharForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Персонаж создан'

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['chars'] = CharBase.objects.all()
    #    return context

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
    ch = CharBase.objects.get(name=name)
    return render(request, 'main/character.html', {'char': ch})


# Редактирование персонажа
@login_required
def edit_character(request, name):
    if request.method == 'POST':
        charform = CharForm(request.POST)
        print("\r\n*\r\n", request.POST, "\r\n*\r\n")
        if charform.is_valid():
            name = charform.cleaned_data['name']
            charbase = CharBase.objects.get(name=name)
            charbase.name = charform.cleaned_data['name']
            charbase.playername = charform.cleaned_data['playername']
            charbase.race = charform.cleaned_data['race']
            charbase.level = charform.cleaned_data['level']
            charbase.expirence = charform.cleaned_data['expirence']
            charbase.strength = charform.cleaned_data['strength']
            charbase.dexterity = charform.cleaned_data['dexterity']
            charbase.constitution = charform.cleaned_data['constitution']
            charbase.intellegence = charform.cleaned_data['intellegence']
            charbase.wisdom = charform.cleaned_data['wisdom']
            charbase.chrarisma = charform.cleaned_data['chrarisma']
            charbase.modified = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # добавление заклинаний
            if 'do_addspell' in request.POST:
                spell = charform.cleaned_data['spells']
                if spell != '':
                    spell = Spell.objects.get(name=spell)
                    charbase.spells.add(spell)

            if 'do_delspell' in request.POST:
                char_spells = request.POST.getlist('char_spells')
                for spell in char_spells:
                    remove_spell = Spell.objects.get(name=spell)
                    charbase.spells.remove(remove_spell)

            charbase.save()
        else:
            print("FORM NOT VALID. ERROR:", charform.errors)

    # Загрузка персонажа
    charform = CharBase.objects.get(name=name)

    # Загрузка спеллов персонажа
    char_spells = charform.spells.all()

    # Загрузка имён спеллов
    spells_name = Spell.objects.values_list('name', flat=True).order_by('name')

    context = {'form': charform, 'spells': spells_name, 'char_spells': char_spells}
    return render(request, 'main/edit_character.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    return render(request, 'main/index.html')
