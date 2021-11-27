from django.db.models import Count, F
from django.db.models.functions import TruncDate
from projeto.models import Catalogo
from .auxiliar import retorna_status


def grafico_registros_por_dia(id_usuario):
    dados_registros = []
    labels_registros = []

    catalogo = Catalogo.objects.filter(usuario_id=id_usuario).annotate(data_insercao_data=TruncDate('data_insercao')).values('data_insercao_data').order_by('data_insercao_data').annotate(num_registros=Count('data_insercao_data'))
    for registro in catalogo:
        dados_registros.append(registro["num_registros"])
        labels_registros.append(registro["data_insercao_data"].strftime("%d/%m/%Y"))

    return dados_registros, labels_registros


def grafico_editoras_mais_registradas(id_usuario):
    dados_editoras = []
    labels_editoras = []

    catalogo = Catalogo.objects.filter(usuario_id=id_usuario).annotate(editora=F('jogo__editora')).values('editora').annotate(num_registros=Count('editora')).order_by('-num_registros')
    for registro in catalogo:
        dados_editoras.append(registro["num_registros"])
        labels_editoras.append(registro["editora"])

    return dados_editoras, labels_editoras


def grafico_status_mais_registrados(id_usuario):
    dados_status = []
    labels_status = []

    catalogo = Catalogo.objects.filter(usuario_id=id_usuario).values('status').annotate(num_registros=Count('status')).order_by('status')
    for registro in catalogo:
        dados_status.append(registro['num_registros'])
        labels_status.append(retorna_status(registro["status"]))

    return dados_status, labels_status
