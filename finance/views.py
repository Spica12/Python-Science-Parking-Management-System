from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.paginator import Paginator

from finance.forms import TariffForm
from finance.models import Tariff
from django.contrib.auth.decorators import login_required
from adminapp.decorators import admin_required, admin_or_operator_required


# Create your views here.
@login_required(login_url="login")
def get_payments_list_by_user(request):



    return render(
        request,
        "finance/payments_list.html",
    )

@admin_or_operator_required
def add_tariff(request):

    last_tariff = Tariff.objects.last()

    if request.method == "POST":
        form = TariffForm(request.POST)
        if form.is_valid():
            new_tariff = form.save(commit=False)
            if last_tariff:
                last_tariff.end_date = new_tariff.start_date - timezone.timedelta(days=1)
                last_tariff.save()
            new_tariff.save()
            return redirect("finance:tariffs_list")
    else:
        form = TariffForm()

    return render(request, "finance/tariffs_add.html", {"form": form})

@login_required(login_url="login")
def get_tariffs_list(request):

    tariffs = Tariff.objects.all().order_by('-start_date')

    paginator = Paginator(tariffs, 10)  # Показувати 10 рядків на сторінці
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "finance/tariffs_list.html", {"page_obj": page_obj})

@admin_or_operator_required
def delete_tariff(request, pk):

    try:
        tariff = Tariff.objects.get(pk=pk)
    except Tariff.DoesNotExist:
        tariff = None

    if tariff:
        tariff.delete()

    return redirect("finance:tariffs_list")
