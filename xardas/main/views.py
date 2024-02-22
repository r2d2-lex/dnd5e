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
from wsgiref.util import FileWrapper

from .forms import CharForm, CreateCharForm
from .forms import FindSpellForm
from .forms import ChangeUserInfoForm
from .forms import RegisterUserForm
from .forms import UploadIconForm
from .services import get_character_from_db, delete_character_from_db
from .models import AdvUser, CharBase, CharClasses, CharRaces, Spell
from .table_processing import ExportXLS
from .tasks import signer
from .xls_map_character import IMAGE_SIZES

from django.urls import reverse
from django.shortcuts import redirect


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
    characters = CharBase.objects.filter(owner=request.user)
    return render(request, 'main/profile.html', {'characters': characters})


@login_required
def view_character(request, character_name):
    ch = get_character_from_db(request, character_name)
    return render(request, 'main/character.html', {'char': ch})


@login_required
def get_spells(request):
    context = {
        'spells': '',
        'status': 0,
    }

    if request.method == 'GET':
        find_spell_form = FindSpellForm(request.GET)
        if find_spell_form.is_valid():
            find_options, spells_list_qs = Spell.spells.main_search(find_spell_form)
            if spells_list_qs.exists():
                spell_list = Spell.spells.spell_list(spells_list_qs)
                context = {
                    'spells': spell_list,
                    'status': spells_list_qs.count(),
                }
            return JsonResponse(context)


@login_required
def find_spells(request):
    spells_list_qs = None
    find_options = None

    if request.method == 'GET':
        find_spell_form = FindSpellForm(request.GET)
        if find_spell_form.is_valid():
            find_options, spells_list_qs = Spell.spells.main_search(find_spell_form)
        else:
            messages.add_message(request, messages.ERROR, find_spell_form.errors)

    page = request.GET.get('page')
    spells_limit_list = 8
    paginator = Paginator(spells_list_qs, spells_limit_list)
    try:
        spells_pages = paginator.page(page)
    except PageNotAnInteger:
        spells_pages = paginator.page(1)
    except EmptyPage:
        spells_pages = paginator.page(paginator.num_pages)

    print('find_spells -> find_options: ', find_options)
    context = {
        'spells': spells_pages,
        'parms': find_options,
        'spell_classes': CharClasses.get_classes_captions(),
        'spell_levels': Spell.get_spell_levels(),
        'spell_schools': Spell.get_spell_schools(),
    }
    return render(request, 'main/find-spells.html', context)


@login_required
def view_spell(request, spell_id):
    spell = get_object_or_404(Spell, id=spell_id)
    context = {'spell': spell}
    return render(request, 'main/view_spell.html', context)


@login_required
def create_character(request):
    if request.method == 'POST':
        character_form = CreateCharForm(request.POST)
        if character_form.is_valid():
            created_character_db = character_form.create_character(request)
            return redirect('main:edit_character', name=created_character_db.name)
        else:
            messages.add_message(request, messages.ERROR, character_form.errors)

    context = {
                'char_classes': CharClasses.get_classes_captions(),
                'char_races': CharRaces.get_races_captions(),
               }
    return render(request, 'main/create_character.html', context)


@login_required
def delete_character(request, character_name):
    if request.method == 'POST':
        delete_character_from_db(request, character_name)
        messages.add_message(request, messages.WARNING, 'Персонаж удалён')
        return redirect(reverse('main:profile'))
    context = {'character_name': character_name}
    return render(request, 'main/delete_character.html', context)


@login_required
def export_character(request, character_name):
    char_base = get_character_from_db(request, character_name)
    with ExportXLS(char_base) as export_xls:
        doc_name, output_stream = export_xls.generate_xls()
        response = HttpResponse(FileWrapper(output_stream), content_type=ExportXLS.CONTENT_TYPE)
        response['Content-Disposition'] = 'inline; filename="{}"'.format(doc_name)
        return response


@login_required
def edit_character(request, character_name):
    char_base = get_object_or_404(CharBase, owner=request.user, character_name=character_name)

    if request.method == 'POST':
        # Загрузка изображения
        for image_field, image_size in IMAGE_SIZES.items():
            print(f'Field: {image_field} - size: [{image_size}]')
            if bool(request.FILES.get(image_field, False)):
                print(f'image_field: {image_field}')
                avatar_form = UploadIconForm(request.POST, request.FILES)
                avatar_form.upload_icon(request, char_base, messages, image_field, image_size)
                return redirect('main:edit_character', character_name=char_base.character_name)

        char_form = CharForm(request.POST)
        if char_form.is_valid():
            char_form.edit_character(char_base, request)
            messages.add_message(request, messages.SUCCESS, 'Изменения сохранены')
            return redirect('main:edit_character', character_name=char_base.character_name)
        else:
            print("char_form NOT VALID. ERROR:\r\n", char_form.errors)
            messages.add_message(request, messages.WARNING, char_form.errors)

    context = {
                'form': char_base,
                'spells': Spell.spells.get_spell_names(),

                'char_classes': CharClasses.get_classes_captions(),
                'char_races': CharRaces.get_races_captions(),

                'cur_race': char_base.get_current_race(),
                'cur_class': char_base.get_current_class(),

                'spell_classes': CharClasses.get_classes_captions(),
                'spell_levels': Spell.get_spell_levels(),
                'spell_schools': Spell.get_spell_schools(),
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
