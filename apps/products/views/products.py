from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

from sales_products.models.sales import SellProduct
from products.models.products import Products


class ProductsView(ListView):
    template_name = 'products.html'
    model = Products
    def get_queryset(self):
        #empresa_logada = self.request.user.funcionario.empresa
        return Products.objects.all()


class ProductDetailView(DetailView):
    template_name = "detail-products.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('id')
        print(pk)
        instance = Products.objects.filter(pk=pk)
        print(instance)
        if instance is None:
            raise Http404("Esse produto não existe!")
        return instance


class EditproductView(UpdateView):
    template_name = "edit-product.html"
    model = Products
    fields=['name', 'value', 
            'quantity', 'status', 
            'image']

    def form_valid(self, form) -> HttpResponse:
        if form.is_valid():
            by_user = form.save(commit=False)
            by_user.created_by = self.request.user
            by_user.save()

            messages.add_message(self.request, constants.SUCCESS, f"O produto '{by_user.name}' atualizado com sucesso.")
            return super(EditproductView, self).form_valid(form)
        else:
             messages.add_message(self.request, constants.ERROR, "Produto não pôde ser atualizado.")


class CreateProductView(CreateView):
    template_name = "create-product.html"
    model = Products
    fields=['name', 'value', 
            'quantity', 'status', 
            'image']

    def form_valid(self, form):
        if form.is_valid():
            by_user = form.save(commit=False)
            by_user.created_by = self.request.user
            by_user.save()

            messages.success(self.request, f"O produto '{by_user.name}' cadastrado com sucesso.")
            return super(CreateProductView, self).form_valid(form)
        else:
             messages.add_message(self.request, constants.ERROR, f"O produto {by_user.name} não pôde ser cadastrado.")


class DeleteProductView(DeleteView):
    model = Products
    success_url = reverse_lazy('products')