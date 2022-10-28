from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, ListView

from django.views.decorators.http import require_POST
from django.urls import reverse_lazy

from cart.models.cart_models import Cart
from products.models.products import Products



def home_carrinho(request):
    cart = Cart.objects.all().order_by('-data_hora')

    #SABER SE EXITE CARRINHO
    cart_id = request.session.get("carrinho_id", None)
    print('CARRINHO',cart_id)
    if cart_id is None:
        #cart_obj = Carrinho.objects.new_or_get(request)
        print('Novo carrinho criado')
        request.session['carrinho_id'] = 12
    else:
        print("Cart ID exists")
    context = {
        'cart':cart,
    }

    request.session['cart'] = cart

    print(cart)

    return render(request, 'products.html', context)


def cart_update(request):
    print(request.POST)
    quantity_sell = request.POST['quantity_sell']
    cart_obj = Cart.objects.all() 
    total = cart_obj
    #print('SUPOER TESTE', total)

    produto_id = request.POST.get('produto_id')
    
    if produto_id is not None:
        try:
            produto_obj = Products.objects.get(id = produto_id)
        except Products.DoesNotExist:
            print("Mostrar mensagem ao usuário, esse produto acabou!")
            return redirect("products")

        cart_obj, new_obj = Cart.objects.new_or_get(request, quantity_sell) 
        if produto_obj in cart_obj.produto.all():
            cart_obj.produto.remove(produto_obj) # cart_obj.products.remove(product_id)
            #cart_obj.produto.add(produto_obj)
            print('Removido',cart_obj)
        else:
            # E o produto se adiciona a instância do campo M2M 
            cart_obj.produto.add(produto_obj) # cart_obj.products.add(product_id)
        qtd = 0
        for produto_qtd in cart_obj.produto.all():
            qtd+=1
        print('RRRR',qtd)
        request.session['cart_items'] = qtd

        #print(produto_qtd.count())

    return redirect("products")


def cart_remove(request, pk):
    cart = Cart(request)
    produto = get_object_or_404(Products, id=pk)
    cart.remove(produto)
    return redirect('products')