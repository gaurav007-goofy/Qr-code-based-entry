# import json
# import pyrebase
# import firebase_admin
# from firebase_admin import credentials, firestore
# from flask import Blueprint, request, render_template
# from configs import Keys
# from models.models import Student
#
# pyrebase_config = json.load(open("../serviceApiKey.json"))
# pyrebase_store = pyrebase.initialize_app(pyrebase_config)
# storage = pyrebase_store.storage()
#
# cred = credentials.Certificate("../serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# studentDB = firestore.client().collection("student-service-db")
#
# entryAPI = Blueprint('entry', __name__, url_prefix='/entry')
#
