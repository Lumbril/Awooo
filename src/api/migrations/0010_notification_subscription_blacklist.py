# Generated by Django 4.1.1 on 2022-11-10 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_data_update_avatar_dog_date_update_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'db_table': 'notifications',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription', to=settings.AUTH_USER_MODEL, verbose_name='Подписка на')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписчик',
                'verbose_name_plural': 'Подписчики',
                'db_table': 'subscriptions',
            },
        ),
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('blocked_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blocked_user', to=settings.AUTH_USER_MODEL, verbose_name='Заблокированный пользователь')),
            ],
            options={
                'verbose_name': 'Пользователь в ЧС',
                'verbose_name_plural': 'Черный список',
                'db_table': 'blacklist',
            },
        ),
    ]
