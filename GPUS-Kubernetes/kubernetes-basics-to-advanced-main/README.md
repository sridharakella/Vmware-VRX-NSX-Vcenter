# Kubernetes Basics to Advanced

This repo has all the manifests, notes, and demo files from my Kubernetes YouTube series “Kubernetes Basics to Advanced.”  
The idea is simple: everything I show in the videos should be reproducible on your own setup without guesswork.

I’m keeping the examples practical and minimal so you can copy, tweak, and break things as you learn.  

---

## What’s Inside

This repo is organised roughly in the same order as the playlist:

- Pods (with and without YAML)
- ReplicaSets, Deployments, and rollout demos
- Services (ClusterIP, NodePort, LoadBalancer)
- Namespaces
- Resource requests/limits
- Quotas and LimitRanges
- Labels and selectors
- Taints, tolerations, nodeSelectors, affinities
- Static Pods, DaemonSets, PriorityClass
- ConfigMaps & Secrets
- Probes (liveness, readiness, startup, exec)

Every topic gets its own folder, so you can jump directly to what you’re learning.

---

## How to Use This Repo

1. Clone it

```
git clone https://github.com/sridharakella/Vmware-VRX-NSX-Vcenter.git
```

2. Pick the topic you’re watching in the playlist.
3. Apply the manifest or run the commands from the notes.
4. Compare your output with mine in the video.
5. Break stuff, fix stuff, repeat.


---

## Requirements

- A local Kubernetes setup (kind, Minikube, or k3s/rke2)
- kubectl installed

---






---

## Contributions

Not looking for huge PRs right now, but if you spot an error or want to add a small improvement, feel free to open an issue.
