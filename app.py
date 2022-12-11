from flask import render_template, Flask, request, redirect, url_for

import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, request, render_template, Response
from configs import Keys
import cv2
from configs import Keys
from models.models import Student, EntryRequest, Security

app = Flask(__name__)

pyrebase_config = json.load(open("serviceApiKey.json"))
pyrebase_store = pyrebase.initialize_app(pyrebase_config)
storage = pyrebase_store.storage()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
studentDB = firestore.client().collection("student-service-db")
entryDB = firestore.client().collection("entry-service-db")
securityDB = firestore.client().collection("security-service-db")
student_data = {}
security_data = {}
qr_data = {}


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
            if data:
                print("Printed Data is: {}".format(str(data)))
                global qr_data
                qr_data = str(data)
                camera.release()
                cv2.destroyAllWindows()
                # render_without_request('index1.html', var1='foo', var2='bar')
                break
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def run():
    # my_dict = {
    #     Keys.security_id: "chahcu",
    #     Keys.building_id: "library",
    #     Keys.created_timestamp: "234-234-245"
    # }
    return render_template('homepage.html')


@app.route('/login/<string:login_type>')
def login_routing(login_type):
    if login_type == "student":
        return render_template("student_login.html")
    elif login_type == "security":
        return render_template("security_login.html")
    else:
        return "error"


@app.route('/student/auth', methods=["POST", "GET"])
def get_student():
    global student_data
    if request.method == "GET":
        if student_data == {}:
            return redirect("/login/student")
        else:
            return render_template("student_profile.html", student=student_data)
    req = request.form
    college_email_id = req[Keys.college_email_id]
    res = studentDB.where(f"{Keys.college_email_id}", "==", f"{college_email_id}").get()
    if len(res) != 1:
        return render_template("student_login_error.html")
    for data in res:
        student_data = data.to_dict()
    if student_data[Keys.password] != req[Keys.password]:
        student_data = {}
        return render_template("student_login_error.html")
    return render_template("student_profile.html", student=student_data)


@app.route('/security/auth', methods=["POST", "GET"])
def get_security():
    global security_data
    if request.method == "GET":
        if security_data == {}:
            return redirect("/login/security")
        else:
            return render_template("security_profile.html", security=security_data)
    req = request.form
    security_id = req[Keys.security_id]
    res = securityDB.where(f"{Keys.security_id}", "==", f"{security_id}").get()
    if len(res) != 1:
        return render_template("security_login_error.html")
    for data in res:
        security_data = data.to_dict()
    if security_data[Keys.password] != req[Keys.password]:
        security_data = {}
        return render_template("security_login_error.html")
    return render_template("security_profile.html", security=security_data)


@app.route('/student/redirect/profile')
def redirect_get_student():
    return redirect("/student/auth")


@app.route('/student/register')
def register_student():
    return render_template("student_signup.html")


@app.post('/student/signup')
def signup_student():
    req = request.form
    res = Student(firstName=req[Keys.first_name],
                  lastName=req[Keys.last_name],
                  collegeId=req[Keys.college_id],
                  collegeEmailId=req[Keys.college_id] + "@nith.ac.in",
                  dateOfBirth=req[Keys.date_of_birth],
                  phoneNumber=req[Keys.phone_number],
                  hostelName=req[Keys.hostelName],
                  password=req[Keys.password]).__dict__
    studentDB.add(res)
    return "User Added Successfully"


@app.get('/student/scan_entry')
def scan_qr():
    return render_template("scan_qr.html")


@app.route('/student/video')
def video():
    print("Its there in video function")
    camera = cv2.VideoCapture(0)
    pic = generate_frames(camera)
    return Response(pic, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.post('/security/redirect/profile')
def redirect_get_security():
    return redirect("/security/auth")


@app.post('/student/add_entry')
def add_entry():
    tok = qr_data.split('#')
    print(tok)
    security_id = tok[0]
    building_id = tok[1]
    entry_data = EntryRequest(
        studentId=student_data[Keys.student_id],
        securityId=security_id,
        buildingId=building_id
    )
    entry_data = entry_data.__dict__
    res = entryDB.add(entry_data)
    print(entry_data)
    return render_template("entry_done.html", entry=entry_data)


@app.route('/security/generate_qr')
def generate_qr():
    return render_template('generate_qr.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
