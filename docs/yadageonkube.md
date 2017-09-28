## Let's create a new cluster

```
source ~/openstack/container.sh
magnum cluster-create --name kubeyadage --keypair-id openstack --cluster-template kubernetes --node-count 5
mkdir -p yadageonkube/magnum
cd yadageonkube/magnum
magnum cluster-config kubeyadage > setup.sh && source setup.sh
cd ..
```

## Let's create some Storage

```
manila create --share-type "Geneva CephFS Testing" --name kubeyadage cephfs 100
manila access-allow kubeyadage cephx kubeyadage-user
```

## Install yadage

```
scl enable rh-python34 zsh
virtualenv venv
source venv/bin/activate
pip install yadage packtivity-kube-plugin
```

## Configure the yadage backend for Kubernetes

```
cat << EOF > ceph-secret.yml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
   name: ceph-secret
data:
   key: '... your b64 encoded auth key ...'
EOF

kubectl create -f ceph-secret.yml --validate=false
```

```
echo 'kubeconfigloc: magnum/config' > backendopt.yml
export PACKTIVITY_STATEPROVIDER=packtivitykube.mounted_posix
export PACKTIVITY_ASYNCBACKEND_OPTS=backendopt.yml
export PACKTIVITY_ASYNCBACKEND=packtivitykube.kubebackend:KubeBackend:KubeProxy
```

```
cat << EOF > mount.yml
cephfs:
  monitors: [... list of monitors ...]
  user: '...your cephfs user...'
  secretRef:
    name: ceph-secret
  path: '/your/cephfs/path....'
EOF
```

## Run a Workflow

```
yadage-run -b fromenv \
  fromenv:workdir100 \
  databkgmc.yml \
  -t github:lukasheinrich/fullpreservation_example_one:workflow \
  -d mountspec=mount.yml \
  --metadir here
```

or 

```
yadage-run  fromenv:workdir101 \
   madgraph_rivet.yml \
   -t from-github/phenochain \
   -p nevents=100 -p rivet_analysis=MC_GENERIC \
  -d mountspec=mount.yml \
  --metadir here2   
```
