from django.shortcuts import redirect, render
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_form.is_valid():
            user_update_form.save()
            profile_form.save()
            messages.success(request, f'{user.username} profile updated')
            return redirect('profile')

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': user_update_form,
        'p_form': profile_form
    }

    return render(request, 'users/profile.html', context)


def login(request):
    return render(request, 'users/login.html')