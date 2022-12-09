import json

import pyrebase
pyrebase_config = json.load(open("serviceApiKey.json"))

firebase = pyrebase.initialize_app(pyrebase_config)

storage = firebase.storage()


if __name__ == '__main__':
    # file = open("images/195036.png")
    # storage.child("display-pictures/195036.png").put("images/195036.png")

    url = storage.child("display-pictures/195036.png").get_url(None)

    print(url)