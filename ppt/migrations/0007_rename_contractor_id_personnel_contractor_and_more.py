# Generated by Django 4.0.3 on 2022-04-26 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt', '0006_accessgroups_accesslevel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personnel',
            old_name='contractor_id',
            new_name='contractor',
        ),
        migrations.RenameField(
            model_name='personnel',
            old_name='services_id',
            new_name='services',
        ),
        migrations.AddField(
            model_name='tenant',
            name='base',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='tenant',
            name='lease',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Lease Agreement'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='percentage1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2, verbose_name='Percentage1'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='percentage2',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2, verbose_name='Percentage2'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='percentage3',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2, verbose_name='Percentage3'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='salesLimit1',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, verbose_name='First Sales Threshold'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='salesLimit2',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, verbose_name='Second Sales Threshold'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='salesLimit3',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, verbose_name='Third Sales Threshold'),
        ),
    ]
