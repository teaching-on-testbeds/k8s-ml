## Exercise: Deploy image classification as a web service

We will start by deploying an image classification model as a web service. Users can upload an image to a basic web app (in Flask) in their browser, then the app will:

* resize the image to the correct input dimensions
* pass it as input to an image classification model that has been fine tuned for food classification
* and return the most likely class (and estimated confidence), as well as the wall time of the `model.predict` call.

### Containerize the basic web app

To make it easy to deploy our basic application, we will containerize it - package the source code together with an operating system, software dependencies, and anything else it needs to run. This will also make it much easier to deploy multiple copies of the application (to handle heavier load) in future exercises.

```
-   app
    -   instance
    -   static
    -   templates
    -   app.py
    -   Dockerfile
    -   requirements.txt
    -   model.keras
```

Note that it includes a [Dockerfile](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/app/Dockerfile), which describes how to build a container for this application. We will build the container (naming it `ml-app`) and then push it to a local distribution "registry" of containers (which is already running on node-0, on port 5000).

In an SSH session on "node-0", run

```
docker build -t ml-app:0.0.1 ~/k8s-ml/app
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

### Deploy the basic web app

Now that we have containerized our application, we can run it! Let's run it now, and will indicate that we want incoming requests on port 32000 to be passed to port 5000 on the container (where our Flask application is listening). In an SSH session on "node-0", run

```
docker run -d -p 32000:5000 node-0:5000/ml-app:0.0.1
```

Here, 

-   `-d` is for detach mode - so we can leave it running int he background.
-   `-p` is to assign the mapping between "incoming request port" (32000) and "container port' (5000).


You can see the list of running containers with 

```
docker ps
```

which will show containers related to the docker register and Kubernetes deployment, but will also show one running container using the `node-0:5000/ml-app:0.0.1` image. To restrict the output to just this image, we can use

```
docker ps -f ancestor=node-0:5000/ml-app:0.0.1
```

Now we can visit our web service and try it out! Run this command on "node-0" to get the URL to use:

```
echo http://$(curl -s ipinfo.io/ip):32000
```

Then, open your browser, paste this URL into the address bar, and hit Enter.

When the web app has loaded, upload an image to your classification service, and check its prediction.

You can also see the resource usage - in terms of CPU and memory - of your container, with 

```
docker stats $(docker ps -q -f ancestor=node-0:5000/ml-app:0.0.1)
```

(which uses command substitution to get the ID of any running container using our `ml-app` image, then gets its statistics). Use Ctrl+C to stop this live display.


When you are finished, you can stop the container by running:


```
docker stop $(docker ps -q -f ancestor=node-0:5000/ml-app:0.0.1)
```

(which uses command substitution to get the ID of any running container using our `ml-app` image, then stops it).

### Transfer a saved model to the remote host

This is a "bring your own model" activity! You should have already trained a model, saved it as `model.keras`, and downloaded your saved model.

Use `scp` to transfer this file to `~/k8s-ml/app` on your "node-0" host.

Then, repeat the steps in the "Containerize the basic web app" and "Deploy the basic web app" sections, i.e. 

```
docker build -t ml-app:0.0.1 ~/k8s-ml/app
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

and then

```
docker run -d -p 32000:5000 node-0:5000/ml-app:0.0.1
```

> **Debugging your service**: if something goes wrong, you can use `docker run -p 32000:5000 node-0:5000/ml-app:0.0.1` to run your service *without* detaching from it, so that you can see output (including error messages).

(For a model that is very large, it may take a few minutes - even up to 10 minutes - before the container is ready to accept requests.)

Use your model to classify an image. Make sure your "deployed" model returns the same result for your custom test image as it did in the Colab notebook. Also note the inference time (the first inference may take much longer than subsequence predictions, so discard the first result.)

Also check the resource usage during inference with

```
docker stats $(docker ps -q -f ancestor=node-0:5000/ml-app:0.0.1)
```

When you are finished, stop the container by running:

```
docker stop $(docker ps -q -f ancestor=node-0:5000/ml-app:0.0.1)
```
