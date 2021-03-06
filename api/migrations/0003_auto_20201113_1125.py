# Generated by Django 3.1.2 on 2020-11-13 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201113_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoption',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='api.product'),
        ),
        migrations.AlterField(
            model_name='productoptionchoice',
            name='product_option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='api.productoption'),
        ),
    ]
