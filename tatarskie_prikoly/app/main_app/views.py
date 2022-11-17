import requests
from django.db.models import Count
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import TransactionHistory, TickerData
from .forms import TradeForm, TickerForm, CreateUserForm
from .filters import TransactionHistoryFilter
from .decorators import unauthenticated_user

############ AUTH PAGES URL ############

@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for {}'.format(user))
            return redirect('login')
        else:
            messages.info(request, form.errors)

    return render(request, 'auth/register.html', {'form': form})

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'auth/login.html', {})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

############ MAIN PAGES URL ############

@login_required(login_url='login')
def index(request):
    last_transactions = TransactionHistory.objects.all().order_by('-date')[:5]
    most_popular_buy  = TransactionHistory.objects.values('buy_currency').annotate(total=Count('buy_currency')).order_by('-total').first()
    most_popular_sell = TransactionHistory.objects.values('sell_currency').annotate(total=Count('sell_currency')).order_by('-total').first()
    user_last_login = request.user.last_login

    context = {
        'last_transactions': last_transactions,
        'most_popular_buy': most_popular_buy,
        'most_popular_sell': most_popular_sell,
        'user_last_login': user_last_login,
    }

    return render(request, 'index.html', context)

@login_required(login_url='login')
def transaction_history(request):
    transaction_history_data = TransactionHistory.objects.all()

    historyFilter = TransactionHistoryFilter(request.GET, queryset=transaction_history_data)
    transaction_history_data = historyFilter.qs

    context = {
        'history': transaction_history_data,
        'historyFilter': historyFilter,
    }

    return render(request, 'transaction_history.html', context)

@login_required(login_url='login')
def trade_regular_trade(request):
    form = TradeForm()
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            complete_order = TransactionHistory(**form.cleaned_data)
            complete_order.save()
            messages.success(request, ('Transaction completed successfully'))
            
            return redirect('transaction_history')
        else:
            messages.success(request, (form.errors))
    
        return redirect('trade_regular_trade')
    return render(request, 'trade_regular_trade.html', {'form': form})

@login_required(login_url='login')
def settings(request):
    ticker_form = TickerForm()
    ticker_currency_arr = TickerData.objects.all()

    context = {
        'ticker_form': ticker_form,
        'ticker_currency_arr': ticker_currency_arr
    }

    return render(request, 'settings.html', context)

############ BACKEND URL ############

@login_required(login_url='login')
@require_http_methods(['POST'])
def add_ticker(request):
    form = TickerForm(request.POST)
    if form.is_valid():
        ticker = TickerData(**form.cleaned_data)
        ticker.save()
    else:
        messages.error(request, form.errors)

    return redirect('settings')

@login_required(login_url='login')
@require_http_methods(['POST'])
def delete_ticker(request):
    for pk in request.POST.getlist('ticker_check'):
        ticker = get_object_or_404(TickerData, pk=pk)
        ticker.delete()

    return redirect('settings')

@login_required(login_url='login')
@require_http_methods(['POST'])
def delete_transaction_history(request):
    for pk in request.POST.getlist('transaction_check'):
        transation = get_object_or_404(TransactionHistory, pk=pk)
        transation.delete()

    return redirect('transaction_history')
