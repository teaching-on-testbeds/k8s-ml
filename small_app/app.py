import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask, redirect, url_for, request, render_template
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import time
import os
import json

app = Flask(__name__)

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)



model = MobileNet(weights='imagenet')


def model_predict(img_path,model):
    #mg_path = 'path/to/image.jpg'
    img = image.load_img(img_path, target_size=(331, 331))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

# Make predictions
    preds = model.predict(x)
    decoded_preds = decode_predictions(preds, top=5)[0]
    return decoded_preds[0][1]



result = {}
    
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', result=result)


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    start_time = time.time()
    preds = None
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        print(f)
        #f.save(secure_filename(f.filename))
        f.save(os.path.join(app.instance_path, 'uploads', secure_filename(f.filename)))
        # Make prediction
        preds = model_predict("./instance/uploads/" + f.filename, model)

        end_time = time.time()
        elapsed_time =  end_time - start_time

        return str(preds) + f", Inference Time : {elapsed_time}"
    return "<h1> Sorry Cant make any preds </h1>"

@app.route('/test', methods=['GET'])
def test():
    preds = model_predict("./instance/uploads/test_image.jpeg", model)
    return str(preds)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
