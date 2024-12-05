from django.shortcuts import render

# Create your views here.
def home(response):
    return render (response, "blog/home.html", {})

def login(response):
    return render(response, "blog/login.html", {})

def posts(response):
    return render(response, "blog/posts.html", {})

def register(response):
    return render(response, "blog/register.html", {})