# Generated by Django 3.0.7 on 2020-09-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20200903_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccionusuario',
            name='usuario',
            field=models.IntegerField(unique=True),
        ),
    ]
