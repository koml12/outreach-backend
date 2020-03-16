# Generated by Django 2.1.15 on 2020-03-16 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_questionnaireans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='event',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='event',
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='event_q',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire_id', to='api.Event'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='event_s',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='survey_id', to='api.Event'),
        ),
        migrations.DeleteModel(
            name='Survey',
        ),
    ]
