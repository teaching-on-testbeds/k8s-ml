## Optimize your deployment: an open-ended challenge

Your task now is to optimize your model and your deployment to:

* maximize accuracy
* minimize resource usage
* minimize response time

by modifying the trained model and the Kubernetes configuration. You may find it challenging to find a good balance on all three criteria at the same time!

For any proposed combination of model + deployment strategy, you will want to evaluate its performance according to all three critera. This section describes how!

### Measuring accuracy

In a "real" deployment, you would certainly want to measure your model's accuracy on the "live" data from the system, not the offline data that you are using for initial model development.

How might you do this, given that "ground truth" labels are not available for live data when the system is deployed? One possible approach would be to use a "held out" set - for a subset of actual user photo uploads, ask users to specify the category instead of assigning one automatically using your model. Use this "held out" set to evaluate your model, by comparing your model output to the user-assigned label.

At this phase in product development, though, you don't have any users or "live" data. You are still evaluating accuracy on the "Food-11" dataset, using the "Train a food classification" notebook.

### Measuring resource usage

To monitor resource usage over time, a Python script is provided for you. 

First, on "node-0", run

```
python -m pip3 install kubernetes
```

to install the Python Kubernetes client. 

Then, get the Python script for monitoring with

```
wget -O ~/resource_monitor.py https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/challenge/resource_monitor.py
```

Once you have downloaded the Python script, you can monitor resource usage at any time with e.g.

```
python3 ~/resource_monitor.py  -d 30 -o ~/resource_usage.csv
```

where 

* the `-d` argument is used to specify monitoring duration, in seconds
* the `-o` argument is used to specify the output file to save results to

A row of data will be written to the file you specified - in this case, `~/resource_usage.csv` - every 5 seconds, with the following statistics:

