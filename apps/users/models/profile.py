from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def upload_to(instance ,filename):
    return 'user-profile/{username}/{filename}'.format(
        username=instance.user, filename=filename)


class ProfileUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_nome = models.CharField(max_length=100, null=False, blank=False)
    photo_user = models.FileField(upload_to=upload_to, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=False)
    email = models.CharField(max_length=70, null=True, blank=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'profile_user'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


    def __str__(self) -> str:
        if self.full_nome:
            return self.full_nome
        else:
            return self.user


    def register(self):
        self.save()
        

# Criar o perfil quado o usuario for criado
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)
post_save.connect(create_profile, sender=User)