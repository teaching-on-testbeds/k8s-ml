## Exercise: Deploy a service with dynamic scaling

In last exercise we used Load balancing to distribute incoming traffic across multiple instances of a particular application running on 5 different pods. The benefit was that in case we have heavy traffic the traffic can be distributed evenly and our service won't be affect. But what if there is a time when the traffic goes down and it can be easily handeled with one pod. in that case the other pods won't be used and the existing resources are not getting used efficiently. To fix this issue we use Horizontal scalling.

**Horizontal Scalling** is a process of adding number of instances of an application or service to handle increasing level of traffic or workload.

Here in our exercise we will be using a widely used horizontal scalling mechanism called *Horizontal Pod Autoscalling(HPA)* provided by kubernetes. The reason why we are using HPA is because HPA scales up or down the number of pods to ensure that the application has enough resources to handle the traffic. 

The flow chart below demonstrates the working of HPA.

![Horizontal Pod Autoscaller](/images/HPA.png)

source: https://granulate.io/blog/kubernetes-autoscaling-the-hpa/


To deploy an ML-App with Horizontal pod Auto scaller, We need to add a new resource in our manifest file of kind *HorizontalPodAutoscaler* and make some changes in resource section of deployment and set the limits and requests for cpu usage. Manifest file is already made for this exercise, so you don't need to worry much about that. Manifest file is inside the folder deploy_hpa named as deployment_hpa.yaml :

```shell
cd ~/k8s-ml/deploy_hpa

```

Let's understand this manifest file:

Run this command to see the manifest file

``` shell
cat deployment_hpa.yaml

```

The content will look similar to this :

```shell
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: ml-app-hpa
spec:
  maxReplicas: 5
  minReplicas: 1
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-app-hpa
  targetCPUUtilizationPercentage: 40
---
apiVersion: v1
kind: Service
metadata:
  name: flask-test-service
spec:
  selector:
    app: ml-app-hpa
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
  name: ml-app-hpa
spec:
  selector:
    matchLabels:
      app: ml-app-hpa
  replicas: 1
  template:
    metadata:
      labels:
        app: ml-app-hpa
    spec:
      containers:
      - name: ml-app-hpa
        image: node1:5000/ml-app:0.0.1
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
        resources:
          limits:
            cpu: "8"
            memory: "8Gi"
          requests:
            cpu: "5"
            memory: "5Gi"

```

Here you can see that there are three kind of resources :

- HorizontalPodAutoscaler :- This creates the horizontal pod autoscaler which starts scalling up the number of pods when the cpu usage goes above 40%.

- Service :- This creates a service which is used to redirect tcp requests in between pods and nodes which also has a load balancer.

- Deployment :- This creates a deployment of our flask app on a single pod with minimum resource requests of cpu:"5", memory:"5Gi" and maximum extension of resources to cpu:"8", memory:"8Gi".

Now we will use this manifest file to deploy our app.

On your terminal run:

``` shell
kubectl apply -f deployment_hs.yaml

```

Now our ml-app is deployed with horizontal scalling.

To check the health of pods run 

```shell
kubectl get pods

```

if the status shows as running, the pods are healthy.

Initially you will see that there is only one pod running, but with time when the traffic increases the pods will scale up and when the traffic goes down the pods will scale down.


and then to stress test run the below mentioned command: 

``` shell
$(echo siege -c 10 -t 30s http://$(curl -s ipinfo.io/ip):32000/test)

```

Once you complete this exercise make sure to delete the deployment and services running. 


To delete the deployment, run the following command:

```shell

kubectl delete -f deployment_hpa.yaml

```

This exercise is done here.