* time since beginning of monitoring
* number of `ml-app` containers currently deployed
* total number of CPU cores [requested](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-requests-are-scheduled) by all the `ml-app` containers
* total memory in KB [requested](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#how-pods-with-resource-requests-are-scheduled) by all the `ml-app` containers
* total [limit](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) on CPU cores of all the `ml-app` containers
* total [limit](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) on memory in KB of all the `ml-app` containers
* total number of CPU cores actually used by all the `ml-app` containers
* total memory in KB actually used by all the `ml-app` containers

To minimize resource usage, you will want to:

* scale the number of replicas (number of deployed containers) according to demand on the system - have a small number of replicas when load is low, but when response time gets slow because of load you will want to scale up the number of replicas.
* avoid requesting too much memory or CPU per container, since this will prevent Kubernetes from deploying more replicas. Your memory or CPU request should be matched to what your application actually needs, in order to be able to deploy more replicas when load on the system is high. The "needs" of your application will, in turn, depend on the size of the model you have deployed.
* keep limits on memory or CPU per container fairly close to the request, since otherwise some containers may not actually get what they requested.

You can use any data analysis tool for CSV files (e.g. Python with `pandas`) on the output file, for example to compute the average of these operational metrics over the duration of the monitoring interval.

### Measuring response time


To evaluate response time, we will use a `bash` script that runs sequence of `siege` tests, each lasting one minute, with varying load conditions.

Get the script on "node-0" by running:

```
wget -O ~/load_test.sh https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/challenge/load_test.sh
```

When you run this script with 

```
bash ~/load_test.sh
```

it will generate a file `~/load_output.csv`, which you can similarly analyze with the data analysis tool of your choice.


### Preliminaries

You should have already 

* trained a model, and downloaded the saved `model.keras` file
* designed a deployment strategy with horizontal scaling, i.e. 
  * created a copy of `deployment_hpa.yaml`: `cp ~/k8s-ml/deploy_hpa/deployment_hpa.yaml ~/deployment.yaml`
  * modified this file: use `nano deployment.yaml` and make your changes, then Ctrl+O and Enter to save the file and Ctrl+X to exit.

When you are ready to evaluate a model and a deployment (i.e. you have a `model.keras` and a `deployment.yaml`), you will follow these steps:

**Transfer the model to your system**: Use `scp` to transfer the saved model from your local device to the "node-0" host. The syntax for `scp` is:

```
scp -i PATH-TO-KEY LOCAL-FILE-PATH USERNAME@REMOTE-IP:REMOTE-FILE-PATH
```

where the `REMOTE-FILE-PATH` is `~/k8s-ml/app/model.keras` , and you run this command in your local terminal. For example,

* if the key I use to connect to the remote host is at `~/.ssh/id_rsa` on my local system
* the saved model `model.keras` is located at `~/Desktop` on my local system, i.e. the `LOCAL-FILE-PATH` is `~/Desktop/model.keras`
* my username on "node-0" is `ffund00` (you can get this by running `echo $USER` on "node-0"!)
* the IP address of my "node-0" host is `128.110.223.18` (you can get this by running `echo $(curl -s ifconfig.me/ip)` on "node-0"!)

then I would run in my local terminal:

```
scp -i ~/.ssh/id_rsa ~/Desktop/model.keras ffund00@128.110.223.18:~/k8s-ml/app/model.keras
```

**Build the container with your model**: Once the file transfer is 100% complete, you will re-build the container with the new model. On "node-0":

```
docker build --no-cache -t ml-app:0.0.1 ~/k8s-ml/app
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

The first time you deploy tbe `ml-app` container on any node in your cluster, it will take extra time to create the container. To avoid "counting" this extra time in our evaluation, you should first deploy the load balanced deployment, e.g. 

```
kubectl apply -f ~/k8s-ml/deploy_lb/deployment_lb.yaml
```

Wait a few minutes until all five pods are "ready":

```
kubectl get pods -o wide
```

Get the URL of the service - run

```
echo http://$(curl -s ifconfig.me/ip):32000
```

copy and paste this URL into your browser's address bar, and verify that your app is up and running there. 

Then delete the deployment:

```
kubectl delete -f ~/k8s-ml/deploy_lb/deployment_lb.yaml
```

Wait a few minutes until there are no more pods:

```
kubectl get pods -o wide
```

Now, you are ready to test your own deployment strategy!

### Run an evaluation

You will need two SSH terminals on "node-0".

In one SSH terminal, apply your `deployment.yaml`:

```
kubectl apply -f ~/deployment.yaml
```

You can wait a few minutes for the intiial pod(s) to be ready:

```
kubectl get pods -o wide
```

Then, in one terminal, run:

```
bash ~/load_test.sh
```

and immediately afterwards, in the second terminal, run:


```
python3 ~/resource_monitor.py  -d 1800 -o ~/resource_usage.csv
```

The test will run for 30 minutes.  When it is finished, you can stop the deployment with

```
kubectl delete -f ~/deployment.yaml
```

After it ends, you can analyze the data in the `resource_usage.csv` and `load_output.csv` files. To get overall statistics for the test:

* **Memory requested**: compute the mean of the `mem_req_KB` column in `resource_usage.csv`.
* **Memory used**: compute the mean of the `mem_use_KB` column in `resource_usage.csv`.
* **Transaction rate**: compute the sum of the `OKAY` column in `load_output.csv`, and divide by `60*60`. This is the number of successful transactions per second.
* **Response time**: in `load_output.csv`, sum the product of the `OKAY` column and the `Resp Time,` column, then divide by the sum of the `OKAY` column. This is the response time in seconds, averaged across all of the transactions in the test. (Do *not* just use the average of the `Resp Time.` column.)

Make sure to save all of the test artifacts - the results `resource_usage.csv` and `load_output.csv`, along with the actual saved model, `model.keras` and the deployment strategy `deployment.yaml` - in a safe place *off* of "node-0" since:

* when you release the resource or it expires, you will no longer have access to files on it.
* and on the next test of a new model and deployment strategy, you will overwrite these files anyway!