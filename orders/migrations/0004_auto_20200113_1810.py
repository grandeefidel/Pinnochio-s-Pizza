# Generated by Django 3.0.1 on 2020-01-13 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='pizza_size',
            field=models.CharField(choices=[('small', 'small'), ('large', 'large')], max_length=5),
        ),
    ]
