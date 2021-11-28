# Generated by Django 3.1.5 on 2021-11-28 21:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projeto', '0004_auto_20211128_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jogo',
            name='nome',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='catalogo',
            unique_together={('jogo', 'usuario')},
        ),
    ]
