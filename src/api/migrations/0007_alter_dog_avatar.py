# Generated by Django 4.1.1 on 2022-11-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_dog_data_update_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Аватар'),
        ),
    ]