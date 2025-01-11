from django.http import HttpResponse

def merchant_home(request):
    return HttpResponse("Admin Home Page")