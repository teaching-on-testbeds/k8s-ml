::: {.cell .markdown}

## Exercise: Deploy an image classification app on cloud.

For this exercise we will use a flask app to deploy the food classification model you build in lab 8.

To download the content of the app clone this repository "https://github.com/teaching-on-testbeds/k8s-ml" or run the following command in your terminal.

``` shell
git clone https://github.com/indianspeedster/Deploy_flask.git
```

The content of the repository contains everything but the model which you want to deploy so now we will transfer the model from your local host to remote host.

``` shell
scp "path of saved model" "name of remote host":"/users/{username}/Deploy_flask/"

```

Now we have our model which we are going to deploy.

Before going ahead make sure that the folder structure is same as in the picture below

![Folder structure for the flask-app](images/folder.png)

Now we are ready to run the flask app, before that you should check what is the public ip from which the content of the app can be accessed.

``` shell
$ curl ifconfig.me
```

The output of this command is the public ip of our remote host.


We will be using Docker to containerise the ml-app. Learning Docker is a large process and that is not the part of this exercise. To make sure that you don't get stuck with docker, a Dockerfile is already provided in the repository you cloned.

Before we move ahead let's check if we have docker installed in our system.

``` shell
$ docker -v

```

The output should be similiar to 

```shell

Docker version 19.03.15, build 99e3ed8919

```
The next step is to get into ks8-ml directory

``` shell
$ cd Deploy_flask

```

Next step is to create a docker image of our flask app and push it to the local registry running at 10.10.1.1:5000

``` shell

$ docker build -t my-app:0.0.1 .
$ docker tag my-app:0.0.1  10.10.1.1:5000/my-app:0.0.1
$ docker push 10.10.1.1:5000/my-app:0.0.1

```
Now our docker image is build and is available to use, we can use it any number of time and concurrently on different ports

For instance we let's run a docker container on port 32001

``` shell
$ docker run -d -p 32001:5000 10.10.1.1:5000/my-app

```
 - -d is for detach mode.
 - -p is to assign the port host_port:container_port.

Get the public ip of your host, go to your browser and run {public_ip}:32001, you will see that your app is up and running there.

This exercise is complete here.

:::

