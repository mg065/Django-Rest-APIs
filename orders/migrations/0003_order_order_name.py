# Generated by Django 4.1.7 on 2023-02-18 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_id_alter_order_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
