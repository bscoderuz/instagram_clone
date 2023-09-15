import re
import threading

import phonenumbers
from decouple import config
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from phonenumbers import NumberParseException
from twilio.rest import Client

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def check_email_or_phone(email_or_phone):
    try:
        phone_number = phonenumbers.parse(email_or_phone)
    except NumberParseException:
        phone_number = None

    if re.fullmatch(email_regex, email_or_phone):
        return "email"
    elif phone_number and phonenumbers.is_valid_number(phone_number):
        return "phone"
    else:
        raise ValueError("Email yoki telefon raqamingiz notog'ri")


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype = 'html'
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'authentication/activate_account.html',
        {'code': code}
    )
    Email.send_email(
        {
            'subject': "Ro'yxatdan o'tish",
            'to_email': email,
            'body': html_content,
            'content_type': '"html'
        }
    )


def send_phone_code(phone, code):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Salom! Sizning tasdiqlash kodingiz: {code}\n",
        from_="+99895005050",
        to=f"{phone}"
    )
