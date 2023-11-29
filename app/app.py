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
import psutil

app = Flask(__name__)

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)



model = load_model("model.keras")
target_size = model.input_shape[1:3]

def model_predict(img_path, model):
    im = Image.open(img_path).convert('RGB')
    image_resized = im.resize(target_size, Image.BICUBIC)
    test_sample = np.array(image_resized)/255.0
    test_sample = test_sample.reshape(1, target_size[0], target_size[1], 3)
    classes = np.array(["Bread", "Dairy product", "Dessert", "Egg", "Fried food",
	"Meat", "Noodles/Pasta", "Rice", "Seafood", "Soup",
	"Vegetable/Fruit"])
    test_probs = model.predict(test_sample)
    most_likely_classes = np.argmax(test_probs.squeeze())
    
    return classes[most_likely_classes], test_probs.squeeze()[most_likely_classes]



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    preds = None
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        print(f)
        f.save(os.path.join(app.instance_path, 'uploads', secure_filename(f.filename)))
        memory_usage_before = psutil.virtual_memory().used
        start_time = time.time()
        preds, probs = model_predict("./instance/uploads/" + f.filename, model)
        end_time = time.time()
        memory_usage_after = psutil.virtual_memory().used
        memory_usage_during = (memory_usage_after - memory_usage_before) / (1024 * 1024)
        elapsed_time =  end_time - start_time
        return str(preds) + " (" + str(round(probs, 2)) + "), Inference Time : {:.4f} seconds".format(elapsed_time) # + ", "  + "Memory usage : {:.4f}mb".format(memory_usage_during)
    return "<h1> Error - no prediction </h1>"

@app.route('/test', methods=['GET'])
def test():
    preds = model_predict("./instance/uploads/test_image.jpeg", model)
    return str(preds)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
