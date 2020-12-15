import argparse
import json
import sys
import json
import os

from .sorteo import Sorteo, SorteoInvalido
from .participante import Participante
from . import sorteo
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

        s = amigo_invisible.sorteo(
            maestro=args.maestro,
            participantes=participantes,
        )
        s.validate()

        notifier = notification.gmail_notifier(user, token)
        for participante, elegido in s.parejas:
            p = next(x for x in s.participantes if x.nombre == participante)
            notifier.send_email('rleblic@gmail.com')

        print(json.dumps(s.to_json()))
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
