import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from constants import TECH_SUPPORT_FIRST_ANSWER, VERIFICATION_CODE_EMAIL_HTML

private_vars = os.environ
SENDER_EMAIL: str = private_vars["SENDER_EMAIL"]
SMTP_SERVER: int = private_vars["SMTP_SERVER"]
SMTP_PORT: int = private_vars["SMTP_PORT"]
APP_PASSWORD: str = private_vars["APP_PASSWORD"]

class EmailSender:

    @staticmethod
    def send_techsup_fast_answer(to_email: str, name: str, theme: str, message_text: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = f"Ваше обращение в поддержку: {theme}"

            body = TECH_SUPPORT_FIRST_ANSWER.replace('{name}', name).replace('{theme}', theme).replace('{message_text}', message_text)
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)

            return True

        except Exception as _ex:
            print(f"[EmailSender->send_tech_support_email]. Error :: {_ex}")
            return False
        
    @staticmethod
    def send_vercode(code: str, to_email: str) -> bool:
        try:
            print('trying to send verification code')
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = to_email
            msg['Subject'] = f"Код верификации для подтверждения регистрации в DMZ Task Tracker"

            formatted_code = f"{code[:2]} {code[2:]}"
            html_body = VERIFICATION_CODE_EMAIL_HTML.replace(
                "{verification_code_formatted}", formatted_code
            )

            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, APP_PASSWORD)
                server.send_message(msg)

            return True

        except Exception as _ex:
            print(f"[EmailSender.py->send_verification_code_email]. Error :: {_ex}")
            return False
