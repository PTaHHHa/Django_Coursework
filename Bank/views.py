from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from Bank.models import Profile
from Bank.forms import ProfileForm, ImageForm

# Create your views here.


def index(request):
    return render(request, "../templates/base.html")


def update_profile(request):
    if request.user.is_authenticated:
        try:
            p = request.user
            form = ProfileForm(request.POST or None, instance=p.profile)
            image = ImageForm(request.POST, request.FILES, instance=p.profile)
        except Profile.DoesNotExist:
            p = Profile(user=request.user)
            form = ProfileForm(request.POST or None, instance=p)
            image = ImageForm(request.POST, request.FILES, instance=p)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                image.save()
                messages.success(request, f'Your account has been updated')
                return redirect('profile')
    else:
        messages.error(request, 'You should login first')
        return redirect('index')
    return render(request, "../templates/update_profile.html", {'form': form})


@login_required
def user_profile(request):
    return render(request, "../templates/profile.html")


def delete_profile(request):
    b = Profile.objects.get(user=request.user)
    b.delete()
    logout(request)
    messages.success(request, 'Account was successfully deleted')
    return render(request, '../templates/base.html')
