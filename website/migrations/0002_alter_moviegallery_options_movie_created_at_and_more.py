# Generated by Django 5.0.7 on 2024-07-18 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moviegallery',
            options={'verbose_name': 'фото', 'verbose_name_plural': 'фотки'},
        ),
        migrations.AddField(
            model_name='movie',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Был добавлен'),
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(null=True, related_name='genre', to='website.genre'),
        ),
    ]
