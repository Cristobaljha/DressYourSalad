# Generated by Django 4.0.4 on 2022-05-06 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dressyoursalad', '0005_alter_pedido_cod_ped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cod_ped',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]