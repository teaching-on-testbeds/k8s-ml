<<<<<<< HEAD
## Exercise: Deploy image classification as a web service

SSH into node-0 of your cluster and leave the terminal open.


### Transfer a saved model to the remote host

For this exercise we will use a flask app to deploy the food classification model you built in https://colab.research.google.com/drive/16w-mLZ4tSxwH7bZof-1Baota-TIYv19B.



The content of the repository contains everything but the model which you want to deploy. Go to the colab notebook, Train and test the model inside colab, save it by adding the below mentioned python code in the last cell of the notebook.

```python
model.save("model.h5")

```
then download the saved model from Colab (use the file brower on the side to locate and download the saved model).

Leave the SSH session running and open a new local terminal, change directory to the directory where your model is saved and run the below mentioned scp command to transfer the model to remote. Replace `USERNAME` and `HOSTNAME`...

``` shell
scp model.h5 USERNAME@HOSTNAME:~/k8s-ml/app/

=======
## Exercise: Deploy an image classification app as a web service

SSH into node-0 of your cluster. In this terminal, clone this repository, which contains all the material needed in the further exercises.

``` shell
git clone https://github.com/teaching-on-testbeds/k8s-ml.git
```

Now, you will need the model that you trained in the previous exercise. (As a demo, though, you can use the saved model that is already in this repository.)  Transfer the model that you trained in the previous exercise to node-0 - run

``` shell
echo scp model.h5 $USER@$(curl -s ipinfo.io/ip):~/k8s-ml/app
>>>>>>> 9e6db1c4fca74ce4defef213925b6f5b59b7efe7
```

to get an SCP command, then run the SCP command in your *local* terminal (not in the SSH session), from the directory where your model is saved. (If your SSH key is in a non-default location, you will need to add an argument to specify the key location.)

<<<<<<< HEAD
Once the file is transfered, open the ssh session at node-0

Now we are ready to run the flask app, We will be using Docker to containerise the ml-app. Learning Docker is a large process and that is not the part of this exercise. To make sure that you don't get stuck with docker, a Dockerfile is already provided in the app you downloaded.


The next step is to get into app directory which contains flask app
=======
The output should look like this:

``` shell
model.h5                                                                                                                  100%  155MB   8.9MB/s   00:17
```
indicating that your model is transfered from your local to remote.

Once the file is transfered, return to the SSH session at node-0.

Now we are ready to deploy our model as a service. Rather than deploying it directly, we will use Docker to package our model, source code, and dependencies in a *container*. This will make it much easier to deploy multiple copies of the application (to handle heavier load) in future exercises.

Next, navigate to the directory that contains our application, which is implemented using Flask:
>>>>>>> 9e6db1c4fca74ce4defef213925b6f5b59b7efe7

``` shell
cd ~/k8s-ml/app
```

<<<<<<< HEAD
This directory has the following structure:
=======
The directory structure is as shown below:
>>>>>>> 9e6db1c4fca74ce4defef213925b6f5b59b7efe7

-   app
    -   instance
    -   static
    -   templates
    -   app.py
    -   Dockerfile
    -   requirements.txt
    -   model.h5

<<<<<<< HEAD
Next step is to create a docker image of our Flask app and push it to the local registry running at 10.10.1.1:5000
=======
This directory includes a Dockerfile, which describes how to containerize the application. We will build the container (naming it `ml-app`) and then push it to a local "registry" of containers (which is running on port 5000 of node-0).

``` shell
docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

Now that we have containerized our application, we can run it! Let's run it now, and will indicate that we want incoming requests on port 32000 to be passed to port 5000 on the container (where our Flask application is listening):

``` shell
docker run -d -p 32000:5000 node-0:5000/ml-app:0.0.1
```

-   `-d` is for detach mode.
-   `-p` is to assign the port host_port:container_port.

Now we can visit our web service and try it out! Run this command:

``` shell
echo http://$(curl -s ipinfo.io/ip):32000
```

to get the URL on which it is running, then open your browser and paste this URL into the address bar.

You can upload images to your image classification service and check its predictions.

When you are finished, you can stop the container by running:


``` shell
docker stop $(docker ps -q -f ancestor=ml-app:0.0.1)

```

---

In this exercise or in a future exercise, you may want to change the model underlying your service. If you do, you will need to repeat the SCP command to transfer the saved model. Then, you will have to rebuild the container, following the same steps as you did above while building the container for the first time.
>>>>>>> 9e6db1c4fca74ce4defef213925b6f5b59b7efe7

``` shell
docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```
<<<<<<< HEAD

The command above will build a docker image named ml-app whose version is 0.0.1 and the push it to a local registry running at 10.10.1.1:5000.
Now our docker image is built and is available to use, we can use it any number of time and concurrently on different ports. In all future exercises we will be using the same docker image.

For instance we let's run a docker container on port 8000

``` shell
docker run -d -p 8000:5000 10.10.1.1:5000/ml-app:0.0.1
```

-   -d is for detach mode.
-   -p is to assign the port host_port:container_port.

To get the URL on which to access the service, run

```shell
echo "http://$(hostname):8000"
```

Copy this URL, and paste it into the address bar in your browser.

Try doing some predictions.

Once you are done using the container, You can stop it by following the steps mentioned:

First you need to get CONTAINER ID, it can be obtained by running

``` shell
docker ps

```

The output will be similar to :

```shell
CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                      NAMES
86c2a79287be        10.10.1.1:5000/ml-app:0.0.1   "python app.py"          10 hours ago        Up 10 hours         0.0.0.0:32001->5000/tcp     gracious_lederberg
9447cbb6496f        38f903b54010                  "kube-scheduler --au…"   16 hours ago        Up 16 hours                                    k8s_kube-scheduler_kube-scheduler-node-0_kube-system_b4fe9dc90ea45aa3cd69106e8d5a65d1_1
569805b52f8a        registry:2                    "/entrypoint.sh /etc…"   21 hours ago        Up 21 hours         10.10.1.1:5000->5000/tcp   local-registry
527b611e2ea3        quay.io/metallb/speaker       "/speaker --port=747…"   21 hours ago        Up 21 hours                                    k8s_speaker_speaker-m8622_metallb-system_9ef6d1ab-8732-43ae-a98c-df7bd134ad57_0
2ca68ecfde5f        k8s.gcr.io/pause:3.3          "/pause"                 21 hours ago        Up 21 hours                                    k8s_POD_speaker-m86
```
Copy the CONTAINER ID, like for the case above, the id will be "86c2a79287be", and the run the command:

``` shell
docker stop 86c2a79287be

```

Here for our experiment, you may need to change the classification model, once you change it you need to rebuild the conatiner to make sure that the changes are reflecting in container.

To rebuild the container follow the same step as you did above while building the container for the first time.

``` shell

docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  10.10.1.1:5000/ml-app:0.0.1
docker push 10.10.1.1:5000/ml-app:0.0.1
```

In future exercises too you need to follow the same process to rebuild a container.

This exercise is complete here.
=======
>>>>>>> 9e6db1c4fca74ce4defef213925b6f5b59b7efe7
