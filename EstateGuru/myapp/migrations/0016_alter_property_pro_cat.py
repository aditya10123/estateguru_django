# Generated by Django 5.1.5 on 2025-01-28 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_property_pro_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='pro_cat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='myapp.property_cat'),
        ),
    ]
