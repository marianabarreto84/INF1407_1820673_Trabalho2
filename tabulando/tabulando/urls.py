"""tabulando URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('admin/', admin.site.urls),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario_criado/', views.usuario_criado, name='usuario_criado'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('adicionar_registro/', views.adicionar_registro, name='adicionar_registro'),
    path('registro_adicionado/', views.registro_adicionado, name='registro_adicionado'),
    path('cadastrar_jogo/', views.cadastrar_jogo, name='cadastrar_jogo'),
    path('jogo_cadastrado/', views.jogo_cadastrado, name='jogo_cadastrado'),
    path('deletar_registro/<int:registro_codigo>/', views.deletar_registro, name='deletar_registro'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
