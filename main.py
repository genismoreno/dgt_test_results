with open('body.txt') as file:
    body = file.read()

with open('headers.txt') as file:
    headers = file.read()

import requests

url = "https://sedeapl.dgt.gob.es:7443/WEB_NOTP_CONSULTA/consultaNota.faces"

import email
import io
message = email.message_from_file(io.StringIO(headers))
p_headers = dict(message.items())

resp = requests.post(url, headers=p_headers, data=body)
content = resp.content
with open('response.txt', 'wb') as file:
    file.write(content)

from lxml import html
root = html.parse('response.txt').getroot()
msg_errors = root.find_class("msgError")
print(len(msg_errors))
for msg_error in msg_errors:
    print(html.tostring(msg_error))



