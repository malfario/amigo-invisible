import smtplib, ssl
import email.utils
from email.mime.text import MIMEText


class EmailNotifier:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password

    def send_email(self, recipient: str) -> None:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._host, self._port, context=context) as server:
            server.login(self._user, self._password)
            message = MIMEText('Hola desde la app el amijo invisible!')
            message['Subject'] = 'Sorteo del amigo invisible'
            message['To'] = email.utils.formataddr(('Amijo', recipient))
            message['From'] = email.utils.formataddr(
                ('no-reply', 'no-reply@amijo-invisible.com')
            )
            server.sendmail(self._user, recipient, message.as_string())


def gmail_notifier(user: str, token: str) -> EmailNotifier:
    return EmailNotifier(host='smtp.gmail.com', port=465, user=user, password=token)
