# Generated by Django 3.1.1 on 2020-10-06 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200930_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
