from flask import Flask, render_template, url_for, request, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def format_time():
    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return s[:-10]


posts = [
    {
        'author': '14 day COVID19 forecast',
        'title': "",
        'content': "",
        'date_posted': "last updated " + format_time()
    },
]

@app.before_request
def before_request_func():
    from data import Forecast
    Forecast().start()

    print("before_request is running!")


@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response


@app.route("/", methods=['GET', 'POST'])
@app.route("/home")
def home():

    return render_template('home.html',)


@app.route("/forecast")
def forecast():
    from data import XY
    bar = XY().create_plot()

    return render_template('forecast.html', posts=posts,  plot=bar)


if __name__ == '__main__':
    app.run(debug=True)
