from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker_sym'] 
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_dc347bfe6e2446899144d051448ffbc7")
        try:
            api = json.loads(api_request.content)
            # return render(request, "home.html", {'api':api})
        except Exception as e:
            api = "Error"
        return render(request, "home.html", {'api':api})
    else:
        return render(request, "home.html", {'ticker':"Enter a ticker above"})

def add_stock(request):
    ticker = Stock.objects.all()

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added."))
            return redirect('add_stock')

        else:
            return render(request, "add_stock.html", {"ticker":ticker})

    else:
        return render(request, "add_stock.html", {"ticker":ticker})

def about(request):
    return render(request, "about.html", {})