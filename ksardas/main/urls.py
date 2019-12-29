from django.urls import path

from .views import BBLoginView, BBLogoutView
from .views import BBPasswordChangeView
from .views import ChangeUserInfoView
from .views import CharCreateView
from .views import edit_character
from .views import DeleteUserView
from .views import index, other_page, profile
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import profile_character

app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/char/create/', CharCreateView.as_view(), name='create_character'),
    path('accounts/profile/char/<str:name>/edit/', edit_character, name='edit_character'),
    path('accounts/profile/char/<str:name>/', profile_character, name='profile_character'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('<str:page>/', other_page, name='other'),
    path('',index, name='index'),
]