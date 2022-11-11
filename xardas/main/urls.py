from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import BBLoginView, BBLogoutView
from .views import BBPasswordChangeView
from .views import ChangeUserInfoView
from .views import create_character
from .views import export_character
from .views import edit_character
from .views import view_spell
from .views import delete_character
from .views import DeleteUserView
from .views import index, other_page, profile
from .views import RegisterUserView, RegisterDoneView
from .views import find_spells
from .views import get_spells
from .views import user_activate
from .views import view_character

app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/char/create/', create_character, name='create_character'),
    path('accounts/profile/char/<str:character_name>/edit/', edit_character, name='edit_character'),
    path('accounts/profile/char/<str:character_name>/export/', export_character, name='export_character'),
    path('accounts/profile/char/<str:character_name>/delete/', delete_character, name='delete_character'),
    path('accounts/profile/char/<str:character_name>/', view_character, name='view_character'),
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