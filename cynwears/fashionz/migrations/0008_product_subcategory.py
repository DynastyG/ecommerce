# Generated by Django 3.2.6 on 2021-09-19 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fashionz', '0007_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fashionz.subcategory'),
        ),
    ]