import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, request, render_template, jsonify
from configs import Keys
from models import Student

pyrebase_config = json.load(open("serviceApiKey.json"))
pyrebase_store = pyrebase.initialize_app(pyrebase_config)
storage = pyrebase_store.storage()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
userDB = firestore.client().collection("user-service-db")

userAPI = Blueprint('user', __name__)


@userAPI.post()
def create_user(req):
    req = request.form
    student_data = Student(firstName=req[Keys.first_name],
                           lastName=req[Keys.last_name],
                           collegeId=req[Keys.college_id],
                           collegeEmailId=req[Keys.college_email_id],
                           dateOfBirth=req[Keys.date_of_birth],
                           phoneNumber=req[Keys.phone_number],
                           imageUrl=req[Keys.image_url]).__dict__
    userDB.add(student_data)
    return "User Added Successfully"


@userAPI.get()
def get_user():
    req = request.form
    college_id = req[Keys.college_id]
    response = userDB.where(f"{Keys.college_id} == {college_id}").get()
    res = response.to_dict()
    if res.len() != 1 or res[Keys.password] != req[Keys.password]:
        return render_template("login_page.html", attempStatus=False)
    return render_template("student_dashboard.html", student=res)


#
# def input_data():
#     req = {
#         "firstName": "Gautam",
#         "lastName": "Verma",
#         "collegeId": "195036",
#         "collegeEmailId": "195036@nith.ac.in",
#         "dateOfBirth": "18-05-2001",
#         "phoneNumber": "8920460627",
#         "imageUrl": storage.child("display-pictures/195036.png").get_url(None)
#     }
#     create_user(req)
#
#
# if __name__ == '__main__':
#     input_data()
