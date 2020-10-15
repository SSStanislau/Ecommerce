from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm, SigninForm
from .models import edit_profile
from .signals import user_logged_in


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Profile created successfully')
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


class SignInView(FormView):
    form_class = SigninForm
    success_url = '/'
    template_name = 'registration/login.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            user_logged_in.send(user.__class__, instance=user, request=self.request)
            return redirect(self.success_url)
        return super(SignInView, self).form_invalid(self.form_class)


@login_required
def profile_edit_form(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'profile/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})
