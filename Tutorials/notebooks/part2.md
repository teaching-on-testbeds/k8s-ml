::: {.cell .markdown}

## Exercise 3: Scaling a ML-app (Part-1)

Last exercise, we deployed a ML app on kubernetes pod, and we saw that the app was working fine, but what will happen if a lot of traffic comes to the app? The single web service soon becomes overwhelmed, causing slow response times and even downtime. To fix this problem what we can do is create multiple pods and evenly distribute the traffic on each of the pod and this process of evenly distributing traffic on the pods is known as **Load balancing**.

In this exercise our core focus will be to understand and implement the concept of **Load Balancing**.

Load balancing in a Kubernetes cluster involves distributing incoming network traffic across multiple instances of a particular application, service or pod. This is done using a load balancer that sits in front of the application instances or pods and distributes traffic to each of them based on a set of rules or algorithms. Here in our case our load balancer will be using Round Robin algoritm to distribute traffic.

The diagram below shows how exactly traffic flows in a load balancer.

![Load_balancer](images/load_balancer.png)


The core idea is that you have multiple pods running and the traffic is always redirected to the pod which is not busy and is least utilized.

Let's see a demo to verify that the response always comes from a different pod.

ssh into node-0

```shell
$ ssh cspandey@pc827.emulab.net

```

create a directory load_balancing_demo

``` shell
$ mkdir load_balancing_demo
$ cd load_balancing_demo
```

Get a sample deployment.yaml file that can be used to deploy a load balancer as service.

``` shell
$ wget https://github.com/indianspeedster/deploy_loadbalancer.yaml
```

Deploy load balancer as a service.

``` shell
$ kubectl apply -f deploy_loadbalancer.yaml

```

The command above will deploy 5 replicas of a simple flask app which return output as hello user from "pod_name". pod_name is the name of the pod from which the user is getting a response.

got to your web browser and enter public ip of any of your node and port 32000, you will get a response.




To see all the pods running you can run the command:

``` shell
$ kubectl get pods

```
You can match the pod_name with the pod from which you are getting response.

Also, to check that at a specific time how much cpu memory a pod is using, run the command:

``` shell

$ kubectl top pods

```

So, Now we understood that how exactly load balancing work.

Next step will be to deploy a ML app with a load balancer.

The steps will be similar with what we did in exercise 2. the only difference is that now we will be using a seperate deployment.yaml file which will specify that we will be creating 5 different replicas of the same ml app on 5 seperate pods.

Clone the repository that contains the the Flask ML app to your remote:

``` shell
$ git clone https://github.com/teaching-on-testbeds/k8s-ml-lb.git

```
get inside the repository:

``` shell
$ cd k8s-ml-lb
```

get your ml model from your local through scp and make sure that the model is named as ml-lb.h5

Create a docker image for the ml-app by using the command.

``` shell
$ docker build -t --no-cache ml-app:latest .

```

Tag the docker image to push it to the local registry

``` shell
$ docker tag ml-app:latest  10.10.1.1:5000/ml-app:latest

```

Push the image to the registry:

``` shell
$ docker push 10.10.1.1:5000/ml-app:latest

```

The last task is to launch the scaled ML application by utilizing a load balancer that has a static scaling configuration of five pods.

On your remote terminal run:

``` shell
$ kubectl apply -f deployment_lb.yaml

```

To check if the deployment is running fine after 2 mins run 

``` shell
$ kubectl get pods

```

If the status of all pods says as "Running" this means that the pods are healthy and running fine.

open your browser and run ip:32000 (here ip is the public ip of any of your nodes) and you can see that your ml app is up and running try making predictions.

**Testing Load balancing**

*Content to be added*
:::