from flask import Flask
from flask import request

app = Flask('application')


@app.before_request
def log_request_info():
    header = request.headers
    print(header)


app.run()
