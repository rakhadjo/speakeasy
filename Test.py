from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask("App Test")
bootstrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug = True)


