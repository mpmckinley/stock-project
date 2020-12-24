from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Stock
from .forms import StockForm

def home(request):
    import requests
    import json

    if request.method == 'POST':
        ticker = request.POST['ticker_sym'] 
        # ***USING SANDBOX TOKEN (replace URL 'sandbox' with 'cloud')***
        api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + ticker + "/quote?token=Tpk_1ef07fc95dc746f2a89346f3613d1982")
        try:
            api = json.loads(api_request.content)
            # return render(request, "home.html", {'api':api})
        except Exception as e:
            api = "Error"
        return render(request, "home.html", {'api':api})
    else:
        return render(request, "home.html", {'ticker':"Enter a ticker above"})

def watchlist(request):
    import requests
    import json

    stocks = Stock.objects.all()

    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added."))
            return redirect('watchlist')

        else:
            return render(request, "watchlist.html", {"stocks":stocks})

    else:
        output = []
        for stock_item in stocks:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(stock_item) + "/quote?token=pk_dc347bfe6e2446899144d051448ffbc7")
            # SANDBOX
            # api_request = requests.get("https://sandbox.iexapis.com/stable/stock/" + str(stock_item) + "/quote?token=Tpk_1ef07fc95dc746f2a89346f3613d1982")
            
            try:
                api = json.loads(api_request.content)
                output.append(api)
                # return render(request, "home.html", {'api':api})
            except Exception as e:
                api = "Error"

        return render(request, "watchlist.html", {"stocks":stocks, "output":output})

def delete(request, stock_pk):
    stock = get_object_or_404(Stock, pk=stock_pk)
    if request.method == "POST":
        stock.delete()
        messages.success(request, ("Ticker Deleted."))
        return redirect('watchlist')

def about(request):
    return render(request, "about.html", {})