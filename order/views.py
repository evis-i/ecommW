from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from basket.basket import Basket
from .models import Order, OrderItem

from account.models import UserBase


# Create your views here.


@login_required
def placeorder(request):
    basket = Basket(request)
    if request.method == 'POST':
        userObj = UserBase.objects.filter(id=request.user.id).first()
        if not userObj.first_name:
            userObj.first_name = request.POST.get('fname')
        if not userObj.last_name:
            userObj.last_name = request.POST.get('lname')
        if not userObj.phone_number:
            userObj.phone_number = request.POST.get('phone')
        if not userObj.postcode:
            userObj.postcode = request.POST.get('zipcode')
        if not userObj.town_city:
            userObj.town_city = request.POST.get('city')
        if not userObj.country:
            userObj.country = request.POST.get('country')
        if not userObj.address_line_1:
            userObj.address_line_1 = request.POST.get('addressline1')
        if not userObj.address_line_2:
            userObj.address_line_2 = request.POST.get('addressline2')

        userObj.save()

        neworder = Order()
        neworder.user = request.user
        neworder.first_name = request.POST.get('fname')
        neworder.last_name = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.postcode = request.POST.get('zipcode')
        neworder.country = request.POST.get('country')
        neworder.town_city = request.POST.get('city')
        neworder.address_line_1 = request.POST.get('addressline1')
        neworder.address_line_2 = request.POST.get('addressline2')
        neworder.amount = basket.get_total_price()
        neworder.save()

        for item in basket:
            #print(item)
            product = item['product']
            quantity = int(item['qty'])
            price = product.price

            OrderItem.objects.create(
                order=neworder,
                product=product,
                price=price,
                quantity=quantity
            )
        basket.clear()

        return redirect('account:dashboard')

    return redirect('basket:basket_summary')
