from django.shortcuts import render

# Create your views here.

def hotel_main(request):
    # Your dashboard view logic
    return render(request, 'hote_kt/hotel_main.html')