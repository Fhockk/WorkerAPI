# from flask_script import Manager

from app import app

# manager = Manager(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
