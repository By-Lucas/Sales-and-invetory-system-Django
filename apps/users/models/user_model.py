from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


def upload_to(instance ,filename):
    return 'user/{username}/{filename}'.format(
        username=instance.user.username, filename=filename)

class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.IntegerField(null=True, blank=True, default=0, db_column='idade')
    cidade = models.CharField(max_length=20, null=True, blank=True, db_column='cidade')
    contato = models.CharField(max_length=11, null=True, blank=True, db_column='contato')
    endereco = models.CharField(max_length=20, null=True, blank=True, db_column='endereco')
    numero_casa = models.IntegerField(null=True, blank=True, db_column='numero_casa')
    data_nascimento = models.DateField(null=True, blank=True, db_column='data_nascimento')
    imagem_perfil = models.ImageField(default='usuario.png', upload_to=upload_to, null=True, blank=True, db_column='imagem_perfil')
    data_cadastro = models.DateTimeField(auto_now_add=True, db_column='data_cadastro')
    data_update = models.DateTimeField(auto_now=True, db_column='data_update')
    

    class Meta:
        db_table = 'profile_user'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return self.user.username 

    def register(self):
        self.save()

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)
    #instance.profile.save()