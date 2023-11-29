## Exercise: Deploy your service using container orchestration (Kubernetes)

In the previous exercise, we deployed a container by running it directly. Now, we will deploy the same container using Kubernetes, a platform for container orchestration.

What are some benefits of using a container orchestration framework like Kubernetes, rather than deploying containers directly?

- *Container Orchestration:* Kubernetes helps to automate the deployment, scaling and management of containers. 
- *Self-healing:* If a container fails, Kubernetes can automatically detect it and replace it with a functional container.
- *Load balancing:* Kubernets can distribute traffic for an application across multiple instances of running containers. (We'll try this in the next exercise.)
- *Resource management:* Kubernetes allows you to set resource limits for containers, to ensure that the application has the resources to run efficiently.

*Pods* are the basic components in Kubernetes, and are used to deploy and manage containerized applications in a scalable and efficient way. They are designed to be ephemeral, meaning they can be created, destroyed, and recreated as needed. They can also be replicated, which allows for load balancing and high availability.

Although we will eventually deploy pods across all three of our "worker" nodes, our deployment will be managed from the "controller" node, which is "node-0".

To deploy an app on a Kubernetes cluster, we use a manifest file, which describes our deployment. For this exercise, we will use the "deployment_k8s.yaml" file inside the "deploy_k8s" directory, which you can see [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_k8s/deployment_k8s.yaml).

This manifest file defines a Kubernetes service named "flask-test-service" and a Kubernetes deployment named "flask-test-app".

* Inside the service definition, you can see the ports that will be used by the deployment. 
* Inside the deployment definition, you can see that 
   * the "ml-app" container you built earlier will be retrieved from the local registry ("node-0:5000/my-app:0.0.1"), 
   * and it will not be cached ("imagePullPolicy: Always"), 
   * the deployment will include just a single copy of our pod ("replicas: 1").


It also defines the resource requirements of the container, in terms of CPU cores and memory. The "request" defines the minimum resource a container may get, and the "limit" defines the maximum resource a container may get.

To start this deployment, we will run:

``` 
kubectl apply -f ~/k8s-ml/deploy_k8s/deployment_k8s.yaml
```

and make sure the following output appears:

```
service/flask-test-service created
deployment.apps/flask-test-app created
```

Wait a few minutes for the pod to start running.

To check the status of deployment, run:

``` 
kubectl get pods -o wide
```

The output will include a line similar to

```
NAME                                               READY   STATUS              RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
flask-test-app-7b4c8648c6-r8zvv                    0/1     ContainerCreating   0          22s     <none>        node-2   <none>           <none>
```

Here the status of the pod is `ContainerCreating`, which means the container is getting ready. When it reaches the `Running` state, then it means the pod is healthy and is running.

Since our pod is running on the cluster via a service, we also need to check the status of the service. Run the command:

``` shell
kubectl get svc -o wide
```
The output will include a line similar to

```
NAME                 TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)         AGE     SELECTOR
flask-test-service   NodePort    10.233.37.25   <none>        6000:32000/TCP   12m     app=flask-test-app
```

Once the pod is running, you can see the resource usage (CPU and memory) of the pod with

```
kubectl top pod
```

Get the URL of the service - run

```
echo http://$(curl -s ipinfo.io/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there. (As before, if your model is large, it may take a while before it is ready to accept requests.)

### Test deployment under load

To test the load on the deployment we will use Siege, a command-line tool used to test and analyze the performance of web servers. It can generate a significant amount of traffic to test the response of a web server under load.

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

When you are done with your experiment, make sure to delete the deployment and service. To delete, run the command:

``` 
kubectl delete -f ~/k8s-ml/deploy_k8s/deployment_k8s.yaml
```
and look for output like

```
service "flask-test-service" deleted
deployment.apps "flask-test-app" deleted
```


