from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User


def alerta_staff(recipientes, nome_template, assunto, context={}):
    recipientes = [staff.email for staff in User.objects.filter(is_staff=True).all() if staff.email is not None and staff.email != '']
    envia_email(recipientes, nome_template, assunto, context)


def envia_email(recipientes, nome_template, assunto, context={}):
    if type(recipientes) == str:
        recipientes = [recipientes]

    mensagem_html = render_to_string('email/' + nome_template + '.html', context)

    send_mail(
        subject='[Tabulando] ' + assunto,
        message=strip_tags(mensagem_html),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipientes,
        fail_silently=False,
        html_message=mensagem_html
    )
