from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.urls import reverse
import random
from PIL import Image


def upload_to(instance ,filename):
    return 'products/{username}/{filename}'.format(
        username=instance.name, filename=filename)


def gerar_id():
        tamanho = 10
        valores = '1234567890'
        code = ''
        for i in range(tamanho):
            code += random.choice(valores)
        return code


class Products(models.Model):

    code = models.IntegerField(default=gerar_id, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    status = models.BooleanField(default=True)
    image = models.ImageField(upload_to=upload_to, default='img.png', null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    """Aqui servirá para mostrar apenas produtos do usuario"""
    @staticmethod
    def get_produts_by_user(usuario_id):
        return Products.objects.filter(created_by=usuario_id).order_by('-date_update')

    class Meta:
        db_table = 'products'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ('-date_create',)

    
    def __str__(self) -> str:
        return self.name


    def get_absolute_url(self):
        return reverse('products')

    
    def save(self, *args, **kwargs):
        super(Products, self).save(*args, **kwargs)
        imag = Image.open(self.image.path)
        if imag.width > 200 or imag.height> 200:
            output_size = (200, 200)
            imag.thumbnail(output_size)
            imag.save(self.image.path)


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    #products = instance.produto.all()
    
    if instance.code:
        # considere o 10 como uma taxa de entrega
        print(instance.name)
    else:
        instance.value = 0.00
    
        
pre_save.connect(pre_save_product_receiver, sender = Products)