# Generated by Django 4.1.1 on 2024-04-06 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_chat_participants'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_name', models.CharField(max_length=128, verbose_name='Имя чата')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat_with_name', to='api.chat', verbose_name='Чат')),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='name_chat_participant', to='api.participant', verbose_name='Участник')),
            ],
            options={
                'verbose_name': 'Имя чата',
                'verbose_name_plural': 'Имена чатов',
                'db_table': 'name_chat',
            },
        ),
    ]