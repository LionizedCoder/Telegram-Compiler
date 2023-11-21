import requests
from io import BytesIO

def generate_image(code: str):
    r = requests.post('https://carbonara.solopov.dev/api/cook',
                      json={'code': code, 'theme': 'one-dark', 'language': 'text/x-c++src',
                            'paddingVertical': '10px', 'paddingHorizontal': '10px'})
    r.raise_for_status()
    return BytesIO(r.content)