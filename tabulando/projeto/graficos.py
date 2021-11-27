from django.db.models import Count
from django.db.models.functions import TruncDate
from projeto.models import Catalogo


def grafico_registros_tempo():
    # dados_registros = []
    # labels_registros = []

    # dados_data = []
    # labels_data = []
    registros_feitos = Catalogo.objects.annotate(data_insercao_data=TruncDate('data_insercao')).values('data_insercao_data').order_by('data_insercao_data').annotate(num_registros=Count('data_insercao_data'))
    print(registros_feitos)

    return
