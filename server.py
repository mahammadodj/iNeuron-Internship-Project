from server_app import pred
from threading import Thread
from flask import Flask

app = Flask(__name__)
thread = Thread(target = pred)

@app.route("/")

def run_server():
    if not run_server():
        thread.start()
    else:
        pass
    return 'Server is running...'

if __name__== '__main__':
    app.run(debug=True)