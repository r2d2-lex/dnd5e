from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.signing import Signer
from ksardas.celery import celery_app
from ksardas.settings import ALLOWED_HOSTS

import os

signer = Signer()


@celery_app.task
def send_verification_email(email, user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    context = {'user': user, 'host': host, 'sign': signer.sign(user)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    send_mail(
        subject,
        body_text,
        os.environ.get('DJ_DEFAULT_FROM_EMAIL'),
        [email],
        fail_silently=False,
        )