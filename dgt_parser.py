import email
import io
import logging

import requests
from lxml import html


class DGTParser:
    URL = "https://sedeapl.dgt.gob.es:7443/WEB_NOTP_CONSULTA/consultaNota.faces"
    BASE_PATH = '/home/genis/projects/dgt_test_results/'

    @staticmethod
    def _read_file(path):
        with open(path) as file:
            return file.read()

    @staticmethod
    def _parse_headers(headers):
        message = email.message_from_file(io.StringIO(headers))
        p_headers = dict(message.items())
        return p_headers

    @staticmethod
    def _find_errors(document):
        # If errors found, probably there are no results yet. Be patient
        msg_errors = document.find_class("msgError")
        if len(msg_errors):
            logging.error('Errors found in response')
            return msg_errors
        return None

    @staticmethod
    def _find_results(document):
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
        return rows if len(rows) else None

    def get_results(self):
        body = self._read_file(self.BASE_PATH + 'body.txt')
        headers = self._read_file(self.BASE_PATH + 'headers.txt')

        p_headers = self._parse_headers(headers)

        response = requests.post(self.URL, headers=p_headers, data=body)
        content = response.content

        document = html.document_fromstring(content)
        errors = self._find_errors(document)

        if errors:
            logging.error('Errors found:')
            logging.error(errors)
            return None

        results = self._find_results(document)
        return results
