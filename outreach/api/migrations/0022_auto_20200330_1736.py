# Generated by Django 2.1.15 on 2020-03-30 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20200330_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registered',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Resume'),
        ),
    ]
