from django.shortcuts import redirect, render
from django.utils import timezone

from finance.forms import TariffForm
from finance.models import Tariff
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
def get_payments_list_by_user(request):



    return render(
        request,
        "finance/payments_list.html",
    )

@login_required(login_url="login")
def add_tariff(request):
    # TODO Додати перевірку чи адмін, якщо ні, то перевести на головну сторінку

    last_tariff = Tariff.objects.last()

    if request.method == "POST":
        form = TariffForm(request.POST)
        if form.is_valid():
            new_tariff = form.save(commit=False)
            if last_tariff:
                last_tariff.end_date =new_tariff.start_date - timezone.timedelta(seconds=1)
                last_tariff.save()
            new_tariff.save()
            return redirect("finance:payments_list_by_user")
    else:
        form = TariffForm()

    return render(request, "finance/tariffs_add.html", {"form": form})

@login_required(login_url="login")
def get_tariffs_list(request):

    tariffs = Tariff.objects.all()

    return render(request, "finance/tariffs_list.html", {"tariffs": tariffs})

@login_required(login_url="login")
def delete_tariff(request, pk):

    try:
        tariff = Tariff.objects.get(pk=pk)
    except Tariff.DoesNotExist:
        tariff = None

    if tariff:
        tariff.delete()

    return redirect("finance:tariffs_list")
