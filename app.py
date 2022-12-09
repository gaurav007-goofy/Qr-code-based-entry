from flask import render_template, Flask

from apis.student_api import studentAPI

app = Flask(__name__)
app.register_blueprint(studentAPI)


@app.route('/')
def run():
    return render_template('scan_qr.html')


@app.route('/login/<string:login_type>')
def login_routing(login_type):
    if login_type == "student":
        return render_template("student_login.html")
    elif login_type == "security":
        return render_template("security_login.html")
    else:
        return "error"


if __name__ == '__main__':
    app.run(debug=True)
