# dwitter/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .forms import DweetForm, CustomUserCreationForm, CustomUserPasswordChangeForm
from .models import Dweet, Profile


def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                dweet = form.save(commit=False)
                dweet.user = request.user
                dweet.save()
                return redirect("dwitter:dashboard")
        followed_dweets = Dweet.objects.filter(
            user__profile__in=request.user.profile.follows.all()
        ).order_by("-created_at")

        return render(request, "dwitter/dashboard.html", {"form": form, "dweets": followed_dweets})
    else:
        return redirect("dwitter:login")

def profile_list(request):
    #profiles = Profile.objects.exclude(user=request.user) # não exibe o usuário atual
    profiles = Profile.objects.all() # exibe todos os usuários
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})

def register(request):
    if request.method == "GET":
        return render(request, "dwitter/register.html", {"form": CustomUserCreationForm, "msg": ""})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # form.full_clean()
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect("dwitter:dashboard")
        else:
            return render(request, "dwitter/register.html", {"form": form,
                                                             "msg": ""})

'''def password_change(request):
    form = CustomUserPasswordChangeForm(request.POST or None)
    if request.method == "GET":
        #form =  CustomUserPasswordChangeForm
        return render(request, "dwitter/password_change_form.html", {"form":  form, "msg": ""})
    else:
        #request.method = "POST"
        #form =  CustomUserPasswordChangeForm(request.POST)
        #form.full_clean()
        #if form.is_valid():
        form.save()
        return redirect("dwitter:dashboard")

            #return render(request, "dwitter/password_change_form.html", {"form": form, "msg": erros})
            #form.errors.as_data()'''

'''def password_change_done(self, request, extra_context=None):
        """
        Display the "success" page after a password change.
        """
        from django.contrib.auth.views import PasswordChangeDoneView

        defaults = {
            "extra_context": {**self.each_context(request), **(extra_context or {})},
        }
        if self.password_change_done_template is not None:
            defaults["template_name"] = self.password_change_done_template
        request.current_app = self.name
        return PasswordChangeDoneView.as_view(**defaults)(request)'''