from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy



class ProductsView(TemplateView):
    template_name = 'products.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    def get(self, request):
        #carrinho = Carrinho.objects.all()
        #produtos = ProdutoModel.objects.all()
        context = {
            'produtos': 'produtos',
            'carrinho':'carrinho'
        }
        return render(request, self.template_name, context)


class CreateProductView(CreateView):
    template_name = 'create-product.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    def get(self, request):
        #carrinho = Carrinho.objects.all()
        #produtos = ProdutoModel.objects.all()
        context = {
            'produtos': 'produtos',
            'carrinho':'carrinho'
        }
        return render(request, self.template_name, context)