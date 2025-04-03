# Generated by Django 5.1.1 on 2024-11-07 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_property_rent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property_rent',
            name='status',
            field=models.CharField(choices=[('available', 'for available'), ('unavailable', 'for unavailable')], max_length=100),
        ),
    ]
