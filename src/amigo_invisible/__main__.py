import asyncio
import argparse
import json
import sys
import json
import os

from .sorteo import Sorteo, SorteoInvalido
from .participante import Participante
from .notification import email as notification
import amigo_invisible


async def main(args):
    user = os.getenv('GMAIL_USER')
    token = os.getenv('GMAIL_TOKEN')
    if not all({user, token}):
        raise Exception('Missing Gmail account info')

    with open(args.config) as f:
        doc = json.load(f)

    titulo = doc.get('titulo')
    maestro = doc.get('maestro')
    mensaje = doc.get('mensaje', {'plain': '', 'html': ''})
    participantes = [Participante.from_json(x) for x in doc.get('participantes', [])]
    if not all({titulo, maestro, len(participantes)}):
        raise Exception('Missing draft config data')

    # Crea un generador de sorteos
    sorteo_generator = amigo_invisible.sorteo(
        maestro=maestro,
        participantes=participantes,
    )

    # Encuentra un sorteo válido
    while (sorteo := next(sorteo_generator)) is None:
        continue

    # Valida el sorteo
    sorteo.validate()

    # Envía notificación a los participantes
    notification_tasks = []
    async with notification.gmail_notifier(user, token) as notifier:
        for partname, selname in sorteo.parejas:
            amijo = next(x for x in participantes if x.nombre == partname)
            message = notification.email_message(
                sorteo=sorteo,
                titulo=titulo,
                mensaje=mensaje,
                amijo=amijo.nombre,
                elegido=selname,
            )
            task = asyncio.create_task(
                notifier.send_notification(recipient=amijo.email, message=message)
            )
            notification_tasks.append(task)
        await asyncio.gather(*notification_tasks)
    print(json.dumps(sorteo.to_json()))


parser = argparse.ArgumentParser()
parser.add_argument('config', help='Datos del sorteo codificados como JSON')
asyncio.run(main(args=parser.parse_args()))
