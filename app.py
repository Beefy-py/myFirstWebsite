from flask import Flask, render_template

s_app = Flask(__name__)


@s_app.route('/')
def home():
    return render_template('home.html')


@s_app.route('/about')
def about():
    return render_template('about.html')


@s_app.route('/projects')
def projects():
    return render_template('projects.html')


if __name__ == "__main__":
    s_app.run(debug=True)