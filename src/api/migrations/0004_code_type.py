# Generated by Django 4.1.1 on 2022-10-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_code_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='type',
            field=models.CharField(choices=[('REGISTRATION', 'Для регистрации'), ('CHANGE_PASSWORD', 'Для смены пароля')], max_length=32, null=True, verbose_name='Тип кода'),
        ),
    ]