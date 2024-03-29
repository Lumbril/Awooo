# Generated by Django 4.1.1 on 2024-02-04 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_chat_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(blank=True, db_table='chat_participant', null=True, related_name='chat_participants', to='api.participant'),
        ),
    ]
