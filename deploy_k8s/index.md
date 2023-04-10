::: {.cell .markdown}

## Exercise 2: Deploy an image classification App on a kubernetes Pod.

Before going ahead first let's understand what is kubernetes.

**Kubernetes** is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It was originally developed by Google and is now maintained by the Cloud Native Computing Foundation (CNCF).

**Key Features**

- *Automated deployment and scaling:* Kubernetes automates the deployment and scaling of containerized applications, making it easier to manage and scale complex microservices architectures.
- *Self-healing:* Kubernetes monitors the health of your applications and automatically restarts or replaces containers if they fail or become unresponsive.
- *Service discovery and load balancing:* Kubernetes provides built-in service discovery and load balancing, making it easier to manage the networking aspects of your applications.
- *Rolling updates and rollbacks:* Kubernetes supports rolling updates and rollbacks, allowing you to deploy updates to your applications without downtime.
- *Config management:* Kubernetes provides built-in support for managing configuration files and secrets, making it easier to manage the configuration of your applications.
- *Resource management:* Kubernetes allows you to set resource limits and requests for your applications, ensuring that they have the resources they need to run properly.

**Pods** : Pods are a fundamental building block in Kubernetes and are used to deploy and manage containerized applications in a scalable and efficient way.They are designed to be ephemeral, meaning they can be created, destroyed, and recreated as needed. They can also be replicated, which allows for load balancing and high availability.

Since, Kubernetes is a Container Orchestration platform so we need containers to go ahead with deploying an application on kubernetes. Here in our execise we will be using Docker container.



In our cluster node-0 is the master node so we will SSH into node-0

``` shell
$ ssh cspandey@pc827.emulab.net

```

Next step is to get all the code into our remote host which will be used to deploy the application.

To download the content of the app clone this repository "https://github.com/teaching-on-testbeds/k8s-ml" or run the following command in your terminal.

``` shell
$ git clone https://github.com/indianspeedster/ml_app_on_ks_pod.git
$ cd ml_app_on_ks_pod
```
Now we have everything which we are going to need to deploy our app, the last thing we need to check is weather kubernetes and Docker is installed or not.

To check kubernetese version :

``` shell
$ kubectl -v
```
To check Docker version :

``` shell
$ docker -v
```

In the repository you will see there is a file named *Dockerfile*, this file will be used to create a docker image which further will be pulled by kubernetes pods.

to create a docker image run the following command in the shell also make sure that you are in the food_classification directory.

``` shell
$ docker build -t my-app:0.0.2 .

```

Now Docker image is ready, we can check the same by running the following command:

``` shell
$ docker images

```

Next step is to push the docker image to the docker registry which is accessible from the kubernetes cluster.
The docker resistry is on 10.10.1.1:5000

First we will tag the image, run the command below to do the same:

``` shell
$ docker tag my-app:latest  10.10.1.1:5000/my-app:0.0.2
```

Next we will push the image to the registry:

``` shell
$ docker push 10.10.1.1:5000/my-app:0.0.2
```

To make things simple and easy all our deployments would be done through a manifest file deployment.yaml . 

To check the content of deployment.yaml file, enter the following commands on your teminal:

``` shell
$ cat pod_deployment.yaml
```

compare the content of the file to make sure that you have loaded the correct file.

```Shell
$ cat pod_deployment.yaml

apiVersion: v1
kind: Service
metadata:
  name: flask-test-service
spec:
  selector:
    app: flask-test-app
  ports:
  - protocol: "TCP"
    port: 6000
    targetPort: 5000
    nodePort: 32000
  type: NodePort


---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-test-app
spec:
  selector:
    matchLabels:
      app: flask-test-app
  replicas: 1
  template:
    metadata:
      labels:
        app: flask-test-app
    spec:
      containers:
      - name: flask-test-app
        image: 10.10.1.1:5000/my-app:0.0.2
        imagePullPolicy: Always
        ports:
        - containerPort: 5000

```

The last and final step is to apply the content of the deployment.yaml file. run the command below to do so:

``` shell
$ kubectl apply -f pod_deployment.yaml
```

If the output looks similar to this

``` shell
service/flask-test-service created
deployment.apps/flask-test-app created
```

Then it means your deployment is successfull.

Since the content of our pod is large so it will take close to a minute for the pod to start running.

To check the status of pod run the below mentioned command:

``` shell
$ kubectl get pods -o wide
```

if the status of pods shows as Running then it means the pod is healthy and is running.

Since our pod is running on the cluster via a service, we also need to check the status of the service. To check run the command:

``` shell
$ kubectl get svc -o wide
```

In the output you will see the nodeport number, it is the same port number on which the app is running.

Next go to your browser and run ip of any of the nodes colon node port, eg: 192.168.56.453:32000  and you will see that your ml app is up and running, try predicting and hae fun ...!

:::