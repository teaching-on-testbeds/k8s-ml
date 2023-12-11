## Exercise: Deploy your service with load balancing

In the previous exercise, we deployed a single replica of a Kubernetes pod. But if the load on the service is high, the single pod will have slow response times. We can address this by deploying multiple "replicas" of the pod, and distributing the traffic across them by assigning each incoming request to a pod. This is called **load balancing**.

The manifest file for deploying a load balanced service is named "deployment_lb.yaml", and it is inside the "~/k8s-ml/deploy_lb" directory. You can see it [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_lb/deployment_lb.yaml).


This manifest file defines a Kubernetes service of type `LoadBalancer` with the name "ml-kube-service" and a Kubernetes deployment named "ml-kube-app". There are two major differences between this deployment and the previous deployment:

* in this one, we specify that the service is of `type: LoadBalancer`, i.e. instead of directly passing incoming requests to one pod, will place a load balancer service in "front" of the pods that will distribute the requests across pods.
* in this one, we specify `replicas: 5` where previously we used `replicas: 1`.

To start this deployment, we will run:

```
kubectl apply -f ~/k8s-ml/deploy_lb/deployment_lb.yaml
```

and make sure the following output appears:

```
service/ml-kube-service created
deployment.apps/ml-kube-app created
```

It will take a few minutes for the pods to start running. To check the status of deployment, run:

``` 
kubectl get pods -o wide
```

and wait until the output shows that all pods are in the "Running" state and show as "1/1" in the "Ready" column. Note that the pods will be deployed across all of the nodes in the cluster. Also note that if some pods are "Ready" but not others, requests will be sent only to the pods that are "Ready".

Once the pods are ready, you can see the resource usage (CPU and memory) of the pods with

```
kubectl top pod
```

Get the URL of the service - run

``` shell
echo http://$(curl -s ifconfig.me/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there. 

### Test deployment under load

As before, we will test this deployment under load. Open a second SSH session on node-0. In one, run

```
watch -n 5 kubectl top pod
```

to monitor the pod's resource usage in real time (This will be updated every 5 seconds). In the second SSH session, run


```
siege -c 10 -t 30s http://$(curl -s ifconfig.me/ip):32000/test
```

After it finishes execution, make a note of key results - how many transactions were served successfully, how many failed, the transaction rate, and what the average response time was (note that this includes inference time, as well as several other elements). 

### Stop the deployment


When you are done with your experiment, make sure to delete the deployment and service. To delete, run the command:

``` 
kubectl delete  -f ~/k8s-ml/deploy_lb/deployment_lb.yaml
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
