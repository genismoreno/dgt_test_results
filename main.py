import logging
import os
import subprocess
import sys
from datetime import datetime

import click

from dgt_parser import DGTParser

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)
logging.getLogger().addHandler(logging.StreamHandler())

fileHandler = logging.FileHandler("/home/genis/projects/dgt_test_results/output.txt")
logging.getLogger().addHandler(fileHandler)


def send_message(message):
    subprocess.Popen(['notify-send', '-t', '10000', message])
    return


@click.command()
@click.option('--cron/--no-cron', default=False)
def main(cron):
    parser = DGTParser()
    try:
        logging.info(f'Starting at {datetime.now()}...')
        results = parser.get_results()
        if results:
            logging.info('Results found.\n')
            if not cron:
                for item in results:
                    logging.info(f'{item} : {results[item]}')
            else:
                # Send notification
                send_message('DGT Results found! Check the logs')
            sys.exit(0)
        else:
            logging.info('Results not found')
            sys.exit(0)
    except Exception as e:
        logging.error(f'Error found: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
