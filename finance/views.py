from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.paginator import Paginator

from finance.forms import DepositForm, TariffForm
from finance.models import Account, Tariff, Payment
from django.contrib.auth.decorators import login_required
from adminapp.decorators import admin_required, admin_or_operator_required


# Create your views here.
@login_required(login_url="login")
def get_payments_list_by_user(request):

    payments = Payment.objects.all()

    paginator = Paginator(payments, 10)  # Показувати 10 рядків на сторінці
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, "finance/payments_list.html", context=context)

@admin_or_operator_required
def delete_payment(request, pk):

    try:
        payment = Payment.objects.get(pk=pk)
        payment.delete()
    except Tariff.DoesNotExist:
        payment = None

    return redirect("finance:payments_list_by_user")


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

@login_required(login_url="login")
def get_my_account(request):
    user = request.user
    account = Account.objects.get(user=user)

    context = {
        'account': account,
    }
    return render(request, "finance/account_my.html", context=context)

@login_required(login_url="login")
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.deposit(amount)
            # messages.success(request, f'Ваш рахунок було поповнено на {amount} {CURRENCY}.')
            return redirect('finance:account_my')  # Замініть 'some_view' на ваш URL
    else:
        form = DepositForm()

    return render(request, 'finance/account_deposit.html', {'form': form})
