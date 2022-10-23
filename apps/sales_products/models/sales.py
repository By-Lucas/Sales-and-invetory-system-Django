from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed
import random

from products.models.products import Products
from .balance import Balance


def generate_id():
    tamanho = 10
    valores = '1234567890'
    code = ''
    for i in range(tamanho):
        code += random.choice(valores)
    return code


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("product_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        print('SRSRS',qs)
        if qs.count() == 1:
            print('SRSRS',qs)
            new_obj = False
            cart_obj = qs.first()
            
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Products.objects.new(user=request.user)
            new_obj = True
            request.session['products_id'] = cart_obj.id
        return cart_obj, new_obj
    
    def get(self, request):
        cart_id = request.session.get("product_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        return qs

    def new(self, user = None):
        user_obj = None
        if not user is None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)



class SellProduct(models.Model):
    code_sale = models.IntegerField(default=generate_id, editable=False)
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, editable=False)
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, editable=False)
    order_status = models.BooleanField(default=True)
    date_sale = models.DateTimeField(auto_now_add=True)


    objects = CartManager()

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_sales_by_usuario(usuario_id):
        return SellProduct.objects.filter(user=usuario_id).order_by('-date_sale')


    class Meta:
        db_table = 'sales'
        verbose_name = 'Produtos vendidos'
        verbose_name_plural = 'Produtos vendidos'
        ordering = ('-date_sale',)


    def __str__(self) -> str:
        return self.product.name


def pre_save_sales_receiver(sender, instance, *args, **kwargs):
    #if action == 'post_add' or action == 'post_remove' or action == 'post_clear':

    if instance.order_status == True:
        instance.amount =  (instance.quantity * instance.product.value)
        instance.unit_price =  instance.product.value
        
    else:
        instance.amount = instance.amount

pre_save.connect(pre_save_sales_receiver, sender = SellProduct)