from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import datetime


class Jogo(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    min_jogadores = models.IntegerField()
    max_jogadores = models.IntegerField()
    idade_minima = models.IntegerField(blank=True, null=True)
    editora = models.CharField(max_length=200)
    # editora = models.ForeignKey(Editora)

    def get_absolute_url(self):
        return reverse('pagina_jogo', args=[str(self.id_busca)])

    class Meta:
        db_table = 'jogo'


"""
class Editora(models.Model):
    codigo = models.BigIntegerField()
    nome = models.CharField(max_length=200)
"""


class Catalogo(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    jogo = models.ForeignKey(Jogo, blank=True, null=True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    data_insercao = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        permissions = [
            ('pode_ver_estatisticas', "Pode ver estatísticas"),
        ]
        db_table = 'catalogo'
