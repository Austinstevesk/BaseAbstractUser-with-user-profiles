from django.shortcuts import redirect, render
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages

# Create your views here.

def register(request):
    context = {}
    if request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created, you can now login')
            return redirect('/')
        context['register_form'] = form

    else:
        form = UserRegisterForm()
        context['register_form'] = form

    return render(request, 'users/register.html', context)


def login(request):
    return render(request, 'users/login.html')