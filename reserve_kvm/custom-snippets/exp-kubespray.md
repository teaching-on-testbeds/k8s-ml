
::: {.cell .markdown}

### Use Kubespray to prepare a Kubernetes cluster

:::


::: {.cell .markdown}

Now that are resources are "up", we will use Kubespray, a software utility for preparing and configuring a Kubernetes cluster, to set them up as a cluster.

:::


::: {.cell .code}
```python
# install Python libraries required for Kubespray
remote = chi.ssh.Remote(server_ips[0])
remote.run("virtualenv -p python3 myenv")
remote.run("git clone --branch release-2.22 https://github.com/kubernetes-sigs/kubespray.git")
remote.run("source myenv/bin/activate; cd kubespray; pip3 install -r requirements.txt")
```
:::

::: {.cell .code}
```python
# copy config files to correct locations
remote.run("mv kubespray/inventory/sample kubespray/inventory/mycluster")
remote.run("git clone https://github.com/teaching-on-testbeds/k8s-ml.git")
remote.run("cp k8s-ml/config/k8s-cluster.yml kubespray/inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml")
remote.run("cp k8s-ml/config/inventory.py    kubespray/contrib/inventory_builder/inventory.py")
remote.run("cp k8s-ml/config/addons.yml      kubespray/inventory/mycluster/group_vars/k8s_cluster/addons.yml")
```
:::

::: {.cell .code}
```python
# build inventory for this specific topology
physical_ips = [n['addr'] for n in net_conf[0]['nodes']]
physical_ips_str = " ".join(physical_ips)
remote.run(f"source myenv/bin/activate; declare -a IPS=({physical_ips_str});"+"cd kubespray; CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}")

```
:::


::: {.cell .code}
```python
# make sure "controller" node can SSH into the others
remote.run('ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -q -N ""')
public_key = remote.run('cat ~/.ssh/id_rsa.pub').tail("stdout")[2:]

for physical_ip in physical_ips:
    remote_worker = chi.ssh.Remote(physical_ip, gateway=remote)
    remote_worker.run(f'echo {public_key} >> ~/.ssh/authorized_keys') 
```
:::


::: {.cell .code}
```python
# build the cluster
remote.run("source myenv/bin/activate; cd kubespray; ansible-playbook -i inventory/mycluster/hosts.yaml  --become --become-user=root cluster.yml")
```
:::

::: {.cell .code}
```python
# allow kubectl access for non-root user
remote.run("sudo cp -R /root/.kube /home/cc/.kube; sudo chown -R cc /home/cc/.kube; sudo chgrp -R cc /home/cc/.kube")
```
:::

::: {.cell .code}
```python
# check installation
remote.run("kubectl get nodes")
```
:::


::: {.cell .markdown}

### Set up Docker

Now that we have a Kubernetes cluster, we have a framework in place for container orchestration. But we still need to set up Docker, for building, sharing, and running those containers.

:::

::: {.cell .code}
```python
# add the user to the "docker" group on all hosts
for physical_ip in physical_ips:
    remote_worker = chi.ssh.Remote(physical_ip, gateway=remote)
    remote_worker.run("sudo groupadd -f docker; sudo usermod -aG docker $USER")
```
:::


::: {.cell .code}
```python
# set up a private distribution registry on the "controller" node for distributing containers
# note: need a brand-new SSH session in order to "get" new group membership
remote = chi.ssh.Remote(server_ips[0])
remote.run("docker run -d -p 5000:5000 --restart always --name registry registry:2")
```
:::

::: {.cell .code}
```python
# set up docker configuration on all the hosts
for physical_ip in physical_ips:
    remote_worker = chi.ssh.Remote(physical_ip, gateway=remote)
    remote_worker.run("sudo wget https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/config/daemon.json -O /etc/docker/daemon.json")
    remote_worker.run("sudo service docker restart")

```
:::


::: {.cell .code}
```python
# check configuration
remote.run("docker run hello-world")
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
print("ssh cc@" + server_ips[0])
```
:::



::: {.cell .markdown}

Now, you can open an SSH session as follows:

* In Jupyter, from the menu bar, use File > New > Terminal to open a new terminal.
* Copy the SSH command from the output above, and paste it into the terminal.

Alternatively, you can use your local terminal to log on to each node, if you prefer. (On your local terminal, you may need to also specify your key path as part of the SSH command, using the `-i` argument followed by the path to your private key.)

:::
     

::: {.cell .markdown}

You can also use `scp` to transfer a file to the remote host from your local terminal. Later in this exercise, you will want to transfer a file named `model.keras` to the directory `~/k8s-ml/app/` on this remote host. If your private key is in `~/.ssh/id_rsa_chameleon`, you would:

* open a *local* terminal on your own device in the same directory where your `model.keras` is located
* run the cell below
* copy and paste the output into your terminal to transfer the file.


:::
     
::: {.cell .code}
```python
print("scp -i ~/.ssh/id_rsa_chameleon model.keras cc@" + server_ips[0] + ":~/k8s-ml/app/")
```
:::
