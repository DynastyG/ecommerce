# Generated by Django 3.2.6 on 2021-09-17 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashionz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(default='cheppys/default.jpg', upload_to='cheppys/'),
        ),
    ]
