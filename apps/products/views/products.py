from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib import messages
from django.contrib.messages import constants

from sales_products.models.sales import SellProduct
from products.models.products import Products


import csv


class ProductsView(ListView):
    template_name = 'products.html'
    model = Products
    def get_queryset(self):
        #empresa_logada = self.request.user.funcionario.empresa
        return Products.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        producs = Products.objects.filter(status=True).order_by('-date_create')
        queryset = request.GET.get('q')
        print(queryset)
        if queryset:
            producs = Products.objects.filter(
                Q(code__icontains=queryset)|
                Q(name__icontains=queryset)|
                Q(value__icontains=queryset)|
                Q(status__icontains=queryset)
            )

        paginator = Paginator(producs, 10)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)

        context = dict()
        context['producs'] = posts
        
        return self.render_to_response(context)


class AllProductsView(ListView):
    template_name = 'all-products.html'
    model = Products
    def get_queryset(self):
        #empresa_logada = self.request.user.funcionario.empresa
        return Products.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        producs = Products.objects.all().order_by('-date_create')
        queryset = request.GET.get('q')
        print(queryset)
        if queryset:
            producs = Products.objects.filter(
                Q(code__icontains=queryset)|
                Q(name__icontains=queryset)|
                Q(value__icontains=queryset)|
                Q(status__icontains=queryset)
            )

        paginator = Paginator(producs, 10)
        page = self.request.GET.get('page')
        posts = paginator.get_page(page)

        context = dict()
        context['producs'] = posts
        
        return self.render_to_response(context)


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


def backup_products(request):
    queryset = Products.objects.all()
    options = Products._meta
    fields = [field.name for field in options.fields]
    responde = HttpResponse(content_type='text/csv')
    responde['Content-Disposition'] = "atachment; filename:'produtos.csv'"
    write = csv.writer(responde)
    write.writerow([options.get_field(field).verbose_name for field in fields])
    for obj in queryset:
        write.writerow([getattr(obj, field) for field in fields])
    return responde