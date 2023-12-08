
::: {.cell .markdown}

### Use Kubespray to prepare a Kubernetes cluster

:::


::: {.cell .markdown}

Now that are resources are "up", we will use Kubespray, a software utility for preparing and configuring a Kubernetes cluster, to set them up as a cluster.

:::


::: {.cell .code}
```python
# install Python libraries required for Kubespray
remote = slice.get_node(name="node-0")
remote.execute("virtualenv -p python3 myenv")
remote.execute("git clone --branch release-2.22 https://github.com/kubernetes-sigs/kubespray.git")
_ = remote.execute("source myenv/bin/activate; cd kubespray; pip3 install -r requirements.txt")
```
:::

::: {.cell .code}
```python
# copy config files to correct locations
remote.execute("mv kubespray/inventory/sample kubespray/inventory/mycluster")
remote.execute("git clone https://github.com/teaching-on-testbeds/k8s-ml.git")
remote.execute("cp k8s-ml/config/k8s-cluster.yml kubespray/inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml")
remote.execute("cp k8s-ml/config/inventory.py    kubespray/contrib/inventory_builder/inventory.py")
remote.execute("cp k8s-ml/config/addons.yml      kubespray/inventory/mycluster/group_vars/k8s_cluster/addons.yml")
```
:::

::: {.cell .code}
```python
# build inventory for this specific topology
physical_ips = [n['addr'] for n in net_conf[0]['nodes']]
physical_ips_str = " ".join(physical_ips)
_ = remote.execute(f"source myenv/bin/activate; declare -a IPS=({physical_ips_str});"+"cd kubespray; CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}")

```
:::


::: {.cell .code}
```python
# make sure "controller" node can SSH into the others
remote.execute('ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -q -N ""')
public_key, stderr = remote.execute('cat ~/.ssh/id_rsa.pub', quiet=True)

for n in node_conf:
    node = slice.get_node(n['name'])
    print("Now copying key to node " + n['name'])
    node.execute(f'echo {public_key.strip()} >> ~/.ssh/authorized_keys')
```
:::


::: {.cell .code}
```python
# build the cluster
_ = remote.execute("source myenv/bin/activate; cd kubespray; ansible-playbook -i inventory/mycluster/hosts.yaml  --become --become-user=root cluster.yml")
```
:::

::: {.cell .code}
```python
# allow kubectl access for non-root user
remote.execute("sudo cp -R /root/.kube /home/ubuntu/.kube; sudo chown -R ubuntu /home/ubuntu/.kube; sudo chgrp -R ubuntu /home/ubuntu/.kube")
```
:::

::: {.cell .code}
```python
# check installation
_ = remote.execute("kubectl get nodes")
```
:::


::: {.cell .markdown}

### Set up Docker

Now that we have a Kubernetes cluster, we have a framework in place for container orchestration. But we still need to set up Docker, for building, sharing, and running those containers.

:::

::: {.cell .code}
```python
# add the user to the "docker" group on all hosts
for n in node_conf:
    node = slice.get_node(n['name'])
    node.execute("sudo groupadd -f docker; sudo usermod -aG docker $USER")
```
:::


::: {.cell .code}
```python
# set up a private distribution registry on the "controller" node for distributing containers
# note: need a brand-new SSH session in order to "get" new group membership
remote.execute("docker run -d -p 5000:5000 --restart always --name registry registry:2")
```
:::

::: {.cell .code}
```python
# set up docker configuration on all the hosts
for n in node_conf:
    node = slice.get_node(n['name'])
    node.execute("sudo wget https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/config/daemon.json -O /etc/docker/daemon.json")
    node.execute("sudo service docker restart")

```
:::


::: {.cell .code}
```python
# check configuration
remote.execute("docker run hello-world")
```
:::


::: {.cell .markdown}

### Get SSH login details

:::


::: {.cell .markdown}

At this point, we should be able to log in to our "controller" node over SSH! Run the following cell, and observe the output - you will see an SSH command this node.

:::


::: {.cell .code}
```python
print(remote.get_ssh_command())
```
:::



::: {.cell .markdown}

Now, you can open an SSH session as follows:

* In Jupyter, from the menu bar, use File > New > Terminal to open a new terminal.
* Copy the SSH command from the output above, and paste it into the terminal.

:::
     

::: {.cell .markdown}

You will also need to know how to transfer a file to the remote host from your local terminal. Later in this exercise, you will want to transfer a file named `model.keras` to the directory `~/k8s-ml/app/` on this remote host.

The easiest way is to use a free file upload service, then download the file on the remote host. For example:

* upload your `model.keras` file to https://www.file.io/
* copy the download link that is provided, and paste it in the following cell
* un-comment the second line in the cell
* run the cell

:::
     
::: {.cell .code}
```python
download_url = "https://file.io/XXXXXXXXXXXX" # replace this URL
# _ = remote.execute("wget " + download_url + " -O ~/k8s-ml/app/model.keras")
```
:::
