## Exercise : Set up your experiment at KVM@TACC on Chameleon

Before you run an experiment at KVM@TACC on Chameleon, you will:

- launch an experiment with VM and network resources.
- wait for your resources to be configured. 
- log in to resources to carry out the experiment. 

This exercise will guide you through those steps.

Note that each "project" on Chameleon has access to a limited quota of resources. Once a project reaches this quota, others in the project will not be able to launch an experiment until you have "released" some resources.

For this reason, you may not "hold on" to resources for an extended period of time (days or weeks) - you will have resources only while you are actively working on them (hours) and then you will release them for others to use. If you have not finished your experiment, you will save all of your work on your own device so that you can continue at a later time with a "new" set of resources.

### Reserving resources

This experiment assumes you have already completed [Hello, Chameleon](https://teaching-on-testbeds.github.io/blog/hello-chameleon), so you have set up your Chameleon account, created and added keys to your account, and joined an active project on Chameleon.

From the [Chameleon website](https://chameleoncloud.org/), click on "Experiment \> Jupyter Interface" in the menu. You may be prompted to log in.

In the Jupyter environment, select File \> New \> Terminal and in this terminal, run


```
cd work
git clone https://github.com/teaching-on-testbeds/k8s-ml
```

Then, in the file browser on the left side, open the `k8s-ml` directory, then the `reserve_kvm` directory, and then double-click on the `reserve_chameleon.ipynb` notebook to open it.

If you are prompted about a choice of kernel, you can accept the Python3 kernel.

Near the beginning of the notebook, you are asked to specify your Chameleon project ID. Once you have done this, and saved the modified notebook, you can either - 

* execute the notebook, one cell at a time, in order
* or use Run \> Run All Cells from the menu to execute the entire notebook

It will take about 30-45 minutes to set up the entire experiment, so you can step away and come back after it is finished! (but, you should keep an eye out in case any cell fails and stops the process in the middle.) Then, scroll to the bottom of the notebook to get instructions for (1) logging in to the "controller" node in your cluster, and (2) transferring a saved model from your local device to the "controller" node in your cluster.

### Releasing resources

As mentioned above, you may not "hold on" to resources for an extended period of time (days or weeks) - you will have resources only while you are actively working on them (hours) and then you will release them for others to use.

When you are not actively working on resources anymore, you will:

* open the `delete_chameleon.ipynb` notebook in the Chameleon Jupyter environment
* fill in your project ID near the beginning of the notebook
* then run the notebook to release resources

In some cases, if there is an error when releasing resources using the notebook, you may need to manually release resource from the [KVM@TACC web interface](https://kvm.tacc.chameleoncloud.org/project/). Here are the instructions for manually releasing resources:

* First, click on Network \> Floating IPs. In any row that includes your username in the "Mapped Fixed IP Address" column, click "Disassociate", then "Release Floating IP". Wait until this is finished.
* Next, click on Compute \> Instances. Check the box next to any instance(s) that include your username. Then, click "Delete Instances". Wait until this is finished.
* Click on Network \> Routers. In any row that includes your username, click "Clear Gateway" then "Delete Router". Wait until this is finished.
* Click on Network \> Networks. Check the box next to any network(s) that include your username. Then, click "Delete Networks". Wait until this is finished.
