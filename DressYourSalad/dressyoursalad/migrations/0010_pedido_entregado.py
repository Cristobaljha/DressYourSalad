# Generated by Django 4.0.4 on 2022-05-12 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressyoursalad', '0009_pedido_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='entregado',
            field=models.BooleanField(default=False),
        ),
    ]