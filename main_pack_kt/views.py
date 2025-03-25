from django.shortcuts import render


# Create your views here.
def main_package(request):
    return render(request, 'main_pack_kt/main_package.html')