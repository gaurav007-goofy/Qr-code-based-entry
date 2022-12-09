from flask import render_template, Flask

app = Flask(__name__)

# app.static_folder = 'static'


@app.route('/')
def run():
    return render_template('homepage.html')


if __name__ == "__main__":
    app.run()
