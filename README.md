## Deploying machine learning systems on Kubernetes

Congratulations! You've been offered an exciting and lucrative new position. You're going to be a machine learning engineer at a small startup company called GourmetGram. They are developing an online photo sharing community focused on food. 

On your first day at work, you are given the following brief:

> When someone uploads a photo of food to our site, it should be tagged and categorized automatically, right?
>
> Your predecessor had already implemented a machine learning model that classified photos into different categories: Bread, Dairy product, Dessert, Egg, Fried food, Meat, Noodles/Pasta, Rice, Seafood, Soup, and Vegetable/Fruit. And they built a simple web app around the upload and classification process.
>
> But, there were problems: one, the categorization was not very accurate. And second, it took too long. The classification happens in real time, when the photo is uploaded and before the user sees the next page (with the photo and info about it, including its assigned category), so it can't take too long.
>
> Of course, we can fix the timing issue to some extent by throwing more compute resources at the problem. But we are also concerned with cost, so we don't want to pay for compute resources that are sitting idle when load is low. 
>
>You can fix both of these problems, right? (That's why we hired you!)

You've been giving some material to ease the onboarding process - 

First, you should have already completed the [Hello, Chameleon](https://teaching-on-testbeds.github.io/blog/hello-chameleon) sequence to configure your account and learn how to use Chameleon.

Next, you should [train your model](https://colab.research.google.com/github/teaching-on-testbeds/k8s-ml/blob/master/train/fine_tune_food.ipynb).

After that, you've been given a sequence that shows you how to reserve a cloud "cluster" on Chameleon, and deploy a web app using your model on this cluster, using several deployment strategies:

* [Set up Kubernetes deployment](reserve_kvm/index.md)
* [Deploy model to a web service with Flask + Docker](deploy_app/index.md)
* [Deploy service using container orchestration (Kubernetes)](deploy_k8s/index.md)
* [Deploy a load balanced service](deploy_lb/index.md)
* [Deploy a service with dynamic scaling](deploy_hpa/index.md)

Finally, you'll need to develop your own solution, given the brief above. You'll train your own model and design your own deployment strategy.

* [Optimize your deployment](challenge/index.md)

---

This material is based upon work supported by the National Science Foundation under Grant No. 2230079. 
