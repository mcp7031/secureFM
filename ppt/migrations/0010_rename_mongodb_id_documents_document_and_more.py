# Generated by Django 4.0.3 on 2022-04-28 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt', '0009_alter_tenant_base'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documents',
            old_name='mongoDB_id',
            new_name='document',
        ),
        migrations.RemoveField(
            model_name='nominal',
            name='incident',
        ),
        migrations.RemoveField(
            model_name='nominal',
            name='safety',
        ),
        migrations.AddField(
            model_name='location',
            name='length',
            field=models.IntegerField(blank=True, null=True, verbose_name='Length'),
        ),
        migrations.AddField(
            model_name='location',
            name='width',
            field=models.IntegerField(blank=True, null=True, verbose_name='Width'),
        ),
    ]
