# Generated by Django 3.0.7 on 2020-09-03 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_carritodecompra_tienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccionusuario',
            name='telefono',
            field=models.CharField(max_length=10),
        ),
    ]
