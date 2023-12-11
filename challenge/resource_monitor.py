from kubernetes import client, config, utils
import time, csv, argparse

parser = argparse.ArgumentParser(description='Monitor Kubernetes resource usage for ml-app')

parser.add_argument('-d', '--duration', required=True, type=float) 
parser.add_argument('-o', '--outputfile', required=True)   

args = parser.parse_args()

# connect to Kubernetes APIs
config.load_kube_config()
core_api = client.CoreV1Api()
cust_api = client.CustomObjectsApi()

init_time = time.time()

with open(args.outputfile, 'w') as resource_csv:
    writer = csv.writer(resource_csv)
    writer.writerow(["time","n_replica","cpu_req_core","mem_req_KB","cpu_lim_core","mem_lim_KB","cpu_use_core","mem_use_KB"])


while time.time() - init_time < args.duration:

    current_time = round(time.time() - init_time, 2)

    # get resource requests and limits for deployed pods
    ret = core_api.list_pod_for_all_namespaces(watch=False)
    cont_req = [r.spec.containers[0].resources.requests for r in ret.items if r.spec.containers[0].name=='ml-app']
    cpu_req_core = sum( [utils.parse_quantity(c['cpu']) for c in cont_req if c and 'cpu' in c] )
    mem_req_KB = sum( [utils.parse_quantity(c['memory'])/1024 for c in cont_req if c and 'memory' in c] )

    cont_lim = [r.spec.containers[0].resources.limits for r in ret.items if r.spec.containers[0].name=='ml-app']
    cpu_lim_core = sum( [utils.parse_quantity(c['cpu']) for c in cont_lim if c and 'cpu' in c] )
    mem_lim_KB = sum( [utils.parse_quantity(c['memory'])/1024 for c in cont_lim if c and 'memory' in c] )

    n_replica = len(cont_lim)

    # get actual usage
    resource = cust_api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace="default", plural="pods")
    cpu_use_core =  sum( [utils.parse_quantity( r['containers'][0]['usage']['cpu'] ) for r in resource["items"]] )
    mem_use_KB =  sum( [utils.parse_quantity( r['containers'][0]['usage']['memory'] )/1024 for r in resource["items"]] )

    resource_stats = [current_time, n_replica, cpu_req_core, mem_req_KB, cpu_lim_core, mem_lim_KB,cpu_use_core,mem_use_KB]

    with open(args.outputfile, 'a') as resource_csv:
        writer = csv.writer(resource_csv)
        writer.writerow(resource_stats)

    time.sleep(5)
