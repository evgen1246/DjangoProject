from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .forms import UserRegisterForm, UserLoginForm


class RegisterView(CreateView):
    """
    Представление для регистрации пользователя
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            send_mail(
                subject="Добро пожаловать в Skystore!",
                message=f"""
Здравствуйте, {self.object.email}!

Благодарим вас за регистрацию в нашем сервисе Skystore.


С уважением,
Команда Skystore
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
            )
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")

        messages.success(self.request, "Регистрация прошла успешно! На вашу почту отправлено приветственное письмо.")
        return response


class UserLoginView(LoginView):
    """
    Представление для авторизации пользователя по электронной почте и паролю
    """

    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли в систему!")
        return super().form_valid(form)


class CustomLogoutView(View):
    """Собственный контроллер для выхода с перенаправлением на главную"""

    def get(self, request):
        logout(request)
        messages.success(request, "Вы успешно вышли из системы!")
        return redirect("catalog:home")
