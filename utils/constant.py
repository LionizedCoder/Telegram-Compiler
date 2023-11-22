import os

token = os.environ['TOKEN']
payload = {
        "source": "",
          "compiler": "r1730",
        "options": {
            "userArguments": "",
            "compilerOptions": {},
            "filters": {
                "intel": False,
            },
            "tools": [],
            "libraries": [
                {"id": "boost", "version": "181"},
                {"id": "fmt", "version": "trunk"},
                {"id": "rangesv3", "version": "trunk"}
            ]
        },
        "lang": "rust",
        "bypassCache": False,
        "allowStoreCodeDebug": True
    }

formatted_payload = {
    "source": '',
    "base": "Rust",
    "useSpaces": False,
    "tabWidth": 4
}

headers = {
    'Content-Type': 'application/json',
    'Connection' : 'keep-alive',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept' : '*/*',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
}