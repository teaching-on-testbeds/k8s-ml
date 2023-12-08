"""Bring up three VMs and set up a Kubernetes cluster.

Instructions:
Wait for the profile instance to start, and then wait for the startup scripts 
to finish running (resources turn green, with a check mark in the corner).
This may take about 30 minutes.

Then, open a shell and log in to the controller.
To verify the Kubernetes and Docker install, run

```
kubectl get nodes
```

and

```
docker run hello-world
```

See https://github.com/teaching-on-testbeds/k8s-ml/blob/main/README.md
for further instructions.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

# Create a Request object to start building the RSpec.
request = portal.context.makeRequestRSpec()
 
node_0 = request.XenVM("node-0")
node_0.cores = 4
node_0.ram = 8192
node_0.exclusive = True
node_0.routable_control_ip = True
node_0.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
iface0 = node_0.addInterface('interface-0', rspec.IPv4Address('192.168.1.10','255.255.255.0'))
node_0.addService(rspec.Execute('/bin/sh','bash /local/repository/reserve_cloudlab/setup.sh'))

node_1 = request.XenVM("node-1")
node_1.cores = 4
node_1.ram = 8192
node_1.exclusive = True
node_1.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
iface1 = node_1.addInterface('interface-1', rspec.IPv4Address('192.168.1.11','255.255.255.0'))

node_2 = request.XenVM("node-2")
node_2.cores = 4
node_2.ram = 8192
node_2.exclusive = True
node_2.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
iface2 = node_2.addInterface('interface-2', rspec.IPv4Address('192.168.1.12','255.255.255.0'))

link_0 = request.Link('net0')
link_0.addInterface(iface1)
link_0.addInterface(iface0)
link_0.addInterface(iface2)

# Print the RSpec to the enclosing page.
portal.context.printRequestRSpec()
