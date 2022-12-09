# import json
# import pyrebase
# import firebase_admin
# from firebase_admin import credentials, firestore
# from flask import Blueprint, request, render_template
# from configs import Keys
# from models.models import Student, Security
#
# pyrebase_config = json.load(open("../serviceApiKey.json"))
# pyrebase_store = pyrebase.initialize_app(pyrebase_config)
# storage = pyrebase_store.storage()
#
# cred = credentials.Certificate("../serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# securityDB = firestore.client().collection("security-service-db")
#
# studentAPI = Blueprint('security', __name__, url_prefix='/security')
#
#
# # @studentAPI.post('/')
# # def create_security(req):
# #     req = request.form
# #     student_data = Security(firstName=req[Keys.first_name],
# #                            lastName=req[Keys.last_name],
# #
# #                            dateOfBirth=req[Keys.date_of_birth],
# #                            phoneNumber=req[Keys.phone_number],
# #                            imageUrl=req[Keys.image_url]).__dict__
# #     studentDB.add(student_data)
# #     return "User Added Successfully"
# #
# #
# #
# # @studentAPI.post('/auth')
# # def get_student():
# #     req = request.form
# #     college_email_id = req[Keys.college_email_id]
# #     res = studentDB.where(f"{Keys.college_email_id} == {college_email_id}").get()
# #     res = res[0].to_dict()
# #     if res.len() != 1 or res[Keys.password] != req[Keys.password]:
# #         return render_template("error")
# #     return render_template("student_profile.html", student=res)
#
# # def input_data():
# #     req = {
# #         "firstName": "Gaurav",
# #         "lastName": "Saini",
# #         "collegeId": "195055",
# #         "collegeEmailId": "195055@nith.ac.in",
# #         "dateOfBirth": "29-12-2000",
# #         "phoneNumber": "9784257561",
# #         "imageUrl": storage.child("display-pictures/195055.jpg").get_url(None)
# #     }
# #     create_student(req)
# #
