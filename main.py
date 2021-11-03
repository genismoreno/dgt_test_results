with open('body.txt') as file:
    body = file.read()

with open('headers.txt') as file:
    headers = file.read()

import email
import io
message = email.message_from_file(io.StringIO(headers))
p_headers = dict(message.items())

import requests

url = "https://sedeapl.dgt.gob.es:7443/WEB_NOTP_CONSULTA/consultaNota.faces"
resp = requests.post(url, headers=p_headers, data=body)
content = resp.content

from lxml import html
document = html.document_fromstring(content)
msg_errors = document.find_class("msgError")
for msg_error in msg_errors:
    print(html.tostring(msg_error))



