from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _U
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from projeto.models import Jogo, Catalogo


class CadastraUsuario(forms.Form):
    first_name = forms.CharField(label='Nome', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Sobrenome', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Nome de Usuário", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}), validators=[RegexValidator(regex=r'^[A-Za-z\d_]+$', message="O nome de usuário deve conter apenas números, letras ou _.")])
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}), validators=[validate_password])
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            raise ValidationError(_U('Este email já está associado a um usuário.'))
        return email

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError(_U('Este nome de usuário já está em uso. Por favor, escolha outro.'))
        return username

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get('password1')
        senha2 = cleaned_data.get('password2')

        if senha1 is not None and senha1 != senha2:
            self.add_error('password2', 'As senhas não são iguais.')


class AdicionaRegistro(forms.Form):
    def __init__(self, *args, **kwargs):  # Importando o usuário para conseguir ver se um registro com o mesmo jogo já foi feito
        self.user = kwargs.pop('usuario', None)
        super(AdicionaRegistro, self).__init__(*args, **kwargs)

    nome = forms.CharField(label='Nome do Jogo', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    opcoes_status = (
        (1, "Tenho"),
        (2, "Desejado"),
        (3, "Vendido"),
        (4, "Doado"),
        (5, "Emprestado"),
    )
    status = forms.ChoiceField(label='Status', choices=opcoes_status, widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_nome(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        if Catalogo.objects.filter(jogo__nome=nome, usuario_id=self.user.id).count() > 0:
            raise ValidationError(_U('Este registro já foi feito. Caso queira alterar seu status, faça isso na página \"Catálogo\".'))
        if Jogo.objects.filter(nome=nome).count() == 0:
            raise ValidationError(_U('Este jogo ainda não foi cadastrado. Por favor, faça o cadastro antes de adicionar o registro.'))
        return nome


class AlteraRegistro(forms.Form):
    opcoes_status = (
        (1, "Tenho"),
        (2, "Desejado"),
        (3, "Vendido"),
        (4, "Doado"),
        (5, "Emprestado"),
    )
    status = forms.ChoiceField(label='Status', choices=opcoes_status, widget=forms.Select(attrs={'class': 'form-control'}))


class CadastraJogo(forms.Form):
    nome = forms.CharField(label='Nome do Jogo', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    editora = forms.CharField(label='Editora', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    idade_minima = forms.IntegerField(label='Idade mínima', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_jogadores = forms.IntegerField(label='Número mínimo de jogadores', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_jogadores = forms.IntegerField(label='Número máximo de jogadores', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_nome(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        if nome[0] != nome[0].upper():
            raise ValidationError(_U('O nome do jogo deve ser iniciado com letra maiúscula.'))
        if Jogo.objects.filter(nome=nome).count() > 0:
            raise ValidationError(_U('Este jogo já foi cadastrado. Por favor, faça o cadastro antes de adicionar o registro.'))
        return nome

    def clean_idade_minima(self):
        cleaned_data = super().clean()
        idade_minima = cleaned_data.get('idade_minima')
        if idade_minima <= 0 and idade_minima >= 130:
            raise ValidationError(_U('A idade mínima não é válida. A idade deve ser maior do que 0 e menor do que 130.'))
        return idade_minima

    def clean(self):
        cleaned_data = super().clean()
        min_jogadores = cleaned_data.get('min_jogadores')
        max_jogadores = cleaned_data.get('max_jogadores')
        if min_jogadores is not None and max_jogadores < min_jogadores:
            self.add_error('max_jogadores', 'O número de jogadores máximo não pode ser menor do que o número mínimo.')
