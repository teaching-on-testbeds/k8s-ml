import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask import Flask, redirect, url_for, request, render_template
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import time
import os
import json

app = Flask(__name__)

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)



model = load_model("model.h5")
target_size = model.input_shape[1:3]

def model_predict(img_path, model):
    im = Image.open(img_path).convert('RGB')
    image_resized = im.resize(target_size, Image.BICUBIC)
    test_sample = np.array(image_resized)/255.0
    test_sample = test_sample.reshape(1, 224, 224, 3)
    classes = np.array(["Bread", "Dairy product", "Dessert", "Egg", "Fried food",
	"Meat", "Noodles/Pasta", "Rice", "Seafood", "Soup",
	"Vegetable/Fruit"])
    test_probs = model.predict(test_sample)
    most_likely_classes = np.argmax(test_probs.squeeze())
    
    return classes[most_likely_classes]



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


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
        return str(preds) + ", Inference Time : {:.4f} seconds".format(elapsed_time)
    return "<h1> Sorry Cant make any preds </h1>"

@app.route('/test', methods=['GET'])
def test():
    preds = model_predict("./instance/uploads/test_image.jpeg", model)
    return str(preds)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
