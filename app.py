from flask import Flask, render_template
from domain.system import System

app = Flask(__name__)

ourSystem = System('version1')

@app.route('/')
def index():
    return render_template('home.html', sysObj = ourSystem)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)