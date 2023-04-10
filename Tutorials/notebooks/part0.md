::: {.cell .markdown}

## Exercise: Deploy an image classification app on cloud.

For this exercise we will use a flask app to deploy the food classification model you build in lab 8.

To download the content of the app clone this repository "https://github.com/teaching-on-testbeds/k8s-ml" or run the following command in your terminal.

``` shell
git clone https://github.com/teaching-on-testbeds/k8s-ml.git
```

The content of the repository contains everything but the model which you want to deploy so now we will transfer the model from your local host to remote host.

Next copy the path of the model which you saved after completeing lab 7 and enter the below mentioned command in your local terminal

``` shell
scp "path of saved model" "name of remote host":"/k8s-ml/"
```

Now we have our model which we are going to deploy.

Before going ahead make sure that the folder structure is same as in the picture below

![Folder structure for the flask-app](images/folder.png)

Now we are ready to run the flask app, before that you should check what is the public ip from which the content of the app can be accessed.

``` shell
$ ifconfig -a
```

From the output of this command get the public ip of your remote host.

Now, we will create a virtual environment to run the flask app.

``` shell
$ sudo apt install virtualenv
$ virtualenv myenv
$ source myenv/bin/activate
```

Next step is to install all the requirements to run the app. on your terminal run :

``` shell
$ pip install -r requirements.txt
```

Next and the final step is to run the below mentioned command on your terminal:

``` shell
$ python app.py
```

Here you go the your flask app with a deep learning model is up and running, the output of the above command will be like this

``` shell
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 120-189-601
```

Now the app is up and running on ip:5000 open the url on your browser and try predicting with different food items.

This exercise is complete.

:::