import email
import io
import sys

import requests
from lxml import html

URL = "https://sedeapl.dgt.gob.es:7443/WEB_NOTP_CONSULTA/consultaNota.faces"


def read_file(path):
    with open(path) as file:
        return file.read()


def parse_headers(headers):
    message = email.message_from_file(io.StringIO(headers))
    p_headers = dict(message.items())
    return p_headers


def find_errors(document):
    # If errors found, probably there are no results yet. Be patient
    msg_errors = document.find_class("msgError")
    if len(msg_errors):
        print('Results not found. Check the following error messages:')
        for msg_error in msg_errors:
            print(f'\t{html.tostring(msg_error)}')
            sys.exit()


def find_results(document):
    result = document.find_class('letraBlancaBold')
    rows = {}
    if len(result):
        table = document.find_class('cuadroBlanco')
        if len(table):
            children = table[0].getchildren()
            for child in children:
                labels = child.find_class('textobold')
                key = labels[0].text_content() if len(labels) else None

                values = child.find_class('formCuadroIzq_big')
                value = values[0].text_content() if len(values) else None
                if key:
                    rows[key] = value
    return rows


def print_results(results):
    if len(results):
        print('Results found.\n')
        for item in results:
            print(f'{item} : {results[item]}')
    else:
        print('Results content could not be found')


def main():
    body = read_file('body.txt')
    headers = read_file('headers.txt')

    p_headers = parse_headers(headers)

    response = requests.post(URL, headers=p_headers, data=body)
    content = response.content

    document = html.document_fromstring(content)
    find_errors(document)

    results = find_results(document)
    print_results(results)


if __name__ == '__main__':
    main()








