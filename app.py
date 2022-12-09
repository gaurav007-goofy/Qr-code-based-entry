from flask import render_template, Flask

from apis.student_api import studentAPI

app = Flask(__name__)
app.register_blueprint(studentAPI)


@app.route('/')
def run():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run()
