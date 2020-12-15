import argparse
import json
import sys
import json
import os

from .sorteo import Sorteo, SorteoInvalido
from .participante import Participante
from . import notification
import amigo_invisible


def main(args):
    try:
        user = os.getenv('GMAIL_USER')
        token = os.getenv('GMAIL_TOKEN')
        if user is None or token is None:
            raise Exception('Missing Gmail account info')

        with open(args.participantes) as f:
            doc = json.load(f)
            participantes = [Participante.from_json(x) for x in doc['participantes']]

        # Crea un generador de sorteos
        sorteo_generator = amigo_invisible.sorteo(
            maestro=args.maestro,
            participantes=participantes,
        )

        # Encuentra un sorteo válido
        while (sorteo := next(sorteo_generator)) is None:
            continue

        # Valida el sorteo
        sorteo.validate()

        # Envía notificación a los participantes
        notifier = notification.gmail_notifier(user, token)
        for participante, elegido in sorteo.parejas:
            p = next(x for x in sorteo.participantes if x.nombre == participante)
            # notifier.send_email('xxx@gmail.com')

        print(json.dumps(sorteo.to_json()))
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--maestro', help='El maestro de ceremonias.')
    parser.add_argument(
        '--participantes', help='JSON conteniendo la lista de participantes.'
    )
    main(args=parser.parse_args())
