from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import UserDeleteForm

# Create your views here.


@login_required
def ProfileView(request, *args, **kwargs):
    return render(request, 'users/profile.html')


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
