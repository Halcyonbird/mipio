# Generated by Django 3.0.7 on 2020-09-07 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20200905_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='usuario',
            field=models.IntegerField(unique=True),
        ),
    ]