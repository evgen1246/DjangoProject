from django.urls import path
from . import views
from .apps import UsersConfig
from .views import CustomLogoutView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
