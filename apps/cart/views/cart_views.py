from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, ListView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.messages import constants

from datetime import datetime, timedelta
from django.utils.timezone import utc

from cart.models.cart_models import Cart
from cart.forms.cart_forms import CartForm
from products.models.products import Products
from sales_products.models.sales import SellProduct



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

    return render(request, 'base.html', context)


def valor(valor):
    soma = 0
    for numero in valor:
        soma += numero
    print(soma, ' Somando')
    return soma


def cart_update(request):
    print(request.POST)
    valor_total = []

    quantity_sell = int(request.POST['quantity'])
    value = request.POST['value'].replace(',', '.')

    valor_total.append(quantity_sell * float(value))
    
    valor(valor_total)

    print(f'Valor = {str(valor_total)}')

    produto_id = request.POST.get('produto_id')

    
    if produto_id is not None:
        try:
            produto_obj = Products.objects.get(id= produto_id)
        except Products.DoesNotExist:
            print("Mostrar mensagem ao usuário, esse produto acabou!")
            return redirect("products")

        cart_obj, new_obj = Cart.objects.new_or_get(request) 
        if produto_obj in cart_obj.produto.all():
            cart_obj.produto.remove(produto_obj)
            #cart_obj.produto.add(produto_obj)
        else:
            # E o produto se adiciona a instância do campo M2M 
           cart_obj.produto.add(produto_obj)
           cart_add = Cart.objects.update(valor_total = 10)

        qtd = 0
        for produto_qtd in cart_obj.produto.all():
            qtd+=1
            
        request.session['cart_items'] = qtd

    return redirect("products")


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


@require_POST
def cart_add(request, pk):

    print(request.POST)
    id = request.POST.get('product_id')
    cart_id = int(request.POST.get('cart_id'))
    user = request.user
    qtd = request.POST.get('quantity')
    value = float(request.POST.get('value').replace(',', '.'))
    amount = int(qtd) * value

    cart=Cart(request)
    produto = get_object_or_404(SellProduct, id=pk)
    form = CartForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(produto=produto, quantidade=cd['quantidade'],overrride_quantity=cd['override'])
    return redirect('products')


@require_POST
def sell_product(request):

    print(request.POST)
    id = request.POST.get('product_id')
    cart_id = int(request.POST.get('cart_id'))
    user = request.user
    qtd = request.POST.get('quantity')
    value = float(request.POST.get('value').replace(',', '.'))
    amount = int(qtd) * value


    carts = Cart.objects.filter(id= cart_id)
    produtos = ''
    for cart in carts:
        for prod in cart.produto.all():
            produtos += f'{prod.name}, '
        
        erro = None
        if any([int(qtd) <= 0, value <= 0]):
            erro = 'A quantidade ou valor do produto deve ser maior que 0'

        if user.is_authenticated:
            venda = SellProduct.objects.create(
                sold_by=user, product=produtos,
                quantity=int(qtd), unit_price=value,
                order_status=True, amount=amount
            )
    print(venda)

    return venda




def cart_remove(request, pk):
    try:
        cart , new_obj = Cart.objects.new_or_get(request) 
        produto = get_object_or_404(Products, id=pk)
        cart.produto.remove(produto)
        messages.add_message(request, constants.SUCCESS, 'Produto removido com sucesso')

    except Exception as e:
        messages.error(request, constants.ERROR, 'Erro ao remover, erro: ', e)
    return redirect('products')