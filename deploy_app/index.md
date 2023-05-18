## Exercise: Deploy an image classification app on cloud.

SSH into Master node (node-0 ) of your cluster and leave the terminal open.




Clone this repository that contains all the material needed in the further exercises.

``` shell
git clone https://github.com/teaching-on-testbeds/k8s-ml.git
```

Transfer the model that you trained in the prev exercise.

Run the below mentioned command 

``` shell
echo scp model.h5 $USER@$(curl -s ipinfo.io/ip):~/k8s-ml/app

```

Copy the output of the command , leave the SSH session running and open a new local terminal, change directory to the directory where your model is saved and paste the command you copied and hit enter.
if the output looks like this:

``` shell
model.h5                                                                                                                  100%  155MB   8.9MB/s   00:17
```
Your model is transfered from your local to remote.

if you get a "Permission denied (publickey)." error, make sure to add "-i ~/.ssh/id_rsa_chameleon" after scp.


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
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

The command above will build a docker image named ml-app whose version is 0.0.1 and the push it to a local registry running at node1:5000.
Now our docker image is built and is available to use, we can use it any number of time and concurrently on different ports. In all future exercises we will be using the same docker image.

For instance we let's run a docker container on port 32000

``` shell
docker run -d -p 32000:5000 node-0:5000/ml-app:0.0.1
```

-   -d is for detach mode.
-   -p is to assign the port host_port:container_port.

Run the below mentioned command in the same terminal:

``` shell
echo http://$(curl -s ipinfo.io/ip):32000
```

copy the output of the previous command, open your browser and paste the same, you will see that your app is up and running there.

Try doing some predictions.

To test the load on the deployment we will use siege. Siege is a command-line tool used to test and analyze the performance of web servers. It can generate a significant amount of traffic to test the response of a web server under load.

Install siege in your system

```shell
sudo apt-get install siege

```
and then run 

``` shell
echo siege -c 10 -t 120s http://$(curl -s ipinfo.io/ip):32000/test

```
copy the output of the command and paste them into your web browser.

Here Siege will generate traffic to your website for 120 seconds with a concurrency level of 10 users.


Once you are done using the container, You can stop it by running the below mentioned command:


``` shell
docker stop $(docker ps -q -f ancestor=ml-app:0.0.1)

```

Here for our experiment, you may need to change the classification model, once you change it you need to rebuild the conatiner to make sure that the changes are reflecting in container.

To rebuild the container follow the same step as you did above while building the container for the first time.

``` shell

docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

In future exercises too you need to follow the same process to rebuild a container.

This exercise is complete here.
