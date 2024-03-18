
::: {.cell .markdown}
### Reserve resources

Now, we are ready to reserve resources!
:::

::: {.cell .markdown}
First, make sure you don't already have a slice with this name:
:::

::: {.cell .code}
```python
try:
    slice = fablib.get_slice(slice_name)
    print("You already have a slice by this name!")
    print("If you previously reserved resources, skip to the 'log in to resources' section.")
except:
    print("You don't have a slice named %s yet." % slice_name)
    print("Continue to the next step to make one.")
    slice = fablib.new_slice(name=slice_name)
```
:::


::: {.cell .markdown}
We will select a site for our experiment that has an IPv4 management network - otherwise, setting up the cluster is more complicated:
:::


::: {.cell .code}
```python
import random
site_name = random.choice(["UCSD", "FIU", "SRI"])
fablib.show_site(site_name)
```
:::

::: {.cell .markdown}
Then we will add hosts and network segments:
:::

::: {.cell .code}
```python
# this cell sets up the nodes
for n in node_conf:
    slice.add_node(name=n['name'], site=site_name, 
                   cores=n['cores'], 
                   ram=n['ram'], 
                   disk=n['disk'], 
                   image=n['image'])
```
:::

::: {.cell .code}
```python
# this cell sets up the network segments
for n in net_conf:
    ifaces = [slice.get_node(node["name"]).add_component(model="NIC_Basic", 
                                                 name=n["name"]).get_interfaces()[0] for node in n['nodes'] ]
    slice.add_l2network(name=n["name"], type='L2Bridge', interfaces=ifaces)
```
:::


::: {.cell .markdown}
The following cell submits our request to the FABRIC site. The output of this cell will update automatically as the status of our request changes. 

* While it is being prepared, the "State" of the slice will appear as "Configuring". 
* When it is ready, the "State" of the slice will change to "StableOK".

You may prefer to walk away and come back in a few minutes (for simple slices) or a few tens of minutes (for more complicated slices with many resources).

:::


::: {.cell .code}
```python
slice.submit()
```
:::


::: {.cell .code}
```python
slice.get_state()
slice.wait_ssh(progress=True)
```
:::
