from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed
import random

from products.models.products import Products
from cart.models.cart_models import Cart
from .balance import Balance


def generate_id():
    tamanho = 10
    valores = '1234567890'
    code = ''
    for i in range(tamanho):
        code += random.choice(valores)
    return code


class SellProduct(models.Model):
    code_sale = models.IntegerField(default=generate_id, editable=False)
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=265, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, editable=False)
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, editable=False)
    order_status = models.BooleanField(default=True)
    date_sale = models.DateTimeField(auto_now_add=True)

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
        return f'{self.id}'


def pre_save_sales_receiver(sender, instance, *args, **kwargs):
    #if action == 'post_add' or action == 'post_remove' or action == 'post_clear':

    if instance.order_status == True:
        instance.amount =  instance.amount 
        instance.unit_price =  instance.unit_price
    else:
        instance.amount = instance.amount

pre_save.connect(pre_save_sales_receiver, sender = SellProduct)