# Generated by Django 4.1.1 on 2023-07-29 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_dog_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='dog',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления'),
        ),
        migrations.AddField(
            model_name='dog',
            name='date_edited',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Изменено'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_deleted',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_edited',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Изменено'),
        ),
        migrations.CreateModel(
            name='Walk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Время начала')),
                ('finish', models.DateTimeField(verbose_name='Время окончания')),
                ('time', models.IntegerField(verbose_name='Фактическое время прогулки')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('date_edited', models.DateTimeField(auto_now=True, null=True, verbose_name='Изменено')),
                ('date_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Дата удаления')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Прогулка',
                'verbose_name_plural': 'Прогулки',
                'db_table': 'walks',
            },
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('walk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.walk', verbose_name='Прогулка')),
            ],
            options={
                'verbose_name': 'GPS точка',
                'verbose_name_plural': 'GPS точки',
                'db_table': 'coordinates',
            },
        ),
    ]
