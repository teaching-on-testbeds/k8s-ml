::: {.cell .markdown}

## Exercise 3: Scaling a ML-app (Part-2)

In last exercise we used Load balancing to distribute incoming traffic across multiple instances of a particular application running on 5 different pods. The benefit was that in case we have heavy traffic the traffic can be distributed evenly and our service won't be affect. But what if there is a time when the traffic goes down and it can be easily handeled with one pod. in that case the other pods won't be used and the existing resources are not getting used efficiently. To fix this issue we use Horizontal scalling.

**Horizontal Scalling** is a process of adding number of instances of an application or service to handle increasing level of traffic or workload.

Here in our exercise we will be using a widely used horizontal scalling mechanism called *Horizontal Pod Autoscalling(HPA)* provided by kubernetes. The reason why we are using HPA is because HPA scales up or down the number of pods to ensure that the application has enough resources to handle the traffic. 

The flow chart below demonstrates the working of HPA.

![Horizontal Pod Autoscaller](images/HPA.png)

source: https://granulate.io/blog/kubernetes-autoscaling-the-hpa/


To deploy an ML-App with Horizontal pod Auto scaller, We need to add a new resource in our manifest file of kind *HorizontalPodAutoscaler* and make some changes in resource section of deployment and set the limits and requests for cpu usage. Manifest file is already made for this exercise, so you don't need to worry much about that.

Clone the repository that contains the Flask ML app and other files for Horizontal scalling:

``` shell
$ cd ~/
$ git clone https://github.com/teaching-on-testbeds/k8s-ml-hs.git
$ cd k8s-ml-h5

```

Get your ml model from your local to the same folder through scp.

Create a docker image for the ml-app by using the command.

``` shell
$ docker build -t --no-cache ml-app-hs:latest .

```

Tag the docker image to push it to the local registry

``` shell
$ docker tag ml-app-hs:latest  10.10.1.1:5000/ml-app-hs:latest

```

Push the image to the registry:

``` shell
$ docker push 10.10.1.1:5000/ml-app-hs:latest

```

Understanding the manifest file:

Run this command to see the manifest file 

``` shell
$ cat deployment_hs.yaml

```
Here you can see that there are three kind of resources :

- HorizontalPodAutoscaler :- This creates the horizontal pod autoscaler
- Service :- This creates a service which is used to redirect tcp requests on in between pods and nodes.
- Deployment :- This creates a deployment of our flask app on a single pod with cpu limits to track the uses of cpu.

Now we will use this manifest file to deploy our app.

On your terminal run:

``` shell
$ kubectl apply -f deployment_hs.yaml

```

Now our ml-app is deployed with horizontal scalling.

To check the healt of pods run 

```shell
$ kubectl get pods

```

if the status shows as running, the pods are healthy.

Initially you will see that there is only one pod running, but with time when the traffic increases the pods will scale up and when the traffic goes down the pods will scale down.

**Testing Horizontal Scalling**
TO - DO










:::