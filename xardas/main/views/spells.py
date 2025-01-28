from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from main.forms import FindSpellForm
from main.models import CharClasses, Spell


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
