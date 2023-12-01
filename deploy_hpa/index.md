## Exercise: Deploy a service with dynamic scaling

When we used load balancing to distribute incoming traffic across multiple pods, the response time under load was much faster. But during time intervals when the load is not heavy, it may be wasteful to deploy so many pods. (The application is loaded and uses memory and some CPU even when there are no requests!)

To address this issue, we can use scaling - where the resource deployment changes in response to load on the service. In this exercise, specifically we use **horizontal scaling**, which adds more pods/replicas to handle increasing levels of work, and removes pods when they are not needed. (This is in contrast to **vertical scaling**, which would increase the resources assigned to pods - CPU and memory - to handle increasing levels of work.)

The manifest file for deploying a service with scaling is "deployment_hpa.yaml", and it is inside the "~/k8s-ml/deploy_hpa" directory. You can see it [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_hpa/deployment_hpa.yaml).

There are two differences between this deployment and the previous deployment:

* in this one, we add a service of `type: HorizontalPodAutoscaler`. We specify the minimum number of replicas and maximum number of replicas we want to have in our deployment, and the condition under which to increase the number of replicas. (This `HorizontalPodAutoscaler` service is *in addition to* the `LoadBalancer` service, which is also in place.)
* in this one, we specify `replicas: 1` again in the deployment - the initial deployment has 1 replica, but it may be scaled up to 5 by the autoscaler. 


To start this deployment, we will run:

``` 
kubectl apply -f ~/k8s-ml/deploy_hpa/deployment_hpa.yaml
```

Let's check the status of the service. Run the command:

```
kubectl get svc -o wide
```

and then

```
kubectl get pods -o wide
```

Initially, you will see one pod in the deployment. Wait until the pod is "Running" and has a "1/1" in the "Ready" column.

Get the URL of the service - run

```
echo http://$(curl -s ipinfo.io/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there. 

### Test deployment under load

You will need two SSH sessions on node-0. In one, run

```
kubectl get hpa --watch
```

to see the current state of the autoscaler.


 In the second SSH session, run


```
siege -c 10 -t 360s http://$(curl -s ipinfo.io/ip):32000/test
```

Note that this test is of a longer duration, so that you will have time to observe additional replicas being brought up and becoming ready to use. 

### Stop the deployment

When you are done with your experiment, make sure to delete the deployment and services. To delete, run the command:

```
kubectl delete -f  ~/k8s-ml/deploy_hpa/deployment_hpa.yaml
```

Use

``` 
kubectl get pods -o wide
```

and verify that (eventually) no pods are running your app.

