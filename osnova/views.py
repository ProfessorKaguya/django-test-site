from django.shortcuts import render
# Create your views here.

def home (request):
    return render(request, 'osnova/home.html')

def uslugi (request):
    return render(request, 'osnova/uslugi.html')
