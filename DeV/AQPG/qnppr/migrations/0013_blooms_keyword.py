# Generated by Django 2.1.5 on 2019-03-29 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qnppr', '0012_auto_20190329_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blooms_keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blm_verb', models.CharField(max_length=100)),
                ('blm_lvl_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qnppr.Blooms_lvl')),
            ],
        ),
    ]
