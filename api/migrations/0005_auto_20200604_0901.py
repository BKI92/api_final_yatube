# Generated by Django 3.0.6 on 2020-06-04 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200603_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
