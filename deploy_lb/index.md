## Exercise 3: Scaling a ML-app (Part-1)

Last exercise, we deployed a ML app on kubernetes pod, and we saw that the app was working fine, but what will happen if a lot of traffic comes to the app? The single web service soon becomes overwhelmed, causing slow response times and even downtime. To fix this problem what we can do is create multiple pods and evenly distribute the traffic on each of the pod and this process of evenly distributing traffic on the pods is known as **Load balancing**.

In this exercise our core focus will be to understand and implement the concept of **Load Balancing**.

Load balancing in a Kubernetes cluster involves distributing incoming network traffic across multiple instances of a particular application, service or pod. This is done using a load balancer that sits in front of the application instances or pods and distributes traffic to each of them based on a set of rules or algorithms. Here in our case our load balancer will be using Round Robin algoritm to distribute traffic.

The diagram below shows how exactly traffic flows in a load balancer.

![Load_balancer](/images/load_balancer.png)


The core idea is that you have multiple pods running and the traffic is always redirected to the pod which is not busy and is least utilized.


To deploy an app with a load balancer we will be needing a manifest file. To file is already there in the folder deploy_lb named as deployment_lb.yaml.


``` shell
cd ~/k8s-ml/deploy_lb
```

Next let's understand what is there in the deployment_lb.yaml file.

```shell
cat deployment_lb.yaml
```

The output will be as follow

``` shell
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
  type: LoadBalancer


---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-test-app
spec:
  selector:
    matchLabels:
      app: flask-test-app
  replicas: 5
  template:
    metadata:
      labels:
        app: flask-test-app
    spec:
      containers:
      - name: flask-test-app
        image: node-0:5000/ml-app:0.0.1
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
        resources:
          limits:
            cpu: "8"
            memory: "5Gi"
          requests:
            cpu: "5"
            memory: "5Gi"
```

Here, the manifest file defines a kubernetes service of type LoadBalancer with name flask-test-service and a kubernetes deployment named flask-test-app.

In the service you can see the ports are defined on which the app will be served. Port is the port of the cluster, targetPort  is the port of container and nodePort is the port of the three nodes. 

In the deployment flask-test-app you have a container which will pull the docker image 10.10.1.1:5000/my-app:0.0.1 from the local registry, "imagePullPolicy: Always" means that the app won't be using cached image and every time the deployment is created it will pull a new image from the registry, you can see "replicas:5" which means that the deployment will create 5 replicas of the app and all will be served through the load balancer where the traffic will be divided equally.

Next step is to deploy this app with a load balancer through the help of the manifest file deployment_lb.yaml .

``` shell
kubectl apply -f deployment_lb.yaml

```

To check if the deployment is running fine after 2 mins run 

``` shell
kubectl get pods

```

If the status of all pods says as "Running" this means that the pods are healthy and running fine.

Run the below mentioned command in the same terminal:

``` shell
echo http://$(curl -s ipinfo.io/ip):32000
```

copy the output of the previous command, open your browser and paste the same, you will see that your app is up and running there.

and then to stress test your deployment run : 

``` shell
$(echo siege -c 10 -t 30s http://$(curl -s ipinfo.io/ip):32000/test)

```
Note the number of successfull hits

When you are done with your experiment, make sure to delete the deployment and service. To delete run the command:

``` shell
kubectl delete -f deployment_lb.yaml

```

This exercise is complete here.
