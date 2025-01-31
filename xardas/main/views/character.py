from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from wsgiref.util import FileWrapper
from main.forms import CharForm, CreateCharForm
from main.forms import UploadIconForm
from main.services import get_character_from_db, delete_character_from_db
from main.models import CharBase, CharClasses, CharRaces, Spell
from main.table_processing import ExportXLS
from main.xls_map_character import IMAGE_SIZES
from django.urls import reverse
from django.shortcuts import redirect


@login_required
def view_character(request, character_name):
    ch = get_character_from_db(request, character_name)
    return render(request, 'main/character.html', {'char': ch})


@login_required
def create_character(request):
    if request.method == 'POST':
        character_form = CreateCharForm(request.POST)
        if character_form.is_valid():
            created_character_db = character_form.create_character(request)
            return redirect('main:edit_character', character_name=created_character_db.character_name)
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
def edit_spell(request, character_name):
    char_base = get_object_or_404(CharBase, owner=request.user, character_name=character_name)
    spells = []
    if request.method == 'POST':
        spells = request.POST.getlist('spells[]')
        action = request.POST.get('action')

        print(f'Action: {action} - {spells}, {character_name}')
        for spell in spells:
            if action == 'Add':
                char_base.spells.add(get_object_or_404(Spell, name=spell))
            if action == 'Delete':
                char_base.spells.remove(get_object_or_404(Spell, name=spell))
    return JsonResponse({'status': 'success', 'spells': spells})


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
