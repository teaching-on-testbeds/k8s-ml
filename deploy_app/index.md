## Exercise: Deploy an image classification app on cloud.

SSH into Master node (node-0 for CloudLab and node1 for Chameleon) of your cluster and leave the terminal open.

For this exercise we will use a flask app to deploy the food classification model you built in https://colab.research.google.com/drive/16w-mLZ4tSxwH7bZof-1Baota-TIYv19B.


To download the content of the flask app run the following command in your terminal.

``` shell
git clone https://github.com/teaching-on-testbeds/k8s-ml.git
```

The content of the repository contains everything but the model which you want to deploy. Go to the colab notebook, Train and test the model inside colab, save it by adding the below mentioned python code in the last cell of the notebook.

```python
model.save("model.h5")

```
then download the saved model from Colab (use the file brower on the side to locate and download the saved model).

Leave the SSH session running and open a new local terminal, change directory to the directory where your model is saved and run the below mentioned scp command to transfer the model to remote.

``` shell
scp model.h5 "name of remote host":/users/username/k8s-ml/app/

```

The name of the remote host can be obtained by copying from the list view of cloudlab home page.
it looks similar to "username@pc724.emulab.net" also remove username by your CloudLab username. Make sure to copy the name of the remote host as it's needed in the future exercises.

Once the file is transfered, open the ssh session at node-0

Now we are ready to run the flask app, We will be using Docker to containerise the ml-app. Learning Docker is a large process and that is not the part of this exercise. To make sure that you don't get stuck with docker, a Dockerfile is already provided in the app you downloaded.

Before we move ahead let's check if we have docker installed in our system.

``` shell
docker -v
```

The output should be similiar to

``` shell

Docker version 19.03.15, build 99e3ed8919
```

The next step is to get into app directory which contains flask app

``` shell
cd k8s-ml/app
```

Before going ahead make sure that the folder structure is same as below

-   app
    -   instance
    -   static
    -   templates
    -   app.py
    -   Dockerfile
    -   requirements.txt
    -   model.h5

Next step is to create a docker image of our flask app and push it to the local registry running at node1:5000

``` shell

docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  node1:5000/ml-app:0.0.1
docker push node1:5000/ml-app:0.0.1
```

The command above will build a docker image named ml-app whose version is 0.0.1 and the push it to a local registry running at node1:5000.
Now our docker image is built and is available to use, we can use it any number of time and concurrently on different ports. In all future exercises we will be using the same docker image.

For instance we let's run a docker container on port 32000

``` shell
docker run -d -p 32000:5000 node1:5000/ml-app:0.0.1
```

-   -d is for detach mode.
-   -p is to assign the port host_port:container_port.

Open your browser and enter "name of the remote host":32000 which can be similar to "username@pc724.emulab.net:32000", you will see that your app is up and running there.

Try doing some predictions.

To test the load on the deployment we will use siege. Siege is a command-line tool used to test and analyze the performance of web servers. It can generate a significant amount of traffic to test the response of a web server under load.

Install siege in your system

```shell
sudo apt-get install siege

```
and then run 

``` shell
siege -c 10 -t 120s http://{enter the url on which the app is running}/test

```
Here Siege will generate traffic to your website for 120 seconds with a concurrency level of 10 users.


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
docker tag ml-app:0.0.1  node1:5000/ml-app:0.0.1
docker push node1:5000/ml-app:0.0.1
```

In future exercises too you need to follow the same process to rebuild a container.

This exercise is complete here.
