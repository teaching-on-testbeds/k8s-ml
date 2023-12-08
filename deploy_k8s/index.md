## Exercise: Deploy your service using container orchestration (Kubernetes)

In the previous exercise, we deployed a container by running it directly. Now, we will deploy the same container using Kubernetes, a platform for container orchestration.

What are some benefits of using a container orchestration framework like Kubernetes, rather than deploying containers directly?

- *Container Orchestration:* Kubernetes helps to automate the deployment, scaling and management of containers. 
- *Self-healing:* If a container fails, Kubernetes can automatically detect it and replace it with a functional container.
- *Load balancing:* Kubernets can distribute traffic for an application across multiple instances of running containers. (We'll try this in the next exercise.)
- *Resource management:* Kubernetes allows you to set resource limits for containers, to ensure that the application has the resources to run efficiently.

*Pods* are the basic components in Kubernetes, and are used to deploy and manage containerized applications in a scalable and efficient way. They are designed to be ephemeral, meaning they can be created, destroyed, and recreated as needed. They can also be replicated, which allows for load balancing and high availability.

Although we will eventually deploy pods across all three of our "worker" nodes, our deployment will be managed from the "controller" node, which is "node-0".

To deploy an app on a Kubernetes cluster, we use a manifest file, which describes our deployment. For this exercise, we will use the "deployment_k8s.yaml" file inside the "~/k8s-ml/deploy_k8s" directory, which you can see [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_k8s/deployment_k8s.yaml).

This manifest file defines a Kubernetes service named "ml-kube-service" and a Kubernetes deployment named "ml-kube-app".

* Inside the service definition, we create a service of `type: NodePort`. This service passes incoming requests on a specified port, to a (different) port on the pod. 
* Inside the deployment definition, you can see that 
   * the "ml-app" container you built earlier will be retrieved from the local registry ("node-0:5000/ml-app:0.0.1"), 
   * the deployment will include just a single copy of our pod ("replicas: 1").
   * there is a "readiness" probe defined - the container is considered "Ready" and requests will be forwarded to it only when it responds with a success code to 3 HTTP requests on the `/test` endpoint.


It also defines the resource requirements of the container, in terms of CPU cores and memory. The "request" defines the minimum resource a container may get, and the "limit" defines the maximum resource a container may get.

To start this deployment, we will run:

``` 
kubectl apply -f ~/k8s-ml/deploy_k8s/deployment_k8s.yaml
```

and make sure the following output appears:

```
service/ml-kube-service created
deployment.apps/ml-kube-app created
```


Let's check the status of the service. Run the command:

``` shell
kubectl get svc -o wide
```

The output will include a line similar to

```
NAME                 TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)         AGE     SELECTOR
ml-kube-service   NodePort    10.233.37.25   <none>        6000:32000/TCP   12m     app=ml-kube-app
```

It may take a few minutes for the pod to start running. To check the status of pods, run:



``` 
kubectl get pods -o wide
```

The output may include a line similar to

```
NAME                                               READY   STATUS              RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
ml-kube-app-7b4c8648c6-r8zvv                    0/1     ContainerCreating   0          22s     <none>        node-2   <none>           <none>
```

In this example, the status of the pod is `ContainerCreating`, which means the container is getting ready. When it reaches the `Running` state, then it means the pod is healthy and is running. When it shows "1/1" in the "Ready" column, it is ready to accept requests according to the probe we had set up.

(As before, if your model is large, it may take a while before it is ready to accept requests.)


Once the pod is ready, check the resource usage (CPU and memory) of the pod with

```
kubectl top pod
```

Note that the resource usage varies depending on whether or not the pod is currently serving a request!

Get the URL of the service - run

```
echo http://$(curl -s ipinfo.io/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there. 

### Test deployment under load

To test the load on the deployment we will use [siege](https://linux.die.net/man/1/siege), a command-line tool used to test and analyze the performance of web servers. It can generate a significant amount of traffic to test the response of a web server under load.

Install Siege on node-0:

```
sudo apt-get update; sudo apt-get -y install siege
```

Open a second SSH session on node-0. In one, run

```
watch -n 5 kubectl top pod
```

to monitor the pod's resource usage in real time (This will be updated every 5 seconds). In the second SSH session, run


```
siege -c 10 -t 30s http://$(curl -s ipinfo.io/ip):32000/test
```

Here Siege will generate traffic to a "test" endpoint on your website, which requests a prediction for a pre-saved image, for 30 seconds with a concurrency level of 10 users. After it finishes execution, make a note of key results - how many transactions were served successfully, how many failed, the transaction rate, and what the average response time was (note that this includes inference time, as well as several other elements). 


### Stop the deployment


When you are done with your experiment, make sure to delete the deployment and service. To delete, run the command:

``` 
kubectl delete -f ~/k8s-ml/deploy_k8s/deployment_k8s.yaml
```

and look for output like

```
service "ml-kube-service" deleted
deployment.apps "ml-kube-app" deleted
```

Use

``` 
kubectl get pods -o wide
```

and verify that (eventually) no pods are running your app.