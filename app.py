from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html')

@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run()
