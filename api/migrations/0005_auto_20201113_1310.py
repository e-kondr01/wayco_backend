# Generated by Django 3.1.2 on 2020-11-13 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201113_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('completed', 'completed'), ('ready', 'ready'), ('unclaimed', 'unclaimed')], max_length=16),
        ),
    ]
