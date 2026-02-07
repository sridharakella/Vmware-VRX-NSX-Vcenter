# Kubernetes Autoscaling Demo – Vertical Pod Autoscaler (VPA)

This repo contains all YAML manifests and commands used in the **Kubernetes Autoscaling Deep Dive (HPA Demo)** video on YouTube.

## Commands Used

```
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler/hack
./vpa-up.sh (This script generates TLS certs, creates all necessary API objects, and deploys the components of VPA)
kubectl apply -f vpa-demo.yaml
kubectl apply -f vpa-policy.yaml
kubectl run loadgen --image=busybox -- /bin/sh -c "while true; do :; done"
watch -n 2 "kubectl get vpa vpa-demo -o yaml | grep -A5 recommendation"
```
