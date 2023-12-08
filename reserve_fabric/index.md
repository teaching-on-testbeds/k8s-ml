## Exercise : Set up your experiment at FANROC

Before you run an experiment at FABRIC, you will:

- launch an experiment with VM and network resources.
- wait for your resources to be configured. 
- log in to resources to carry out the experiment. 

This exercise will guide you through those steps.

### Reserving resources

This experiment assumes you have already completed [Hello, FABRIC](https://teaching-on-testbeds.github.io/blog/hello-fabric), so you have set up your FABRIC account, created and added keys to your account, and joined an active project on FABRIC.

From the [FABRIC website](https://portal.fabric-testbed.net/), click on "JupyterHub" in the menu. You may be prompted to log in.

In the Jupyter environment, select File \> New \> Terminal and in this terminal, run


```
git clone https://github.com/teaching-on-testbeds/k8s-ml
```

Then, in the file browser on the left side, open the `k8s-ml` directory, then the `reserve_fabric` directory, and then double-click on the `reserve_fabric.ipynb` notebook to open it.

If you are prompted about a choice of kernel, you can accept the Python3 kernel.

Then, you can either - 

* execute the notebook, one cell at a time, in order
* or use Run \> Run All Cells from the menu to execute the entire notebook

It will take about 30 minutes to set up the entire experiment, so you can step away and come back after it is finished! (but, you should keep an eye out in case any cell fails and stops the process in the middle.) Then, scroll to the bottom of the notebook to get instructions for (1) logging in to the "controller" node in your cluster, and (2) transferring a saved model from your local device to the "controller" node in your cluster.

### Releasing resources

When you have finished with your resources, you will:

* open the `delete_fabric.ipynb` notebook in the FABRIC Jupyter environment
* then run the notebook to release resources
