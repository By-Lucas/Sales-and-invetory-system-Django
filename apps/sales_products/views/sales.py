from multiprocessing import context
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib import messages
from django.contrib.messages import constants

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from sales_products.models.sales import SellProduct
from sales_products.models.balance import Balance
from products.models.products import Products
#from sales_products.forms.sales_form import SalesForm

from datetime import datetime, timedelta
from django.utils.timezone import utc

import csv


def calculate_balance():

    all_amount = 0
    day_amount = 0
    week_amount = 0
    month_amount = 0

    sell = SellProduct.objects.all()

    hoje = datetime.utcnow().replace(tzinfo=utc)
    semana = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=7)
    
    day = SellProduct.objects.filter(date_sale__range = [semana, hoje])
    n = 0
    for x in day:
        week_amount += x.amount
        n+=1
        print(x, n)

    days = []

    for sell_product in sell:
        days.append(sell_product.date_sale.day)
        all_amount += sell_product.amount
        
        if sell_product.date_sale.day == hoje.day :
            day_amount += sell_product.amount

        if sell_product.date_sale.month > 0 and sell_product.date_sale.month < 31:
            month_amount += sell_product.amount

        if sell_product.date_sale.hour % 23 == 0 and sell_product.date_sale.minute % 59 == 0:
            print(sell_product.date_sale )

    data = dict()
    data['day'] = day_amount
    data['week'] = week_amount
    data['month'] = month_amount
    data['all'] = all_amount

    return data


@login_required(login_url=reverse_lazy('login'))
def sell_produc(request):
    id = int(request.POST.get('id'))
    name = request.POST.get('name')
    user = request.user
    qtd = int(request.POST.get('quantity_sell'))
    value = float(request.POST.get('value').replace(',', '.'))

    get_balance = calculate_balance()
    amount = get_balance['all']
    amount_day = get_balance['day']
    amount_week = get_balance['week']
    amount_month = get_balance['month']

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
            balance = Balance.objects.create(amount=amount,
                                            amount_day=amount_day,
                                            amount_week=amount_week,
                                            amount_month=amount_month,
                                            )
        else:
            balance = Balance.objects.update(amount=amount,
                                            amount_day=amount_day,
                                            amount_week=amount_week,
                                            amount_month=amount_month,
                                            )
        
        messages.success(request, f"O produto '{name}' foi vendido")
        return redirect('products')

    else:
        messages.add_message(request, constants.ERROR, f"Erro ao fazer a venda do produto' {name}: {erro}")
        return redirect('products')


class ProductsSoldView(LoginRequiredMixin, ListView):
    template_name = 'products-solds.html'
    redirect_field_name = 'login'
    model = SellProduct

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        sell = SellProduct.objects.all().order_by('-date_sale')
        queryset = request.GET.get('q')
        print(queryset)
        if queryset:
            sell = SellProduct.objects.filter(
                Q(code_sale__icontains=queryset)|
                Q(quantity__icontains=queryset)|
                Q(amount__icontains=queryset)|
                Q(date_sale__icontains=queryset)
            )
        paginator = Paginator(sell, 10)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)

        context = dict()
        context['posts'] = posts
        
        return self.render_to_response(context)


class DeleteProductsSoldView(LoginRequiredMixin, DeleteView):
    model = SellProduct
    redirect_field_name = 'login'
    success_url = reverse_lazy('all_producs_sold')
    
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            messages.add_message(self.request, constants.SUCCESS, 'Venda deletada com sucesso.')
            return self.success_url.format(**self.object.__dict__)
        else:
            messages.add_message(self.request, constants.ERROR, 'Não foi possível deletar venda.')
            return self.success_url.format(**self.object.__dict__)


@login_required(login_url=reverse_lazy('login'))
def backup_products_sold(request):
    queryset = SellProduct.objects.all()
    options = SellProduct._meta
    fields = [field.name for field in options.fields]
    responde = HttpResponse(content_type='text/csv')
    responde['Content-Disposition'] = "atachment; filename:'vendas.csv'"
    write = csv.writer(responde)
    write.writerow([options.get_field(field).verbose_name for field in fields])
    for obj in queryset:
        write.writerow([getattr(obj, field) for field in fields])
    return responde