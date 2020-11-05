# Generated by Django 3.1.2 on 2020-11-05 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_auto_20201104_2050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productoption',
            old_name='option_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='productoptionchoice',
            old_name='choice_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='productoptionchoice',
            old_name='choice_price',
            new_name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='has_options',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productoptionchoice',
            name='is_available',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]