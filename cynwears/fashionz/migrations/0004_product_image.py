# Generated by Django 3.2.6 on 2021-09-18 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashionz', '0003_auto_20210918_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.FileField(default='products/default.jpg', upload_to='products/'),
        ),
    ]