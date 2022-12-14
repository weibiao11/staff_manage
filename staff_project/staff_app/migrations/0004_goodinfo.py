# Generated by Django 3.2 on 2022-11-12 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_app', '0003_mobilenum'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8, verbose_name='商品名称')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='商品价格')),
                ('color', models.SmallIntegerField(choices=[(1, '红色'), (2, '绿色')], default=1, verbose_name='商品的颜色')),
            ],
        ),
    ]
