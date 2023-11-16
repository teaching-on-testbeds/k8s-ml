## Exercise: Deploy a service with dynamic scaling

When we used load balancing to distribute incoming traffic across multiple pods, the response time under load was much faster. But during time intervals when the load is not heavy, it may be wasteful to deploy so many pods.

To address this issue, we can use scaling - where the resource deployment changes in response to load on the service. In this exercise specifically we use horizontal scaling, which adds more pods to handle increasing levels of work, and removes pods when they are not needed.

Our manifest file for this deployment is "deployment_hpa.yaml", inside the "deploy_hpa" directory.

```shell
cd ~/k8s-ml/deploy_hpa
cat deployment_hpa.yaml
```

You can also view the manifest file [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_hpa/deployment_hpa.yaml).

This file defines a HorizontalPodAutoscaler that deploys 1-5 pods as needed, depending on the CPU utilization.

On your terminal run:

``` shell
kubectl apply -f deployment_hpa.yaml
```

to deploy the service, and run 

```shell
kubectl get pods
```

to check its status and make sure the pod or pods are Running.

Initially you will see that there is only one pod running, but when the traffic increases, the number of pods deployed will increase.


To test your deployment, run

``` shell
siege -c 10 -t 30s http://$(curl -s ipinfo.io/ip):32000/test
```

Once you complete this exercise make sure to delete the deployment and services:

```shell

kubectl delete -f deployment_hpa.yaml

```



