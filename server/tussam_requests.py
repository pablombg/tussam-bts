# tussam-bts
# License: CC0 1.0 Universal

import xml.etree.ElementTree as ET
import http.client
import json


url = "/InfoTusWS/services/InfoTus?WSD"
headers = {
    'content-type': 'text/xml;charset=UTF-8',
    'Authorization': 'Basic aW5mb3R1cy11c2VybW9iaWxlOjJpbmZvdHVzMHVzZXIxbW9iaWxlMg==',
    'deviceid': 'A38-f3e2a984ead95d5j'
}
body_template = '''
<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:d="http://www.w3.org/2001/XMLSchema"
            xmlns:c="http://schemas.xmlsoap.org/soap/encoding/"
            xmlns:v="http://schemas.xmlsoap.org/soap/envelope/">
    <v:Header/>
    <v:Body>
        <n0:getBuses id="o0"
                     c:root="1"
                     xmlns:n0="http://services.infotusws.tussam.com/">
            <labelLinea i:type="d:string">{}</labelLinea>
        </n0:getBuses>
    </v:Body>
</v:Envelope>
'''


def get_positions(route):
    body = body_template.format(route)
    conn = http.client.HTTPConnection("www.infobustussam.com", 9005)
    conn.request("POST", url, body=body, headers=headers)

    response = conn.getresponse()
    response_data = response.read().decode("utf-8")

    tree = ET.fromstring(response_data)
    positions = []

    for element in tree.iter("bus"):
        lat = element[1].text[:-6] + "." + element[1].text[-6:]
        lon = element[2].text[:-6] + "." + element[2].text[-6:]
        positions.append([float(lon), float(lat)])

    return json.dumps(positions)
