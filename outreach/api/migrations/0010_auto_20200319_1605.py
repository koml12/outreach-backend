# Generated by Django 2.1.15 on 2020-03-19 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200319_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='questionnaire_id',
            new_name='questionnaires',
        ),
    ]
