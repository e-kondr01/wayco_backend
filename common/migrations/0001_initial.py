# Generated by Django 3.1.2 on 2020-10-27 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('latitude', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('longitude', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('address', models.CharField(max_length=128)),
                ('rating', models.PositiveSmallIntegerField(null=True)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(max_length=16, verbose_name='Номер заказа')),
                ('total_sum', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('done_at', models.DateTimeField(null=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=32)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='accounts.consumer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('image_src', models.URLField(null=True)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='common.cafe')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=128)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='options', to='common.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductOptionChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_name', models.CharField(max_length=128)),
                ('choice_price', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('product_option', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='choices', to='common.productoption')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('chosen_options', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordered_products', to='common.productoptionchoice')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordered_products', to='common.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordered_products', to='common.product')),
            ],
        ),
        migrations.CreateModel(
            name='CafePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_src', models.URLField()),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='common.cafe')),
            ],
        ),
    ]
