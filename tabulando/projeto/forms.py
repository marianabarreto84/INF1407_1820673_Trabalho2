from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _U
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User


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

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get('password1')
        senha2 = cleaned_data.get('password2')

        if senha1 is not None and senha1 != senha2:
            self.add_error('password2', 'As senhas não são iguais.')


class AdicionaRegistro(forms.Form):
    nome = forms.CharField(label='Nome do Jogo', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
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
