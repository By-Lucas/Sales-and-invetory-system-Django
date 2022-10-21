from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed
import random



class Balance(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=9, default=0.00)
    date_order = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    def placeOrder(self):
        self.save()

    @staticmethod
    def get_sales_by_usuario(usuario_id):
        return Balance.objects.filter(user=usuario_id).order_by('amount')


    class Meta:
        db_table = 'balance'
        verbose_name = 'Saldo'
        verbose_name_plural = 'Saldos'
        ordering = ('-date_order',)


    def __str__(self) -> str:
        return f'{self.amount}'

