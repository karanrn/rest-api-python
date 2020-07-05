from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Welcome!"

@app.route('/user/<string:user_name>')
def show_user(user_name):
    return 'User {} is the best'.format(user_name)

if __name__ == "__main__":
    app.run()