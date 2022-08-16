import mlrun

# check if we are attached to k8s for running remote (container) jobs
no_k8s = False if mlrun.mlconf.namespace else True
print(no_k8s)
