from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('myuser', 'default cookie')
    return HttpResponse(f'Got cookie value: <i>{value}</i>')


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('<h2><i>Cookie set successfully!</i></h2>')
    response.set_cookie('myuser', 'mycookie', max_age=3600)
    return response


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('myuser', 'default session')
    return HttpResponse(f'Got session value: <i>{value}</i>')


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['myuser'] = 'mysession'
    return HttpResponse(f'<h2><i>Session set successfully</i></h2>')
