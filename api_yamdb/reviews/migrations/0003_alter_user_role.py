# Generated by Django 3.2 on 2023-03-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230330_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user')], default='user', max_length=20, verbose_name='Роль'),
        ),
    ]