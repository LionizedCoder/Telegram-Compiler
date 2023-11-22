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
    "source": "",
    "base": "Rust",
    "useSpaces": False,
    "tabWidth": 4
}