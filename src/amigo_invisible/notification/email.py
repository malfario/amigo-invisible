import ssl
import aiosmtplib
from pathlib import Path
from datetime import datetime
from email.message import Message
from email.mime.text import MIMEText
from typing import Any, Dict, AsyncGenerator
from email.mime.multipart import MIMEMultipart
import jinja2

from amigo_invisible import Participante, Sorteo
from . import Notifier


class EmailNotifier(Notifier):
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._server = aiosmtplib.SMTP(
            self._host,
            self._port,
            use_tls=True,
            tls_context=ssl.create_default_context(),
        )

    async def __aenter__(self):
        await self._server.connect()
        await self._server.login(self._user, self._password)
        return self

    async def __aexit__(self, exc_type, exc_value, tb):
        self._server.close()

    async def send_notification(self, recipient: str, message: Any):
        await self._server.send_message(
            message=message,
            sender=self._user,
            recipients=recipient,
        )


def gmail_notifier(user: str, token: str) -> EmailNotifier:
    return EmailNotifier(host='smtp.gmail.com', port=465, user=user, password=token)


def email_message(
    sorteo: Sorteo, mensaje: Dict[str, str], titulo, amijo, elegido: str
) -> Message:
    message = MIMEMultipart('alternative')
    message['Subject'] = titulo

    env = jinja2.Environment(
        loader=jinja2.PackageLoader(
            package_name='amigo_invisible',
            package_path=str(Path('resources', 'templates')),
            encoding='utf-8',
        )
    )

    for name, subtype in [('message.txt', 'plain'), ('message.html', 'html')]:
        template = env.get_template(name)
        mimepart = MIMEText(
            template.render(
                fecha=sorteo.fecha.strftime(r'%d/%m/%Y a las %H:%M'),
                amijo=amijo.capitalize(),
                elegido=elegido.capitalize(),
                maestro=sorteo.maestro.capitalize(),
                mensaje=mensaje.get(subtype),
            ),
            subtype,
            'utf-8',
        )
        message.attach(mimepart)

    return message
