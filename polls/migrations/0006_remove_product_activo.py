# Generated by Django 3.0.7 on 2020-08-19 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200819_0114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Activo',
        ),
    ]