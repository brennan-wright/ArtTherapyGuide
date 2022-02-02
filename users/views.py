from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views.generic import View

from .forms import UserChangeUsernameForm, UserDeleteForm

# Create your views here.


@login_required
def profile_view(request, *args, **kwargs):
    from directive.models import DirectivePage
    user = request.user
    directive_page = DirectivePage.objects.filter(
        posted_by=user).order_by('-id')
    context = {
        'directive_page': directive_page,
    }
    return render(request, 'users/profile.html', context)


class UserDeleteView(LoginRequiredMixin, View):
    """
    Deletes the currently signed-in user and all associated data.
    """

    def get(self, request, *args, **kwargs):
        form = UserDeleteForm()
        return render(request, 'users/user_deletion.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserDeleteForm(request.POST)
        # Form will be valid if checkbox is checked.
        if form.is_valid():
            user = request.user
            # Logout before we delete. This will make request.user
            # unavailable (or actually, it points to AnonymousUser).
            logout(request)
            # Delete user (and any associated ForeignKeys, according to
            # on_delete parameters).
            user.delete()
            messages.success(request, 'Account successfully deleted')
            return redirect('/')


class UserChangeUsernameView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = UserChangeUsernameForm(instance=request.user)
        return render(request, 'users/user_changeusername.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserChangeUsernameForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return reverse('profile')
        return render(request, 'users/user_changeusername.html', {'form': form})
