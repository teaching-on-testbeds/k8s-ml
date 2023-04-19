
## Exercise : Reserve resources on CloudLab

To run an experiment on cloud-lab you need to follow the following steps: 
- Reserve Nodes as per your working schedule.

- Select a profile which is relevent to your experiment.

- Instantiate the profile and wait for the resources to come up.

- Log in to the resources and run your experiment.

### Reserve nodes

Before you start  the experiment, make sure you plan that when exactly you are going to do the experiment. For this experiment we have to reserve servers which are very scarce on CloudLab, so plan everything accordingly, use the resources and when you are done release them so that it can be available for others to use.

To reserve resources, click on **Experiments** at the top left corner of the CloudLab home page https://www.cloudlab.us/. From the dropdown select **Reserve Nodes** and then select all the options as given in the picture below:

![Reserve Nodes](../images/cloudlab-reservation.png)

Make sure to enter dates as per your requirements, Next click on check which will check if resources are available and a dialogue box will appear, select yes and then click on submit. your reservation will be done.

### Open and Instantiate profile

For this experiment we will be using the following profile : https://www.cloudlab.us/instantiate.php?profile=79d0f735-a099-11ea-b1eb-e4434b2381fc 

Once you click on the link it will take to the landing page which would look similar to this and contains a brief description of the profile :

![K8s Profile](../images/cloudlab-start-1.png)

Click on Next and you will see a page similar to the image below. Here you have to select parameters for our experiment. You don't need to make any changes here since everything selected by default is enough for the present experiment. make sure that the parameters are same as shown in the image.

![Parameterize](../images/cloudlab-start-2.png)

 click on Next and this will take to a Finalize section where we have to select the cluster. For our experiment use of any of the cluster is fine. Make sure to select the cluster which has resources available to use. To check the resources click on "Check Resource Availability".


![Finalize](../images/cloudlab-start-3.png)

Click on Next in Finalize section and it will take to the Schedule section. Here select the number of hours you are going to use the profile. for our experiment 16 hours is enough and if needed extra it can be extened.

![Schedule](../images/cloudlab-start-4.png)

Click Finish and the profile will start to intantiate, the process will take close to 30 mins and once done you will get a mail saying "Kubernetes Instance Setup Complete". This means that the resources are ready to use and you can login.  

Once the Process is complete the final page will look similar to this.

This is the Topology view where all three nodes have a tick on them as shown.

![Profile ready](../images/topology_view.png)

Here we have the list view which also have the SSH login commands.

![Profile ready](../images/list_view.png)

