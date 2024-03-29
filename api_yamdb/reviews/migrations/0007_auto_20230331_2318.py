# Generated by Django 3.2 on 2023-03-31 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20230331_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('-year',)},
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.genre')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.title')),
            ],
        ),
    ]
