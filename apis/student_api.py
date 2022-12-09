import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, request, render_template
from configs import Keys
from models.models import Student

pyrebase_config = json.load(open("serviceApiKey.json"))
pyrebase_store = pyrebase.initialize_app(pyrebase_config)
storage = pyrebase_store.storage()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
studentDB = firestore.client().collection("student-service-db")

studentAPI = Blueprint('student', __name__, url_prefix='/student')


@studentAPI.post('/')
def create_student(req):
    req = request.form
    student_data = Student(firstName=req[Keys.first_name],
                           lastName=req[Keys.last_name],
                           collegeId=req[Keys.college_id],
                           collegeEmailId=req[Keys.college_email_id],
                           dateOfBirth=req[Keys.date_of_birth],
                           phoneNumber=req[Keys.phone_number],
                           imageUrl=req[Keys.image_url]).__dict__
    studentDB.add(student_data)
    return "User Added Successfully"


@studentAPI.post('/signup')
def signup_student(signup_type):
    return render_template("")


@studentAPI.post('/auth')
def get_student():
    req = request.form
    college_email_id = req[Keys.college_id]
    print(college_email_id)
    res = studentDB.where(f"{Keys.college_email_id}", "==", f"{college_email_id}").get()
    student_res = {}
    if len(res) != 1:
        return render_template("student_login_error.html")
    for data in res:
        student_res = data.to_dict()
    if student_res[Keys.password] != req[Keys.password]:
        return render_template("student_login_error.html")
    return render_template("student_profile.html", student=student_res)

# def input_data():
#     req = {
#         "firstName": "Gaurav",
#         "lastName": "Saini",
#         "collegeId": "195055",
#         "collegeEmailId": "195055@nith.ac.in",
#         "dateOfBirth": "29-12-2000",
#         "phoneNumber": "9784257561",
#         "imageUrl": storage.child("display-pictures/195055.jpg").get_url(None)
#     }
#     create_student(req)
#
