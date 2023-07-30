from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MyLogoutView,
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    ProfileView,
    RegisterView,
)

app_name = 'myauth'
urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,
        ),
        name='login'
    ),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about-me/', ProfileView.as_view(), name='about_me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cookie/get/', get_cookie_view, name='get_cookie'),
    path('cookie/set/', set_cookie_view, name='set_cookie'),
    path('session/get/', get_session_view, name='get_session'),
    path('session/set/', set_session_view, name='set_session'),
]
