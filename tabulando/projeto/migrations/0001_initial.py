# Generated by Django 3.1.5 on 2021-11-26 22:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jogo',
            fields=[
                ('codigo', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('min_jogadores', models.IntegerField()),
                ('max_jogadores', models.IntegerField()),
                ('idade_minina', models.IntegerField(blank=True, null=True)),
                ('editora', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'jogo',
            },
        ),
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.BigIntegerField()),
                ('data_insercao', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('status', models.IntegerField(blank=True, null=True)),
                ('jogo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projeto.jogo')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'catalogo',
            },
        ),
    ]
