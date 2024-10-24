import imaplib
import email
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

def fetch_emails():
    # Используйте пароль приложения вместо обычного пароля
    EMAIL = os.getenv('EMAIL_HOST_USER')
    PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    # Подключение к серверу Gmail IMAP
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')

    # Поиск всех писем
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()

    email_data = []
    for e_id in email_ids[-5:]:  # Получение последних 5 писем
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg['subject']
                from_ = msg['from']

                # Обработка тела письма (если письмо многочастное)
                if msg.is_multipart():
                    for part in msg.get_payload():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                email_data.append({'from': from_, 'subject': subject, 'body': body})

    mail.logout()
    return email_data
