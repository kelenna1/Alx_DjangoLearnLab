from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(response):
    return render (response, "blog/home.html", {})

def login(response):
    return render(response, "blog/login.html", {})

def posts(response):
    return render(response, "blog/posts.html", {})

def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, "Registration succesful. You can proceed to log in.")
        return redirect("login")
    else:
        form = RegisterForm()
    return render(response, "blog/register.html", {'form': form})

@login_required
def profile(response):
    return render (response, "blog/profile.html", {})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')
    return render(request, 'blog/edit_profile.html', {'user': request.user})