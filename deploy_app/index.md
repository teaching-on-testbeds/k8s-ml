::: {.cell .markdown}

## Exercise: Deploy an image classification app on cloud.

For this exercise we will use a flask app to deploy the food classification model you build in lab 8.

To download the content of the app run the following command in your terminal.

``` shell
wget https://github.com/teaching-on-testbeds/k8s-ml/tree/main/app

```

The content of the repository contains everything but the model which you want to deploy so now we will transfer the model from your local host to remote host. Make sure that your model is named as "model.h5"

``` shell
scp "path of saved model" "name of remote host":"/users/{username}/app/"

```

After transfering the file again log in to node-0.


Now we are ready to run the flask app, before that you should check what is the public ip from which the content of the app can be accessed.

``` shell
curl ifconfig.me
```

The output of this command is the public ip of our remote host.


We will be using Docker to containerise the ml-app. Learning Docker is a large process and that is not the part of this exercise. To make sure that you don't get stuck with docker, a Dockerfile is already provided in the app you downloaded.

Before we move ahead let's check if we have docker installed in our system.

``` shell
docker -v

```

The output should be similiar to 

```shell

Docker version 19.03.15, build 99e3ed8919

```
The next step is to get into app directory which contains flask app

``` shell
cd app

```


Before going ahead make sure that the folder structure is same as below

- app
    - instance
    - static
    - templates
    - app.py
    - Dockerfile
    - requirements.txt
    - model.h5

Next step is to create a docker image of our flask app and push it to the local registry running at 10.10.1.1:5000

``` shell

docker build -t my-app:0.0.1 .
docker tag my-app:0.0.1  10.10.1.1:5000/my-app:0.0.1
docker push 10.10.1.1:5000/my-app:0.0.1

```
Now our docker image is built and is available to use, we can use it any number of time and concurrently on different ports. In all future exercises we will be using the same docker image.

For instance we let's run a docker container on port 32001

``` shell
docker run -d -p 32001:5000 10.10.1.1:5000/my-app

```
 - -d is for detach mode.
 - -p is to assign the port host_port:container_port.

Get the public ip of your host, go to your browser and run {public_ip}:32001, you will see that your app is up and running there.

Try doing some predictions.

Once you are done using the app, You can stop it by below mentioned command:

``` shell
docker stop 10.10.1.1:5000/my-app

```
This exercise is complete here.

:::

