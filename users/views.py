from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        # Отправка приветственного письма
        send_mail(
            'Добро пожаловать в магазин!',
            f'Спасибо за регистрацию, {user.email}!',
            'noreply@store.com',
            [user.email],
            fail_silently=False,
        )
        login(self.request, user)
        return redirect(self.success_url)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')


def logout_view(request):
    logout(request)
    return redirect('catalog:home')
