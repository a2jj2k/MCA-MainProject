# Generated by Django 2.1.5 on 2019-04-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qnppr', '0016_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='fig',
            field=models.ImageField(blank=True, null=True, upload_to='question_fig'),
        ),
    ]
