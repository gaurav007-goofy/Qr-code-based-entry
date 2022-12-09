import json

import pyrebase
pyrebase_config = json.load(open("serviceApiKey.json"))

firebase = pyrebase.initialize_app(pyrebase_config)

storage = firebase.storage()


if __name__ == '__main__':
    file = open("images/195055.jpg")
    storage.child("display-pictures/195055.jpg").put("images/195055.jpg")

    url = storage.child("display-pictures/195055.jpg").get_url(None)

    print(url)