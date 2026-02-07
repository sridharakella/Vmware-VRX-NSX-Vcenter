# Kubernetes Autoscaling Demo – Horizontal Pod Autoscaler (HPA)

This repo contains all YAML manifests and commands used in the **Kubernetes Autoscaling Deep Dive (HPA Demo)** video on YouTube.

##  Prerequisites
- Kubernetes cluster (minikube, kind, or cloud-managed)
- Metrics Server installed - https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
- `kubectl` configured

## Commands Used

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml (installing metric server)
kubectl apply -f hpa-deploy.yaml
kubectl autoscale deployment hpa-demo --cpu-percent=50 --min=1 --max=5
kubectl run -it --rm load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://hpa-demo; done"
kubectl get hpa -w
```
