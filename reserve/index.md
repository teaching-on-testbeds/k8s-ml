::: {.cell .markdown}

## Exercise : Reserve resources on Cloud-Lab

To run an experiment on cloud-lab you need to follow the following steps: 

- Select a profile which is relevent to your experiment, here for our experiment we have to select k8s.

- Instantiate the profile and wait for the resources to come up.

- Log in to the resources and run your experiment.

### Open and Instantiate profile

For this experiment we will be using the following profile : https://www.cloudlab.us/instantiate.php?profile=79d0f735-a099-11ea-b1eb-e4434b2381fc 

Once you click on the link it will take to the landing page which would look similar to this and contains a brief description of the profile :

![K8s Profile](images/profile.png)

Click on Next and you will see a page similar to the image below. Here you have to select parameters for our experiment. You don't need to make any changes here since everything selected by default is enough for the present experiment. make sure that the parameters are same as shown in the image.

![Parameterize](images/parameters.png)

 click on Next and this will take to a Finalize section where we have to select the cluster. For our experiment use of any of the cluster is fine. Make sure to select the cluster which has resources available to use. To check the resources click on "Check Resource Availability".


![Finalize](images/finalize.png)

Click on Next in Finalize section and it will take to the Schedule section. Here select the number of hours you are going to use the profile. for our experiment 16 hours is enough and if needed extra it can be extened.

![Schedule](images/schedule.png)

Click Finish and the profile will start to intantiate, the process will take close to 30 mins and once done you will get a mail saying "Kubernetes Instance Setup Complete". This means that the resources are ready to use and you can login.  

Once the Process is complete the final page will look similar to this, where all three nodes have a tick on them as shown in the image below.

![Profile ready](images/profile_ready.png)


Since Kubernetes is based on the concept of master and worker node and here in our experiment node-0 and node-1 are master nodes you can login to any of them and start next exercises.

This exercise is done here.


:::