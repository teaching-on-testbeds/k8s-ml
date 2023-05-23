
## Exercise 2: Deploy your service using container orchestration (Kubernetes)

In the previous exercise, we deployed a container by running it directly. Now, we will deploy the same container using Kubernetes, a platform for container orchestration.

What are some benefits of using Kubernetes, rather than deploying containers directly?

- *Container Orchestration:* Kubernetes helps to automate the deployment, scaling and management of applications that are containerized. it also helps to manage containers and their interdependency.

- *Self-healing:* If a container fails, Kubernetes can automatically detect it and replace it with a fully functional container to make sure that the application is always available and running.
- *Service discovery and load balancing:* Kubernetes provides a built-in service discovery mechanism which helps containers to find other containers running inside the cluster and communicate with each other, even as they are dynamically created and destroyed. Kubernetes also has a built-in load balancing mechanism that can distribute traffic across multiple instances of your application. In next exercise we will be implementing load balancing on our app.
- *Resource management:* Kubernetes allows you to set resource limits and requests for your applications, ensuring that the application have the resources to run efficiently.

*Pods* are the basic components in Kubernetes and are used to deploy and manage containerized applications in a scalable and efficient way. They are designed to be ephemeral, meaning they can be created, destroyed, and recreated as needed. They can also be replicated, which allows for load balancing and high availability.

Although we will eventually deploy pods across all three of our nodes, our deployment will be managed from the "master" node, which is node-0.

To deploy an app on a Kubernetes cluster, we use a manifest file, which describes our deployment. For this exercise, we will use the "deployment_k8s.yaml" file inside the "deploy_k8s" directory, which you can see by running:

``` shell
cd ~/k8s-ml/deploy_k8s
cat deployment_k8s.yaml
```

You can also view the manifest file [here](https://github.com/teaching-on-testbeds/k8s-ml/blob/main/deploy_k8s/deployment_k8s.yaml).

This manifest file defines a Kubernetes service named "flask-test-service" and a Kubernetes deployment named "flask-test-app".

* Inside the service definition, you can see the ports that will be used by the deployment. 
* Inside the deployment definition, you can see that 
   * the "ml-app" container you built earlier will be retrieved from the local registry ("node-0:5000/my-app:0.0.1"), 
   * and it will not be cached ("imagePullPolicy: Always"), 
   * the deployment will include just a single copy of our pod ("replicas: 1").

To start this deployment, we will run:

``` shell
kubectl apply -f deployment_k8s.yaml

```

and make sure the following output appears:

``` shell
service/flask-test-service created
deployment.apps/flask-test-app created
```

It will take close to a minute for the pod to start running.

To check the status of deployment, run:

``` shell
kubectl get pods -o wide

```
The output will look similar to

``` shell
NAME                                               READY   STATUS              RESTARTS   AGE     IP            NODE     NOMINATED NODE   READINESS GATES
flask-test-app-7b4c8648c6-r8zvv                    0/1     ContainerCreating   0          22s     <none>        node-2   <none>           <none>
nfs-subdir-external-provisioner-7567fc7fcf-6qkcj   1/1     Running             0          3d21h   192.168.5.4   node-2   <none>           <none>
```

Here the status of the pod is ContainerCreating, which means the container is getting ready. When it reaches the Running state, then it means the pod is healthy and is running.

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
The port shows as 6000:32000/TCP which means the service is running inside the cluster on port 6000 and is bound to port 32000 on the nodes.

Get the URL of the service - run

``` shell
echo http://$(curl -s ipinfo.io/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there.

To test the load on the deployment we will use `siege, a command-line tool used to test and analyze the performance of web servers. It can generate a significant amount of traffic to test the response of a web server under load.

Install siege on node-0:

```shell
sudo apt-get update; sudo apt-get -y install siege

```
and then run 

``` shell
siege -c 10 -t 30s http://$(curl -s ipinfo.io/ip):32000/test
```

Here Siege will generate traffic to your website for 30 seconds with a concurrency level of 10 users.


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


