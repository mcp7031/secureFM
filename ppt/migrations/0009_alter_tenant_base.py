# Generated by Django 4.0.3 on 2022-04-26 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt', '0008_alter_tenant_percentage1_alter_tenant_percentage2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='base',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Base Sales'),
        ),
    ]
