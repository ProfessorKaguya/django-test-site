from django.shortcuts import render, redirect

# Create your views here.
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileImageForm, ProfileSexForm, ProfileAgreedForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользователь {username} успешно зарегистрирован')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/registration.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        update_user_form = UserUpdateForm(request.POST, instance=request.user)
        agreed_form = ProfileAgreedForm(request.POST, instance=request.user.profile)
        sex_form = ProfileSexForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid() and update_user_form.is_valid() and sex_form.is_valid() and agreed_form.is_valid():
            update_user_form.save()
            profile_form.save()
            sex_form.save()
            agreed_form.save()
            messages.success (request, "Вы успешно обновили аккаунт")
            return redirect('profile')
    else:
        profile_form = ProfileImageForm(instance=request.user.profile)
        update_user_form = UserUpdateForm(instance=request.user)
        sex_form = ProfileSexForm(instance=request.user.profile)
        agreed_form = ProfileAgreedForm(instance=request.user.profile)
    data = {
        'profile_form': profile_form,
        'update_user_form': update_user_form,
        'sex_form': sex_form,
        'agreed_form': agreed_form

        }
    return render(request, 'users/profile.html', data)