from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .basket import Basket
from store.models import Product


# Create your views here.
def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basketSummary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        response = JsonResponse({'Success': True})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty':basketqty, 'subtotal':baskettotal})
        return response

@login_required
def startOrder(request):
    basket = Basket(request)
    basketqty = basket.__len__()
    baskettotal = basket.get_total_price()

    context = {'basket': basket, 'basketqty': basketqty, 'baskettotal': baskettotal }

    return render(request, 'store/startOrder.html', context)