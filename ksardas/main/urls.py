from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import BBLoginView, BBLogoutView
from .views import BBPasswordChangeView
from .views import ChangeUserInfoView
#from .views import CharCreateView
from .views import create_character
from .views import edit_character
from .views import edit_spell
from .views import DeleteUserView
from .views import index, other_page, profile
from .views import RegisterUserView, RegisterDoneView
from .views import view_spells
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
    #path('accounts/profile/char/create/', CharCreateView.as_view(), name='create_character'),
    path('accounts/profile/char/create/', create_character, name='create_character'),
    path('accounts/profile/char/<str:name>/edit/', edit_character, name='edit_character'),
    path('accounts/profile/char/<str:name>/', view_character, name='view_character'),
    path('accounts/profile/allspells/', view_spells, name='view_spells'),
    path('accounts/profile/editspell/<int:id>/', edit_spell, name='edit_spell'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)