# Generated by Django 4.1.1 on 2024-01-04 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_walk_distance_alter_walk_finish_alter_walk_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('state', models.CharField(choices=[('SENT', 'SENT'), ('READ', 'READ')], max_length=32, verbose_name='Статус')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор сообщения')),
                ('destination', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_destination', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
        ),
    ]