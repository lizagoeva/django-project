from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView, TemplateView
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import Profile
from django.contrib.auth.mixins import UserPassesTestMixin


class ProfilesListView(ListView):
    queryset = Profile.objects.select_related('user').order_by('user')
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    queryset = Profile.objects.select_related('user')


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        profile_owner = self.get_object().user
        return self.request.user.is_staff or profile_owner == self.request.user

    model = Profile
    fields = 'avatar', 'bio', 'agreement_accepted'
    template_name = 'myauth/profile-update.html'

    def get_success_url(self):
        return reverse(
            'myauth:profile_details',
            kwargs={'pk': self.object.pk},
        )


class ProfileView(TemplateView):
    template_name = 'myauth/about-me.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(self.request, user=user)
        return response


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
