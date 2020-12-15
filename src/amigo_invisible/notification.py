import smtplib, ssl


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
            message = '''\
                Subject: Tu amijo invisible

                Hola desde la app el amijo invisible!
            '''
            server.sendmail('rleblic@gmail.com', recipient, message)


def gmail_notifier(user: str, token: str) -> EmailNotifier:
    return EmailNotifier(host='smtp.gmail.com', port=465, user=user, password=token)
