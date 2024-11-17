from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'page/home.html')

def about_us(request):
    return render(request, 'page/about_us.html')

def contact_us(request):
    return render(request, 'page/contact_us.html')