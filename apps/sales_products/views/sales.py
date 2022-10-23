from venv import create
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

from sales_products.models.sales import SellProduct
from products.models.products import Products
from sales_products.forms.sales_form import SalesForm


class SellProductView(CreateView):
    #template_name = "create-product.html"
    model = SellProduct
    fields=['product', 'quantity']

    def form_valid(self, form):
        if form.is_valid():
            id = self.request.POST.get('product')
            prod = Products.objects.filter(id=id)

            by_user = form.save(commit=False)
            by_user.sold_by = self.request.user
            by_user.product = prod
            by_user.quantity = self.request.POST.get('quantity_sell')
            by_user.save()

            messages.success(self.request, f"O produto '{by_user.name}' foi vendido")
            return super(SellProductView, self).form_valid(form)
        else:
             messages.add_message(self.request, constants.ERROR, f"O produto '{by_user.name}' deu erro na venda.")


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

        messages.success(request, f"O produto '{name}' foi vendido")
        return redirect('products')

    else:
        messages.add_message(request, constants.ERROR, f"Erro ao fazer a venda do produto' {name}: {erro}")
        return redirect('products')