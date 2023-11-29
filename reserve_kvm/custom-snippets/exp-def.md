::: {.cell .markdown}
### Define configuration for this experiment (3 VMs)
:::

::: {.cell .markdown}

For this specific experiment, we will need three virtual machines connected to a common network. Each of the virtual machines will be of the `m1.large` type, with 4 VCPUs, 8 GB memory, 40 GB disk space.

:::

::: {.cell .code}
```python
username = os.getenv('USER')

node_conf = [
 {'name': "node-0",  'flavor': 'm1.large', 'image': 'CC-Ubuntu20.04', 'packages': ["virtualenv"], 'bastion': True}, 
 {'name': "node-1",  'flavor': 'm1.large', 'image': 'CC-Ubuntu20.04', 'packages': [], 'bastion': False}, 
 {'name': "node-2",  'flavor': 'm1.large', 'image': 'CC-Ubuntu20.04', 'packages': [], 'bastion': False} 
]
net_conf = [
 {"name": "net0", "subnet": "192.168.1.0/24", "nodes": [{"name": "node-0",   "addr": "192.168.1.10"}, {"name": "node-1", "addr": "192.168.1.11"}, {"name": "node-2", "addr": "192.168.1.12"}]},
]
route_conf = []
```
:::
