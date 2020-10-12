from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView

from .forms import UserRegistrationForm, MultiEditForm
from .models import edit_profile


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


class RegisterView(LoginRequiredMixin, FormView):
    template_name = "profile/edit.html"
    form_class = MultiEditForm
    success_url = 'shop:home'

    def form_valid(self, form):
        edit_profile(form, self.request.user)
        messages.success(self.request, 'Your profile was successfully changed')
        return HttpResponse('Well done')
