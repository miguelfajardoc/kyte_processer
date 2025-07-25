import base64
import re
import quopri
import csv
import io

def extract_url(msg):
    data_b64 = msg['payload']['parts'][0]['body']['data']
    decoded_bytes = base64.urlsafe_b64decode(data_b64 + '==')
    decoded_text = quopri.decodestring(decoded_bytes).decode('utf-8')
    return re.search("(?P<url>https?://[^ ]+)", decoded_text).group("url")[:-3]   ##probar que funcione siempre ? 

def extract_data(response):
    csv_reader = csv.reader(io.StringIO(response.content.decode("utf-8")))
    return list(csv_reader)