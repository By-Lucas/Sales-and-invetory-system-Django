# Generated by Django 4.1.2 on 2022-11-10 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='idade',
            field=models.BigIntegerField(blank=True, db_column='idade', default=0, null=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='numero_casa',
            field=models.BigIntegerField(blank=True, db_column='numero_casa', null=True),
        ),
    ]
