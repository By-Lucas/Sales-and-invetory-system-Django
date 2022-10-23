from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

from sales_products.models.sales import SellProduct
from sales_products.models.balance import Balance
from products.models.products import Products
from sales_products.forms.sales_form import SalesForm

from datetime import datetime, timedelta


def calculate_balance():
    sell = SellProduct.objects.all()

    all_amount = 0
    day_amount = 0
    week_amount = 0
    month_amount = 0

    days = []

    for sell_product in sell:
        all_amount += sell_product.amount
        days.append(sell_product.date_sale.day)

        if sell_product.date_sale.hour > 0 and sell_product.date_sale.hour < 23  and sell_product.date_sale.minute > 1 and sell_product.date_sale.minute < 59 :
            day_amount += sell_product.amount

        if len(days[0:7]) > 0:
            week_amount += sell_product.amount
        
        if sell_product.date_sale.month > 0 and sell_product.date_sale.month < 31  or sell_product.date_sale.month < 28 or sell_product.date_sale.month  < 29 or sell_product.date_sale.month  < 30 :
            month_amount += sell_product.amount

        if sell_product.date_sale.hour % 23 == 0 and sell_product.date_sale.minute % 59 == 0:
            print(sell_product.date_sale )

    data = dict()
    data['day'] = day_amount
    data['week'] = week_amount
    data['month'] = month_amount
    data['all'] = all_amount
    print(data)

    return data


def sell_produc(request):

    id = int(request.POST.get('id'))
    name = request.POST.get('name')
    user = request.user
    qtd = int(request.POST.get('quantity_sell'))
    value = float(request.POST.get('value').replace(',', '.'))

    prod = Products.objects.get(id=id)

    erro = None
    if any([qtd <= 0, value <= 0]):
        erro = 'A quantidade ou valor do produto deve ser maior que 0'

    if all([erro == None, id > 0, name != '', user != '']):
        venda = SellProduct.objects.create(
            sold_by=user, product=prod,
            quantity=qtd,
            order_status=True
        )
        if not Balance.objects.exists():
            balance = Balance.objects.create(amount=calculate_balance()['all'],
                                            amount_day=calculate_balance()['day'],
                                            amount_week=calculate_balance()['week'],
                                            amount_month=calculate_balance()['month'],
                                            )
        else:
            balance = Balance.objects.update(amount=calculate_balance()['all'],
                                            amount_day=calculate_balance()['day'],
                                            amount_week=calculate_balance()['week'],
                                            amount_month=calculate_balance()['month'],
                                            )
        
        messages.success(request, f"O produto '{name}' foi vendido")
        return redirect('products')

    else:
        messages.add_message(request, constants.ERROR, f"Erro ao fazer a venda do produto' {name}: {erro}")
        return redirect('products')