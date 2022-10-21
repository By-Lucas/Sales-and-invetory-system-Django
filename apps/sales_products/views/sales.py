from venv import create
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User
from sales_products.models.sales import SellProduct


from products.models.products import Products



def sell_produc(request, *args, **kwargs):
    user = request.user
    id = request.POST.get('id')
    qtf = request.POST.get('quantity_sell')
    value = request.POST.get('quantity_value')

    amount = request.POST.get('amount')
    unit_price = request.POST.get('unit_price')

    order_status = True
    

    prod = Products.objects.filter(id=id)

    instance = SellProduct.objects.create(
                            product=prod, quantity=qtf)

    if instance is None:
        raise Http404("Esse produto não existe!")
    return instance