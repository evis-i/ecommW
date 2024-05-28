from django.shortcuts import render, get_object_or_404

from .models import Category, Product


# Create your views here.


def all_products(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'store/home.html', {'products': products})


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/productDetails.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/productsPerCat.html', {'products': products,
                                                              'category': category})
