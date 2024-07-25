from django.shortcuts import render


# Create your views here.
def main_page(request):
    # TODO Додати вивід поточного тарифу


    return render(request,"parking_service/index.html",)
