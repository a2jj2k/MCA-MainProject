# Generated by Django 2.1.5 on 2019-04-29 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_archive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archive',
            name='module',
        ),
    ]
