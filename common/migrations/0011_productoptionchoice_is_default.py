# Generated by Django 3.1.2 on 2020-11-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20201105_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoptionchoice',
            name='is_default',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
