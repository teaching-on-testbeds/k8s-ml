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

It will take about 30-45 minutes to set up the entire experiment, so you can step away and come back after it is finished! Then, scroll to the bottom of the notebook to get instructions for (1) logging in to the "controller" node in your cluster, and (2) transferring a saved model from your local device to the "controller" node in your cluster.