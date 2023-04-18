from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os
import json
import subprocess

app = Flask(__name__)

# create the folders when setting up your app

    
    
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html',result={})


@app.route('/siege-results/<ip>', methods=['GET'])
def seigeResult(ip):
    # shekhar Code
    #siege_cmd = f"siege -c 10 -t 3s http://{ip}:32000/test"
    #ip = "127.0.0.1"  # example IP address
    siege_cmd = "siege -c 10 -t 10s http://{0}:32000/test".format(ip)


# Run the Siege command and capture its output
    result = subprocess.run(siege_cmd.split(), stdout=subprocess.PIPE)

    with open("/users/cspandey/siege.log", "r") as f:
        lines = f.readlines()
        last_line = lines[-1]
        values = last_line.split(",")[1:]
        values = [float(val) for val in values]

    keys = [
        "Transactions", "Elapsed time", "Data transferred", "Response time", "Transaction rate","Throughput",
    "Concurrency", "Successful transactions", "Failed transactions"
        ]
    my_dict = {key: value for key, value in zip(keys, values)}
    return render_template('index.html', result=my_dict, IP=ip)

    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=32020, debug=True)