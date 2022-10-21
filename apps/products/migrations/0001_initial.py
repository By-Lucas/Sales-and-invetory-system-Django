# Generated by Django 4.1.2 on 2022-10-21 03:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models.products


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(default=products.models.products.gerar_id, editable=False)),
                ('name', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('status', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to=products.models.products.upload_to)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'products',
                'ordering': ('-date_create',),
            },
        ),
    ]
