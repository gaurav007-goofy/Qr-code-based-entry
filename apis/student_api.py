import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, request, render_template, Response
from configs import Keys
import cv2
from models.models import Student, EntryRequest

pyrebase_config = json.load(open("serviceApiKey.json"))
pyrebase_store = pyrebase.initialize_app(pyrebase_config)
storage = pyrebase_store.storage()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
studentDB = firestore.client().collection("student-service-db")
entryDB = firestore.client().collection("entry-service-db")

studentAPI = Blueprint('student', __name__, url_prefix='/student')

global_student_id = "null"


def generate_frames(camera):
    print("Its there in generate frames")
    qr_detector = cv2.QRCodeDetector()
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (0, 0), fx=0.6, fy=0.6)
            data, one, _ = qr_detector.detectAndDecode(frame)
            if (data):
                print("Printed Data is: {}".format(str(data)))
                camera.release()
                cv2.destroyAllWindows()
                # render_without_request('index1.html', var1='foo', var2='bar')
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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
    global_student_id = student_res[Keys.student_id]
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


@studentAPI.get('/scan_entry')
def scan_qr():
    return render_template("scan_qr.html")


@studentAPI.route('/video')
def video():
    print("Its there in video function")
    camera = cv2.VideoCapture(0)
    pic = generate_frames(camera)
    return Response(pic, mimetype='multipart/x-mixed-replace; boundary=frame')


@studentAPI.get('/add_entry')
def add_entry():
    security_id = "3hd8k3"
    building_id = "reading_hall"
    entry_data = EntryRequest(
        studentId=global_student_id,
        securityId=security_id,
        buildingId=building_id
    )
    entry_data = entry_data.__dict__
    res = entryDB.add(entry_data)
    print(res)
    for row in res:
        print(res.to_dict())
    return "done"
