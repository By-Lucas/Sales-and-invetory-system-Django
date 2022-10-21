from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User
from sales_products.models.sales import SellProduct


from products.models.products import Products



class ProductsView(TemplateView):
    template_name = 'products.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    def get(self, request):
        produtos = Products.objects.all()
        context = {
            'products': produtos,
        }
        return render(request, self.template_name, context)


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


class CreateProductView(CreateView):
    template_name = "create-product.html"
    model = Products
    fields=['name', 'value', 
            'quantity', 'status', 
            'image']

    def form_valid(self, form):
        #Enviar o commit mas nao salvar no banco ate ser feito algumas coisas antes
        prod = form.save(commit=False)
        prod.save()
        return super(CreateProductView, self).form_valid(form)


class DeleteProductView(DeleteView):
    model = Products
    success_url = reverse_lazy('products')