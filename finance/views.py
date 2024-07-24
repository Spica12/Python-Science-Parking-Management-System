from django.shortcuts import render

# Create your views here.
def get_payments_list_by_user(request):

    return render(
        request,
        "finance/payments_list.html",
    )
