# Generated by Django 4.1.1 on 2022-11-04 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_dog_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dog',
            old_name='hasAvatar',
            new_name='has_avatar',
        ),
    ]