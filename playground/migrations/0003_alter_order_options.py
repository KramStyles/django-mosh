# Generated by Django 4.0.4 on 2022-07-08 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can Cancel Orders')]},
        ),
    ]
