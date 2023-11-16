## Exercise: Deploy your service with load balancing

In the previous exercise, we deployed a single replicate of a Kubernetes pod. But if the load on the service is high, the single pod will have slow response times. We can address this by deploying multiple pods, and distributing the traffic across them by assigning each incoming request to a pod. This is called **load balancing**.

The manifest file for deploying a load balanced service is named "deployment_lb.yaml", and it is inside the "deploy_lb" directory.


``` shell
cd ~/k8s-ml/deploy_lb
cat deployment_lb.yaml
```

You can also view the manifest file [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_lb/deployment_lb.yaml).


Here, the manifest file defines a Kubernetes service of type LoadBalancer with name "flask-test-service" and a Kubernetes deployment named "flask-test-app".

Next we will deploy this using the manifest file:

``` shell
kubectl apply -f deployment_lb.yaml

```

To check if the deployment is running, after a couple of minutes run 

``` shell
kubectl get pods

```

If the status of all pods says as "Running" this means that the pods are healthy and running fine.

Get the URL of the service - run

``` shell
echo http://$(curl -s ipinfo.io/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there.

and then to stress test your deployment run: 

``` shell
siege -c 10 -t 30s http://$(curl -s ipinfo.io/ip):32000/test
```
Make a note of key results - how many transactions were served successfully, how many failed, and what the average response time was. You should see an improvement relative to the single pod deployment!

When you are done with your experiment, make sure to delete the deployment and service:

``` shell
kubectl delete -f deployment_lb.yaml

```
