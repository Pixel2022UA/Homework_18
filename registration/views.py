from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import SignUpForm
from .tokens import account_activation_token


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string(
                "account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "id": user.pk,
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user("Verify registration", message)
            return HttpResponse(
                f"We have sent you an email, follow the link in the email to verify your account."
            )
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def activate(request, id, token):
    try:
        user = User.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("index")
    else:
        return render(request, "account_activation_invalid.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect("index")
        else:
            return HttpResponse("This user is not activated or does not exist")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def index(request):
    return render(request, "index.html", {"user": request.user})
