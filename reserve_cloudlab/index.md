## Exercise : Set up your experiment on CloudLab

Before you run an experiment on CloudLab, you will:

- launch an experiment with VM and network resources.
- wait for your resources to be configured. 
- log in to resources to carry out the experiment. 

This exercise will guide you through those steps.

Note that there are limited resources on CloudLab. If all resources are exhausted, others in the project will not be able to launch an experiment until you have "released" some resources.

For this reason, you may not "hold on" to resources for an extended period of time (days or weeks) - you will have resources only while you are actively working on them (hours) and then you will release them for others to use. If you have not finished your experiment, you will save all of your work on your own device so that you can continue at a later time with a "new" set of resources.

### Reserving resources

This experiment assumes you have already completed [Hello, CloudLab](https://teaching-on-testbeds.github.io/blog/hello-cloudlab), so you have set up your CloudLab account, created and added keys to your account, and joined an active project on CloudLab.

Log in to the [CloudLab website](https://cloudlab.us/). Then, open the following link:

[https://www.cloudlab.us/p/cl-education/k8s-ml](https://www.cloudlab.us/p/cl-education/k8s-ml)


Click Next, and on the following page, select your project and a CloudLab cluster. The status indicator next to each cluster tells you roughly how heavily utilized it is at the moment - green indicates that there are not many users, orange means heavy load, and red means that it is almost fully utilized. You are more likely to be successful if you choose a cluster with a green indicator.

Click Next. On the last page, you’ll be asked to set the duration of your experiment. At the end of this duration, your resources will be deleted automatically - so make sure to give yourself enough time to finish. But, to be fair to others, you should not "hold on" to resources excessively - only while you are *actively* working.

When you have made all your choices, click “Finish” to ask CloudLab to reserve resources according to your configuration.

Wait until all resources turn "green". 

Then, open a shell and use SSH to log in to the controller - "node-0".

Set up a Kubernetes cluster with

```
bash /local/repository/reserve_cloudlab/setup.sh
```

This may take about 30 minutes. When it is finished, close your SSH session, and open a *new* one.

To verify the Kubernetes and Docker install, run

```
kubectl get nodes
```

and

```
docker run hello-world
```


### Releasing resources

As mentioned above, you may not "hold on" to resources for an extended period of time (days or weeks) - you will have resources only while you are actively working on them (hours) and then you will release them for others to use.

If you finish working before your resources "expire", please click the "Terminate" button to free these resources for other experimenters.