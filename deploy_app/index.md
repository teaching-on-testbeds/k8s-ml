## Exercise: Deploy an image classification app as a web service

SSH into node-0 of your cluster. In this terminal, clone this repository, which contains all the material needed in the further exercises.

``` shell
git clone https://github.com/teaching-on-testbeds/k8s-ml.git
```

Then, transfer the model that you trained in the previous exercise to this node - run this command

``` shell
echo scp model.h5 $USER@$(curl -s ipinfo.io/ip):~/k8s-ml/app
```

to get an SCP command, then run the SCP command in your *local* terminal (not in the SSH session), from the directory where your model is saved. (If your SSH key is in a non-default location, you will need to add an argument to specify the key location.)

The output should look like this:

``` shell
model.h5                                                                                                                  100%  155MB   8.9MB/s   00:17
```
indicating that your model is transfered from your local to remote.

Once the file is transfered, return to the SSH session at node-0.

Now we are ready to deploy our model as a service. Rather than deploying it directly, we will use Docker to package our model, source code, and dependencies in a *container*. This will make it much easier to deploy multiple copies of the application (to handle heavier load) in future exercises.

Next, navigate to the directory that contains our application, which is implemented using Flask:

``` shell
cd k8s-ml/app
```

The directory structure is as shown below:

-   app
    -   instance
    -   static
    -   templates
    -   app.py
    -   Dockerfile
    -   requirements.txt
    -   model.h5

This directory includes a Dockerfile, which describes how to containerize the application. We will build the container (naming it `ml-app`) and then push it to a local "registry" of containers (which is running on port 5000 of node-0).

``` shell
docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```

Now that we have containerized our application, we can run it! Let's run it now, and will indicate that we want incoming requests on port 32000 to be passed to port 5000 on the container (where our Flask application is listening):

``` shell
docker run -d -p 32000:5000 node-0:5000/ml-app:0.0.1
```

-   `-d` is for detach mode.
-   `-p` is to assign the port host_port:container_port.

Now we can visit our web service and try it out! Run this command:

``` shell
echo http://$(curl -s ipinfo.io/ip):32000
```

to get the URL on which it is running, then open your browser and paste this URL into the address bar.

You can upload images to your image classification service and check its predictions.

When you are finished, you can stop the container by running:


``` shell
docker stop $(docker ps -q -f ancestor=ml-app:0.0.1)

```

---

In this exercise or in a future exercise, you may want to change the model underlying your service. If you do, you will need to repeat the SCP command to transfer the saved model. Then, you will have to rebuild the container, following the same steps as you did above while building the container for the first time.

``` shell

docker build --no-cache -t ml-app:0.0.1 .
docker tag ml-app:0.0.1  node-0:5000/ml-app:0.0.1
docker push node-0:5000/ml-app:0.0.1
```
