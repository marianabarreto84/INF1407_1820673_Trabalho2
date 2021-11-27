# Modulo com funções auxiliares para views
from projeto.models import Jogo


def seleciona_jogo(nome):
    jogo = Jogo.objects.filter(nome=nome).all()[0]
    return jogo.codigo


def retorna_status(status):
    if status == 1:
        return "Tenho"
    if status == 2:
        return "Desejado"
    if status == 3:
        return "Vendido"
    if status == 4:
        return "Doado"
    return "Emprestado"
