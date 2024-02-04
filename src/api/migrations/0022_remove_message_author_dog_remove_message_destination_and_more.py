# Generated by Django 4.1.1 on 2024-02-04 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_message_author_dog_message_destination_dog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='author_dog',
        ),
        migrations.RemoveField(
            model_name='message',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='message',
            name='destination_dog',
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participant_dog', to='api.dog', verbose_name='Собака пользователя')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='participant_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Участник чата',
                'verbose_name_plural': 'Участники чатов',
                'db_table': 'participant',
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('date_edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Изменено')),
                ('date_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')),
                ('participants', models.ManyToManyField(db_table='chat_participant', related_name='chat_participants', to='api.participant')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'db_table': 'chat',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chat', to='api.chat', verbose_name='Чат'),
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_author', to='api.participant', verbose_name='Автор сообщения'),
        ),
    ]
