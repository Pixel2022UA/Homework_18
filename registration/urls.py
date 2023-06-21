from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("registration/", views.signup, name="registration"),
    path(
        "activate/<str:id>/<str:token>/",
        views.activate,
        name="activate",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login")
]
