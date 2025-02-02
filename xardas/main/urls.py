from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views.register import BBLoginView, BBLogoutView
from .views.register import BBPasswordChangeView
from .views.register import ChangeUserInfoView
from .views.register import DeleteUserView
from .views.register import RegisterUserView, RegisterDoneView
from .views.register import user_activate
from .views.character import create_character
from .views.character import delete_character
from .views.character import export_character
from .views.character import edit_character
from .views.character import edit_character_spell
from .views.character import view_character
from .views.spells import view_spell
from .views.spells import find_spells
from .views.spells import get_spells
from .views.profile import profile
from .views.views import index, other_page


app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('char/create/', create_character, name='create_character'),
    path('char/<str:character_name>/spell/', edit_character_spell, name='edit_character_spell'),
    path('char/<str:character_name>/edit/', edit_character, name='edit_character'),
    path('char/<str:character_name>/export/', export_character, name='export_character'),
    path('char/<str:character_name>/delete/', delete_character, name='delete_character'),
    path('char/<str:character_name>/', view_character, name='view_character'),
    path('accounts/profile/spells/', find_spells, name='find_spells'),
    path('accounts/profile/get-spells/', get_spells, name='get_spells'),
    path('accounts/profile/spell/<int:spell_id>/', view_spell, name='view_spell'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)