"""Cloud Foundry test"""
from flask import Flask, render_template
import os

app = Flask(__name__)

print(os.getenv("PORT"))
port = int(os.getenv("PORT", 5000))

base_url = "http://s3.us-east.cloud-object-storage.appdomain.cloud/adb-sum/"

@app.route('/', methods=["GET"])
def get_index_page():
    return render_template('index.html', result={})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)