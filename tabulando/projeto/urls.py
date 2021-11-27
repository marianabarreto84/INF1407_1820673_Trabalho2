from django.urls import path
from . import views

urlpatterns = [

    # Paginas Iniciais (home, faq, contato, admin)
    path('', views.pagina_inicial, name='pagina_inicial'),

    # Paginas de Usuário (login, perfil, cadastro, etc...)
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario_criado/', views.usuario_criado, name='usuario_criado'),

    # Páginas do Catalogo
    path('catalogo/', views.catalogo, name='catalogo'),
    path('adicionar_registro/', views.adicionar_registro, name='adicionar_registro'),
    path('registro_adicionado/', views.registro_adicionado, name='registro_adicionado'),
    path('cadastrar_jogo/', views.cadastrar_jogo, name='cadastrar_jogo'),
    path('jogo_cadastrado/', views.jogo_cadastrado, name='jogo_cadastrado'),
    path('jogo/<int:codigo>/', views.pagina_jogo, name='pagina_jogo'),
    path('deletar_registro/<int:registro_codigo>/', views.deletar_registro, name='deletar_registro'),
    path('alterar_registro/<int:registro_codigo>/', views.alterar_registro, name='alterar_registro'),

    # Página de Estatísticas
    path('estatisticas/', views.estatisticas, name='estatisticas'),

    # AJAX
    path('verifica_nome_jogo', views.verifica_nome_jogo, name='verifica_nome_jogo'),
]
