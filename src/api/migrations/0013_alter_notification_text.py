# Generated by Django 4.1.1 on 2022-11-10 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_notification_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст уведомления'),
        ),
    ]
