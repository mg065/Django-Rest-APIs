# Generated by Django 4.1.7 on 2023-02-18 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]