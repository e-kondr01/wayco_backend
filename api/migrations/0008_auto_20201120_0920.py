# Generated by Django 3.1.2 on 2020-11-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201113_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('claimed', 'claimed'), ('ready', 'ready'), ('unclaimed', 'unclaimed')], max_length=16),
        ),
    ]
