# Generated by Django 3.1.1 on 2020-10-15 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_productreview_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ('-timestamp',)},
        ),
    ]
