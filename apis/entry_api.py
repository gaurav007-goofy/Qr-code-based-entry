# import json
# import pyrebase
# import firebase_admin
# from firebase_admin import credentials, firestore
# from flask import Blueprint, request, render_template
# from configs import Keys
# from models.models import Student, EntryRequest
#
# cred = credentials.Certificate("../serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# entryDB = firestore.client().collection("entry-service-db")
#
# entryAPI = Blueprint('entry', __name__, url_prefix='/entry')
#
#
# @entryAPI.get('/scan/<string:student_id>')
# def scan_qr():
#     return render_template("scan_qr.html")
#
#
# @entryAPI.get('/add/<string:student_id>')
# def add_entry(student_id):
#     security_id = "3hd8k3"
#     building_id = "reading_hall"
#     entry_data = EntryRequest(
#         studentId=student_id,
#         securityId=security_id,
#         buildingId=building_id
#     )
#     entry_data = entry_data.__dict__
#     res = entryDB.add(entry_data)
#     print(res)
#     for row in res:
#         print(res.to_dict())
#     return "done"
#
#
