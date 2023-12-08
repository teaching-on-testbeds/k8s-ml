sudo apt update
sudo apt -y install virtualenv

# get Kubespray + materials for this assignment
git clone --branch release-2.22 https://github.com/kubernetes-sigs/kubespray.git
git clone https://github.com/teaching-on-testbeds/k8s-ml.git

mv kubespray/inventory/sample kubespray/inventory/mycluster
cp k8s-ml/config/k8s-cluster.yml kubespray/inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml
cp k8s-ml/config/inventory.py    kubespray/contrib/inventory_builder/inventory.py
cp k8s-ml/config/addons.yml      kubespray/inventory/mycluster/group_vars/k8s_cluster/addons.yml

# wait for other hosts to come up
until sudo ssh -o StrictHostKeyChecking=no node-1 true >/dev/null 2>&1; do echo "Waiting for node-1 to come up"; sleep 5; done
until sudo ssh -o StrictHostKeyChecking=no node-2 true >/dev/null 2>&1; do echo "Waiting for node-2 to come up"; sleep 5; done

# install keys at all other hosts
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -q -N ""
PUBKEY=$(cat /users/$USER/.ssh/id_rsa.pub)
echo $PUBKEY >> /users/$USER/.ssh/authorized_keys
sudo ssh -o StrictHostKeyChecking=no node-1 "echo $PUBKEY >> /users/$USER/.ssh/authorized_keys"
sudo ssh -o StrictHostKeyChecking=no node-2 "echo $PUBKEY >> /users/$USER/.ssh/authorized_keys"

virtualenv -p python3 myenv
source myenv/bin/activate
cd kubespray
pip3 install -r requirements.txt

declare -a IPS=(192.168.1.10 192.168.1.11 192.168.1.12)
CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}

ansible-playbook -i inventory/mycluster/hosts.yaml  --become --become-user=root cluster.yml

# allow kubectl access for non-root user
for login_user in $(ls /users)
do 
    sudo cp -R /root/.kube /users/$login_user/.kube
    sudo chown -R $login_user /users/$login_user/.kube
done

# Add the user to the docker group on all hosts
sudo groupadd -f docker
ssh -o StrictHostKeyChecking=no node-1 "sudo groupadd -f docker"
ssh -o StrictHostKeyChecking=no node-2 "sudo groupadd -f docker"
for login_user in $(ls /users)
do 
    sudo usermod -aG docker $login_user
    ssh -o StrictHostKeyChecking=no node-1 "sudo groupadd -f docker; sudo usermod -aG docker $login_user"
    ssh -o StrictHostKeyChecking=no node-2 "sudo groupadd -f docker; sudo usermod -aG docker $login_user"

done


# Set up private distribution registry
# needs to be in new session
ssh -o StrictHostKeyChecking=no node-0 "docker run -d -p 5000:5000 --restart always --name registry registry:2"

sudo wget https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/config/daemon.json -O /etc/docker/daemon.json; sudo service docker restart
ssh -o StrictHostKeyChecking=no node-1 "sudo wget https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/config/daemon.json -O /etc/docker/daemon.json; sudo service docker restart"
ssh -o StrictHostKeyChecking=no node-2 "sudo wget https://raw.githubusercontent.com/teaching-on-testbeds/k8s-ml/main/config/daemon.json -O /etc/docker/daemon.json; sudo service docker restart"

