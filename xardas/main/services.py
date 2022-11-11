from django.shortcuts import get_object_or_404
from .models import CharBase


def get_character_from_db(request, character_name):
    return get_object_or_404(CharBase, owner=request.user, character_name=character_name)


def delete_character_from_db(request, character_name):
    character = get_character_from_db(request, character_name)
    character.delete()
    return
