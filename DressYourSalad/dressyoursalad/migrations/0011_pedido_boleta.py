# Generated by Django 4.0.4 on 2022-05-16 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressyoursalad', '0010_pedido_entregado'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='boleta',
            field=models.IntegerField(default=0, verbose_name='Número de boleta'),
        ),
    ]
