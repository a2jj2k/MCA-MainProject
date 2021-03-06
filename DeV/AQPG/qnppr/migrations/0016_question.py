# Generated by Django 2.1.5 on 2019-04-03 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qnppr', '0015_auto_20190401_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField()),
                ('fig', models.ImageField(blank=True, upload_to='question_fig')),
                ('klevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qnppr.Blooms_lvl')),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qnppr.Mark')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qnppr.Module')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qnppr.Subject')),
            ],
        ),
    ]
