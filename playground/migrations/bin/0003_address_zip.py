# Generated by Django 4.0.4 on 2022-06-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
