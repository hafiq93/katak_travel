from django.shortcuts import render

# Create your views here.
# Create your views here.
def dashboard(request):
    return render(request, 'merchant_kt/merchant_dashboard.html')  # Add your template