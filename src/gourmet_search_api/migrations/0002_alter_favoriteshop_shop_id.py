# Generated by Django 3.2.25 on 2024-03-31 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gourmet_search_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteshop',
            name='shop_id',
            field=models.IntegerField(),
        ),
    ]