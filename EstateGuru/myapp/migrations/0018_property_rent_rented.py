# Generated by Django 5.1.5 on 2025-01-29 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_remove_property_pro_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='property_rent',
            name='rented',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
