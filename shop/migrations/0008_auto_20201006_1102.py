# Generated by Django 3.1.1 on 2020-10-06 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_collection_shopcollection'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopcollection',
            options={'ordering': ('-timestamp',)},
        ),
        migrations.AddField(
            model_name='shopcollection',
            name='cover',
            field=models.ImageField(blank=True, upload_to='collections/'),
        ),
    ]
