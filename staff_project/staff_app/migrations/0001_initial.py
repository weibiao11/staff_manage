# Generated by Django 3.2 on 2022-11-09 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='部门标题')),
            ],
        ),
        migrations.CreateModel(
            name='StaffInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='姓名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('salary', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='工资')),
                ('entry_time', models.DateTimeField(verbose_name='入职时间')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('staff_department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='staff_app.department')),
            ],
        ),
    ]