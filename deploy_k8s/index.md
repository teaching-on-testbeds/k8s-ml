
## Exercise 2: Deploy an image classification App on a kubernetes Pod.

Before going ahead first let's understand what is kubernetes.

**Kubernetes** is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. It was originally developed by Google and is now maintained by the Cloud Native Computing Foundation (CNCF).

**Key Features**

- *Container Orchestration:* Kubernetes helps to automate the deployment, scaling and management of applications that are containerized. it also helps to manage containers and their interdependency.


- *Self-healing:* If any containers fail, kubernetes can automatically detect it and replace it with a fully functional container and make sure that the application is always available and running.


- *Service discovery and load balancing:* Kubernetes provides a built-in service discovery mechanism which helps containers to find other containers running inside the cluster and communicate with each other, even as they are dynamically created and destroyed. So, everytime a new container comes up, we don't need to network the same with other containers but it by default gets networked. Kubernetes also have a built-in load balancing mechanism that can distribute traffic across multiple instances of your application. In next exercise we will be implementing load balancing on our app.


- *Resource management:* Kubernetes allows you to set resource limits and requests for your applications, ensuring that the application have the resources to run efficiently. we will see the implementation of this in exercise 4 where we limit the cpu usage by 40%.

**Pods** : Pods are the basic components in Kubernetes and are used to deploy and manage containerized applications in a scalable and efficient way.They are designed to be ephemeral, meaning they can be created, destroyed, and recreated as needed. They can also be replicated, which allows for load balancing and high availability.

Since, Kubernetes is a Container Orchestration platform so we need containers to go ahead with deploying an application on kubernetes. Here in our execise we will be using Docker container.



In our cluster node-1 is the master node so we will log into node-1.

To deploy an app on a kubernetes cluster we need a manifest file. We have the manifest in the folder deploy_k8s named as deployment_k8s.yaml , lets go to the folder :

``` shell

cd ~/k8s-ml/deploy_k8s

```

Next let's understand what is there in the deployment_k8s.yaml file.


```Shell
cat deployment_k8s.yaml

```

The output will look like this:

```shell 
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
        image: node1:5000/ml-app:0.0.1
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

Here, the manifest file defines a kubernetes service with name flask-test-service and a kubernetes deployment named flask-test-app.

In the service you can see the ports are defined on which the app will be served. Port is the port of the cluster, targetPort  is the port of container and nodePort is the port of the three nodes. 

In the deployment flask-test-app you have a container which will pull the docker image 10.10.1.1:5000/my-app:0.0.1 from the local registry, "imagePullPolicy: Always" means that the app won't be using cached image and every time the deployment is created it will pull a new image from the registry.

The last and final step is to apply the content of the deployment_k8s.yaml file. run the command below to do so:

``` shell
kubectl apply -f deployment_k8s.yaml

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
kubectl get pods -o wide

```
The output will look similar to

``` shell
NAME                                               READY   STATUS              RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
flask-test-app-7b4c8648c6-r8zvv                    0/1     ContainerCreating   0          22s     <none>        node-2   <none>           <none>
nfs-subdir-external-provisioner-7567fc7fcf-6qkcj   1/1     Running             0          3d21h   192.168.5.4   node-2   <none>           <none>

```
Here the status of the pod shows ContainerCreating which means the container is getting ready.

if the status of pods shows as Running then it means the pod is healthy and is running.

Since our pod is running on the cluster via a service, we also need to check the status of the service. To check run the command:

``` shell
kubectl get svc -o wide
```
The output will look similar to 

```shell
NAME                 TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)         AGE     SELECTOR
flask-test-service   NodePort    192.168.153.237   <none>        6000:32000/TCP   2m20s   app=flask-test-app
kubernetes           ClusterIP   192.168.128.1     <none>        443/TCP         3d21h   <none>
```
The port shows as 6000:32000/TCP which means the service is running inside the cluster on port 6000 and is binded to port 32000 of our nodes.


Next open your browser and enter floating_ip of any of the node:32000 which can be similar to 192.5.86.230:32000, you will see that your app is up and running there.




When you are done with your experiment, make sure to delete the deployment and service. To delete run the command:

``` shell
kubectl delete -f deployment_k8s.yaml

```
if the output looks similar to 

```shell
service "flask-test-service" deleted
deployment.apps "flask-test-app" deleted
```
The deployment is deleted.

This exercise is complete.


