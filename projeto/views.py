from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django.db.models import F
from projeto.forms import CadastraUsuario, CadastraJogo, AdicionaRegistro, AlteraRegistro, AlteraJogo

from projeto.models import Catalogo, Jogo

from .auxiliar import seleciona_jogo, retorna_status

from .graficos import grafico_registros_por_dia, grafico_editoras_mais_registradas, grafico_status_mais_registrados


def pagina_inicial(request):
    return render(request, "pagina_inicial.html")


def faq(request):
    return render(request, "faq.html")


def contato(request):
    return render(request, "contato.html")


def cadastro_usuario(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('pagina_inicial'))

    if request.method == 'POST':
        form = CadastraUsuario(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                is_active=True,
                is_staff=False,
                is_superuser=False,

                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.save()

            return HttpResponseRedirect(reverse('usuario_criado'))
    else:
        form = CadastraUsuario()

    contexto = {
        'form': form
    }
    return render(request, "cadastro_usuario.html", contexto)


@login_required
def perfil_usuario(request):
    return render(request, "perfil_usuario.html")


def usuario_criado(request):
    return render(request, "usuario_criado.html")


@login_required
def catalogo(request):
    usuario = request.user
    catalogo = Catalogo.objects.filter(usuario_id=usuario.id)
    catalogo = catalogo.annotate(nome_jogo=F('jogo__nome'))
    catalogo = catalogo.annotate(editora=F('jogo__editora'))
    catalogo = catalogo.annotate(codigo_jogo=F('jogo__codigo'))
    catalogo = catalogo.values('codigo', 'nome_jogo', 'editora', 'data_insercao', 'status', 'codigo_jogo')
    catalogo = catalogo.order_by('-data_insercao')

    for registro in catalogo:
        registro["status_str"] = retorna_status(registro['status'])

    if len(catalogo) > 0:
        form = AlteraRegistro(initial={'status': registro['status']})
    else:
        form = AlteraRegistro()
    context = {
        'catalogo': catalogo,
        'form': form,
    }
    return render(request, "catalogo.html", context)


@login_required
def adicionar_registro(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('pagina_inicial'))

    if request.method == 'POST':
        form = AdicionaRegistro(request.POST, usuario=request.user)

        if form.is_valid():
            nome_jogo = form.cleaned_data["nome"]
            id_jogo = seleciona_jogo(nome_jogo)
            registro = Catalogo.objects.create(
                usuario_id=request.user.id,
                jogo_id=id_jogo,
                status=form.cleaned_data["status"],
            )
            registro.save()
            return HttpResponseRedirect(reverse('registro_adicionado'))
    else:
        form = AdicionaRegistro()

    contexto = {
        'form': form,
    }
    return render(request, "adicionar_registro.html", contexto)


@login_required
def registro_adicionado(request):
    return render(request, "registro_adicionado.html")


@login_required
def cadastrar_jogo(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('pagina_inicial'))

    if request.method == 'POST':
        form = CadastraJogo(request.POST)
        if form.is_valid():
            jogo = Jogo.objects.create(
                nome=form.cleaned_data["nome"],
                editora=form.cleaned_data["editora"],
                min_jogadores=form.cleaned_data["min_jogadores"],
                max_jogadores=form.cleaned_data["max_jogadores"],
                idade_minima=form.cleaned_data["idade_minima"],
            )
            jogo.save()
            return HttpResponseRedirect(reverse('jogo_cadastrado'))
    else:
        form = CadastraJogo()
    print(form)
    contexto = {
        'form': form,
    }
    return render(request, "cadastrar_jogo.html", contexto)


@login_required
def jogo_cadastrado(request):
    return render(request, "jogo_cadastrado.html")


@login_required
def deletar_registro(request, registro_codigo):
    if request.method == "POST":
        registro = Catalogo.objects.get(codigo=registro_codigo)
        registro.delete()
    return HttpResponseRedirect(reverse('catalogo'))


@login_required
def alterar_registro(request, registro_codigo):
    registro = get_object_or_404(Catalogo, codigo=registro_codigo)
    if request.method == 'POST':
        form = AlteraRegistro(request.POST)
        if form.is_valid():
            registro.status = form.cleaned_data["status"]
            registro.save()
            return HttpResponseRedirect(reverse('catalogo'))
    else:
        form = AlteraRegistro(initial={'status': registro.status})
    contexto = {
        'codigo': registro_codigo,
        'form': form,
    }
    return render(request, "alterar_registro.html", contexto)


def verifica_nome_jogo(request):
    nome_jogo = request.GET.get("nome_jogo", None)
    resposta = {
        'existe': Jogo.objects.filter(nome__iexact=nome_jogo).exists(),
    }
    return JsonResponse(resposta)


@login_required
@permission_required('projeto.pode_ver_estatisticas')
def estatisticas(request):
    catalogo = Catalogo.objects.filter(usuario_id=request.user.id).all()
    dados_registros, labels_registros = grafico_registros_por_dia(request.user.id)
    dados_editoras, labels_editoras = grafico_editoras_mais_registradas(request.user.id)
    dados_status, labels_status = grafico_status_mais_registrados(request.user.id)
    contexto = {
        'catalogo': len(catalogo),
        'dados_registros': dados_registros,
        'labels_registros': labels_registros,
        'dados_editoras': dados_editoras,
        'labels_editoras': labels_editoras,
        'dados_status': dados_status,
        'labels_status': labels_status,
    }
    return render(request, "estatisticas.html", contexto)


@login_required
def pagina_jogo(request, codigo):
    jogo = get_object_or_404(Jogo, codigo=codigo)
    contexto = {
        'jogo': jogo,
    }
    return render(request, "pagina_jogo.html", contexto)


@login_required
def historico_jogos(request):
    jogos = Jogo.objects.order_by('nome').all()
    contexto = {
        'jogos': jogos,
    }
    return render(request, "historico_jogos.html", contexto)


@login_required
def alterar_jogo(request, jogo_codigo):
    jogo = get_object_or_404(Jogo, codigo=jogo_codigo)
    if request.method == 'POST':
        form = AlteraJogo(request.POST, usuario=request.user)
        if form.is_valid():
            jogo.nome = form.cleaned_data['nome']
            jogo.editora = form.cleaned_data['editora']
            jogo.min_jogadores = form.cleaned_data['min_jogadores']
            jogo.max_jogadores = form.cleaned_data['max_jogadores']
            jogo.idade_minima = form.cleaned_data['idade_minima']
            jogo.save()
            return HttpResponseRedirect(reverse('historico_jogos'))
    else:
        form = AlteraJogo(initial={'nome': jogo.nome, 'editora': jogo.editora, 'min_jogadores': jogo.min_jogadores, 'max_jogadores': jogo.max_jogadores, 'idade_minima': jogo.idade_minima})
    pode_deletar = True
    registros_associados = Catalogo.objects.filter(jogo__nome=jogo.nome).all()
    if len(registros_associados) > 0:
        pode_deletar = False
    contexto = {
        'codigo': jogo_codigo,
        'form': form,
        'pode_deletar': pode_deletar,
    }
    return render(request, "alterar_jogo.html", contexto)


@login_required
def deletar_jogo(request, jogo_codigo):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('catalogo'))
    jogo = get_object_or_404(Jogo, codigo=jogo_codigo)
    registros = Catalogo.objects.filter(jogo_id=jogo_codigo).all()
    if len(registros) == 0:
        jogo.delete()
    return HttpResponseRedirect(reverse('historico_jogos'))
