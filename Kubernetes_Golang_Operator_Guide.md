# Kubernetes Golang Operator Development - Complete Guide

## Overview

A **Kubernetes Operator** is a method of packaging, deploying, and managing a Kubernetes application. Operators extend Kubernetes to automate the management of complex, stateful applications by encoding operational knowledge into software.

---

## **Options for Creating Golang Operators**

There are **4 main approaches** to building Kubernetes operators in Go:

| Approach | Best For | Complexity | Learning Curve |
|----------|----------|------------|----------------|
| **1. Operator SDK** | Production operators | Medium | Moderate |
| **2. Kubebuilder** | Clean, modern operators | Medium | Moderate |
| **3. controller-runtime** | Custom, low-level control | High | Steep |
| **4. client-go (from scratch)** | Full customization | Very High | Very Steep |

---

## **Option 1: Operator SDK (Recommended)**

### **What is Operator SDK?**

The Operator SDK is part of the **Operator Framework** (Red Hat/CNCF project) and provides tools to build, test, and package operators. It's built on top of Kubebuilder and adds additional features for operator lifecycle management.

### **Key Features**

✅ Built on Kubebuilder (includes all Kubebuilder features)  
✅ Operator Lifecycle Manager (OLM) integration  
✅ Scorecard for operator testing  
✅ Support for Helm and Ansible operators (not just Go)  
✅ Bundle generation for operator distribution  
✅ Automated CSV (ClusterServiceVersion) generation  

### **When to Use Operator SDK**

- Building production-grade operators
- Planning to distribute via OperatorHub.io
- Need OLM integration
- Want comprehensive tooling and scaffolding
- Enterprise/Red Hat environments

### **Installation**

```bash
# macOS
brew install operator-sdk

# Linux
export ARCH=$(case $(uname -m) in x86_64) echo -n amd64 ;; aarch64) echo -n arm64 ;; *) echo -n $(uname -m) ;; esac)
export OS=$(uname | awk '{print tolower($0)}')
export OPERATOR_SDK_DL_URL=https://github.com/operator-framework/operator-sdk/releases/download/v1.34.1
curl -LO ${OPERATOR_SDK_DL_URL}/operator-sdk_${OS}_${ARCH}
chmod +x operator-sdk_${OS}_${ARCH} && sudo mv operator-sdk_${OS}_${ARCH} /usr/local/bin/operator-sdk

# Verify
operator-sdk version
```

### **Quick Start - Create an Operator**

```bash
# 1. Create project directory
mkdir memcached-operator
cd memcached-operator

# 2. Initialize operator project
operator-sdk init --domain=example.com --repo=github.com/example/memcached-operator

# 3. Create API (CRD) and Controller
operator-sdk create api --group cache --version v1alpha1 --kind Memcached --resource --controller

# 4. Define your API (edit api/v1alpha1/memcached_types.go)
# Add fields to MemcachedSpec struct

# 5. Generate CRDs and manifests
make manifests

# 6. Implement controller logic (controllers/memcached_controller.go)
# Add reconciliation logic

# 7. Test locally
make install  # Install CRDs
make run     # Run operator locally

# 8. Build and deploy
make docker-build docker-push IMG=<your-registry>/memcached-operator:v0.0.1
make deploy IMG=<your-registry>/memcached-operator:v0.0.1
```

### **Project Structure**

```
memcached-operator/
├── api/
│   └── v1alpha1/
│       ├── memcached_types.go      # CRD definition
│       └── zz_generated.deepcopy.go
├── controllers/
│   ├── memcached_controller.go     # Controller logic
│   └── suite_test.go
├── config/
│   ├── crd/                        # CRD manifests
│   ├── manager/                    # Manager deployment
│   ├── rbac/                       # RBAC rules
│   ├── samples/                    # Example CRs
│   └── default/                    # Kustomization
├── main.go                         # Operator entry point
├── Dockerfile
├── Makefile
└── go.mod
```

### **Sample API Definition**

```go
// api/v1alpha1/memcached_types.go
type MemcachedSpec struct {
    // Size is the number of memcached instances
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    Size int32 `json:"size"`
    
    // Image is the container image to use
    Image string `json:"image,omitempty"`
    
    // Port is the port memcached listens on
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=65535
    Port int32 `json:"port,omitempty"`
}

type MemcachedStatus struct {
    // Nodes are the names of the memcached pods
    Nodes []string `json:"nodes"`
    
    // Conditions represent the latest available observations
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}
```

### **Sample Controller Logic**

```go
// controllers/memcached_controller.go
func (r *MemcachedReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)
    
    // Fetch the Memcached instance
    memcached := &cachev1alpha1.Memcached{}
    err := r.Get(ctx, req.NamespacedName, memcached)
    if err != nil {
        if errors.IsNotFound(err) {
            return ctrl.Result{}, nil
        }
        return ctrl.Result{}, err
    }
    
    // Check if deployment exists, if not create it
    found := &appsv1.Deployment{}
    err = r.Get(ctx, types.NamespacedName{Name: memcached.Name, Namespace: memcached.Namespace}, found)
    if err != nil && errors.IsNotFound(err) {
        // Create deployment
        dep := r.deploymentForMemcached(memcached)
        log.Info("Creating a new Deployment", "Deployment.Namespace", dep.Namespace, "Deployment.Name", dep.Name)
        err = r.Create(ctx, dep)
        if err != nil {
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    }
    
    // Ensure deployment size is same as spec
    size := memcached.Spec.Size
    if *found.Spec.Replicas != size {
        found.Spec.Replicas = &size
        err = r.Update(ctx, found)
        if err != nil {
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    }
    
    // Update status
    podList := &corev1.PodList{}
    listOpts := []client.ListOption{
        client.InNamespace(memcached.Namespace),
        client.MatchingLabels(labelsForMemcached(memcached.Name)),
    }
    if err = r.List(ctx, podList, listOpts...); err != nil {
        return ctrl.Result{}, err
    }
    podNames := getPodNames(podList.Items)
    if !reflect.DeepEqual(podNames, memcached.Status.Nodes) {
        memcached.Status.Nodes = podNames
        err := r.Status().Update(ctx, memcached)
        if err != nil {
            return ctrl.Result{}, err
        }
    }
    
    return ctrl.Result{}, nil
}
```

### **Pros & Cons**

**Pros:**
- ✅ Built on proven Kubebuilder foundation
- ✅ OLM integration for easy distribution
- ✅ Comprehensive tooling (scorecard, bundle generation)
- ✅ Active community and Red Hat backing
- ✅ Good for enterprise operators

**Cons:**
- ⚠️ More complex than pure Kubebuilder
- ⚠️ Some OLM-specific concepts to learn
- ⚠️ Heavier tooling footprint

---

## **Option 2: Kubebuilder (Modern & Clean)**

### **What is Kubebuilder?**

Kubebuilder is a framework for building Kubernetes APIs using **Custom Resource Definitions (CRDs)**. It's maintained by Kubernetes SIG API Machinery and provides a clean, opinionated way to build operators.

### **Key Features**

✅ Official Kubernetes project  
✅ Clean, minimal scaffolding  
✅ Modern Go best practices  
✅ Excellent documentation (book.kubebuilder.io)  
✅ Webhook support built-in  
✅ Testing framework included  
✅ Active development and maintenance  

### **When to Use Kubebuilder**

- Building modern, clean operators
- Want official Kubernetes project backing
- Prefer minimal tooling
- Don't need OLM integration immediately
- Building operators for your own use (not distribution)

### **Installation**

```bash
# macOS
brew install kubebuilder

# Linux
curl -L -o kubebuilder https://go.kubebuilder.io/dl/latest/linux/amd64
chmod +x kubebuilder && mv kubebuilder /usr/local/bin/

# Verify
kubebuilder version
```

### **Quick Start**

```bash
# 1. Initialize project
mkdir myapp-operator
cd myapp-operator
kubebuilder init --domain mycompany.com --repo github.com/mycompany/myapp-operator

# 2. Create API
kubebuilder create api --group apps --version v1 --kind MyApp

# 3. Edit types (api/v1/myapp_types.go)

# 4. Generate manifests
make manifests

# 5. Implement controller (controllers/myapp_controller.go)

# 6. Run locally
make install
make run

# 7. Deploy
make docker-build docker-push IMG=myregistry/myapp-operator:v1
make deploy IMG=myregistry/myapp-operator:v1
```

### **Key Differences from Operator SDK**

| Feature | Kubebuilder | Operator SDK |
|---------|-------------|--------------|
| **Base** | Standalone | Built on Kubebuilder |
| **OLM Support** | Manual | Built-in |
| **Bundle Generation** | Manual | Automated |
| **Scorecard** | No | Yes |
| **Helm/Ansible** | No | Yes |
| **Complexity** | Lower | Higher |

### **Sample Kubebuilder Markers**

```go
// Kubebuilder markers for code generation

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:resource:path=myapps,scope=Namespaced
// +kubebuilder:printcolumn:name="Age",type="date",JSONPath=".metadata.creationTimestamp"
// +kubebuilder:printcolumn:name="Status",type="string",JSONPath=".status.phase"
type MyApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`
    
    Spec   MyAppSpec   `json:"spec,omitempty"`
    Status MyAppStatus `json:"status,omitempty"`
}

// Field validation markers
type MyAppSpec struct {
    // +kubebuilder:validation:Required
    // +kubebuilder:validation:MinLength=1
    Name string `json:"name"`
    
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    Replicas int32 `json:"replicas"`
    
    // +kubebuilder:validation:Enum=small;medium;large
    Size string `json:"size"`
}
```

### **RBAC Markers**

```go
//+kubebuilder:rbac:groups=apps.mycompany.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=apps.mycompany.com,resources=myapps/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=apps.mycompany.com,resources=myapps/finalizers,verbs=update
//+kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=pods,verbs=get;list;watch
```

### **Pros & Cons**

**Pros:**
- ✅ Official Kubernetes project
- ✅ Clean, minimal approach
- ✅ Excellent documentation
- ✅ Modern Go practices
- ✅ Active maintenance

**Cons:**
- ⚠️ No built-in OLM support
- ⚠️ Less enterprise tooling
- ⚠️ Manual bundle creation

---

## **Option 3: controller-runtime (Low-Level)**

### **What is controller-runtime?**

controller-runtime is the underlying library used by both Operator SDK and Kubebuilder. It provides the core controller functionality without scaffolding tools.

### **When to Use**

- Need maximum control and customization
- Building unique operators that don't fit standard patterns
- Want minimal dependencies
- Already familiar with Kubernetes internals

### **Quick Example**

```go
package main

import (
    "context"
    "fmt"
    
    corev1 "k8s.io/api/core/v1"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/manager"
    "sigs.k8s.io/controller-runtime/pkg/reconcile"
)

type MyReconciler struct {
    client.Client
}

func (r *MyReconciler) Reconcile(ctx context.Context, req reconcile.Request) (reconcile.Result, error) {
    // Custom reconciliation logic
    pod := &corev1.Pod{}
    err := r.Get(ctx, req.NamespacedName, pod)
    if err != nil {
        return reconcile.Result{}, client.IgnoreNotFound(err)
    }
    
    fmt.Printf("Reconciling pod: %s\n", pod.Name)
    return reconcile.Result{}, nil
}

func main() {
    mgr, err := manager.New(manager.GetConfigOrDie(), manager.Options{})
    if err != nil {
        panic(err)
    }
    
    err = (&MyReconciler{
        Client: mgr.GetClient(),
    }).SetupWithManager(mgr)
    if err != nil {
        panic(err)
    }
    
    if err := mgr.Start(context.Background()); err != nil {
        panic(err)
    }
}
```

### **Pros & Cons**

**Pros:**
- ✅ Maximum flexibility
- ✅ Minimal dependencies
- ✅ Full control over implementation

**Cons:**
- ⚠️ No scaffolding
- ⚠️ Manual CRD creation
- ⚠️ Steep learning curve
- ⚠️ More boilerplate code

---

## **Option 4: client-go (From Scratch)**

### **What is client-go?**

client-go is the official Go client for Kubernetes. Building operators from scratch using only client-go gives you complete control but requires deep Kubernetes knowledge.

### **When to Use**

- Need absolute control
- Building non-standard operators
- Learning Kubernetes internals
- Performance-critical applications

### **Basic Example**

```go
package main

import (
    "context"
    "fmt"
    "time"
    
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/watch"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
)

func main() {
    // Create in-cluster config
    config, err := rest.InClusterConfig()
    if err != nil {
        panic(err)
    }
    
    // Create clientset
    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        panic(err)
    }
    
    // Watch pods
    watcher, err := clientset.CoreV1().Pods("default").Watch(context.TODO(), metav1.ListOptions{})
    if err != nil {
        panic(err)
    }
    
    for event := range watcher.ResultChan() {
        pod, ok := event.Object.(*corev1.Pod)
        if !ok {
            continue
        }
        
        fmt.Printf("Event: %s, Pod: %s\n", event.Type, pod.Name)
        
        // Custom reconciliation logic here
    }
}
```

### **Pros & Cons**

**Pros:**
- ✅ Complete control
- ✅ No framework dependencies
- ✅ Deep understanding of Kubernetes

**Cons:**
- ⚠️ Very high complexity
- ⚠️ Manual everything (CRDs, RBAC, deployment)
- ⚠️ Error-prone
- ⚠️ Time-consuming
- ⚠️ Not recommended for most use cases

---

## **Comparison Matrix**

| Feature | Operator SDK | Kubebuilder | controller-runtime | client-go |
|---------|--------------|-------------|-------------------|-----------|
| **Scaffolding** | ✅ Excellent | ✅ Excellent | ❌ None | ❌ None |
| **OLM Support** | ✅ Built-in | ⚠️ Manual | ❌ No | ❌ No |
| **Learning Curve** | Medium | Medium | Steep | Very Steep |
| **Documentation** | ✅ Good | ✅ Excellent | ⚠️ OK | ⚠️ OK |
| **Community** | Large | Large | Medium | Large |
| **Flexibility** | Medium | Medium | High | Very High |
| **Best For** | Production | Modern Ops | Custom | Advanced |
| **Setup Time** | Fast | Fast | Slow | Very Slow |

---

## **Recommendation Decision Tree**

```
Are you building a production operator for distribution?
├─ Yes → Use Operator SDK
│   └─ Need OLM/OperatorHub? → Operator SDK
└─ No  → Building for internal use?
    ├─ Yes → Use Kubebuilder (simpler, cleaner)
    └─ No  → Need maximum customization?
        ├─ Yes → Use controller-runtime
        └─ No  → Learning? → Use Kubebuilder
                 └─ Expert? → Use client-go
```

---

## **Getting Started Workflow**

### **Step 1: Prerequisites**

```bash
# Install Go (1.21+)
go version

# Install Docker
docker version

# Install kubectl
kubectl version --client

# Access to Kubernetes cluster (minikube, kind, or remote)
kubectl cluster-info

# Install chosen framework
# Operator SDK or Kubebuilder (see installation sections above)
```

### **Step 2: Create Project**

**With Operator SDK:**
```bash
operator-sdk init --domain=mycompany.com --repo=github.com/mycompany/myoperator
operator-sdk create api --group=apps --version=v1 --kind=MyApp --resource --controller
```

**With Kubebuilder:**
```bash
kubebuilder init --domain=mycompany.com --repo=github.com/mycompany/myoperator
kubebuilder create api --group=apps --version=v1 --kind=MyApp
```

### **Step 3: Define API**

Edit `api/v1/myapp_types.go`:

```go
type MyAppSpec struct {
    // Your desired state fields
    Size     int32  `json:"size"`
    Image    string `json:"image"`
    Version  string `json:"version"`
}

type MyAppStatus struct {
    // Observed state fields
    Nodes      []string           `json:"nodes"`
    Conditions []metav1.Condition `json:"conditions,omitempty"`
}
```

### **Step 4: Generate Manifests**

```bash
make manifests
make generate
```

### **Step 5: Implement Controller**

Edit `controllers/myapp_controller.go`:

```go
func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the custom resource
    // 2. Check if dependent resources exist
    // 3. Create/Update dependent resources
    // 4. Update status
    // 5. Return result
}
```

### **Step 6: Test Locally**

```bash
# Install CRDs
make install

# Run operator locally (outside cluster)
make run

# In another terminal, create a CR
kubectl apply -f config/samples/
```

### **Step 7: Build & Deploy**

```bash
# Build container image
make docker-build IMG=myregistry/myoperator:v1.0

# Push to registry
make docker-push IMG=myregistry/myoperator:v1.0

# Deploy to cluster
make deploy IMG=myregistry/myoperator:v1.0
```

### **Step 8: Verify**

```bash
# Check operator pod
kubectl get pods -n myoperator-system

# Create custom resource
kubectl apply -f config/samples/apps_v1_myapp.yaml

# Check custom resource
kubectl get myapps

# Check operator logs
kubectl logs -n myoperator-system deployment/myoperator-controller-manager
```

---

## **Best Practices**

### **1. Use Finalizers for Cleanup**

```go
const myAppFinalizer = "myapp.mycompany.com/finalizer"

if myApp.ObjectMeta.DeletionTimestamp.IsZero() {
    if !containsString(myApp.GetFinalizers(), myAppFinalizer) {
        controllerutil.AddFinalizer(myApp, myAppFinalizer)
        if err := r.Update(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
    }
} else {
    // Handle deletion
    if containsString(myApp.GetFinalizers(), myAppFinalizer) {
        if err := r.cleanupExternalResources(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        
        controllerutil.RemoveFinalizer(myApp, myAppFinalizer)
        if err := r.Update(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
    }
}
```

### **2. Implement Status Conditions**

```go
import "k8s.io/apimachinery/pkg/api/meta"

meta.SetStatusCondition(&myApp.Status.Conditions, metav1.Condition{
    Type:    "Ready",
    Status:  metav1.ConditionTrue,
    Reason:  "DeploymentReady",
    Message: "Deployment is ready with 3 replicas",
})

if err := r.Status().Update(ctx, myApp); err != nil {
    return ctrl.Result{}, err
}
```

### **3. Use Owner References**

```go
import "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"

deployment := &appsv1.Deployment{...}
if err := controllerutil.SetControllerReference(myApp, deployment, r.Scheme); err != nil {
    return ctrl.Result{}, err
}
```

### **4. Handle Errors Gracefully**

```go
if err != nil {
    log.Error(err, "Failed to create deployment")
    return ctrl.Result{RequeueAfter: time.Minute}, err
}
```

### **5. Add Metrics**

```go
import "github.com/prometheus/client_golang/prometheus"

var (
    reconciliationTotal = prometheus.NewCounter(
        prometheus.CounterOpts{
            Name: "myapp_reconciliations_total",
            Help: "Total number of reconciliations",
        },
    )
)

func (r *MyAppReconciler) Reconcile(...) {
    reconciliationTotal.Inc()
    // ...
}
```

---

## **Learning Resources**

### **Official Documentation**
- **Operator SDK**: https://sdk.operatorframework.io/
- **Kubebuilder Book**: https://book.kubebuilder.io/
- **controller-runtime**: https://pkg.go.dev/sigs.k8s.io/controller-runtime

### **Sample Projects**
- IBM Operator Samples: https://github.com/IBM/operator-sample-go
- Operator SDK Samples: https://github.com/operator-framework/operator-sdk/tree/master/testdata

### **Tutorials**
- Operator SDK Go Tutorial: https://sdk.operatorframework.io/docs/building-operators/golang/tutorial/
- Kubebuilder Tutorial: https://book.kubebuilder.io/cronjob-tutorial/cronjob-tutorial.html

### **Videos**
- KubeCon Operator Development talks
- YouTube: "Kubernetes Operator in Go"

---

## **Summary**

For **most use cases**, start with:
- **Operator SDK** if you need OLM/distribution
- **Kubebuilder** for clean, internal operators

Both provide excellent scaffolding, documentation, and community support. You can always drop down to controller-runtime or client-go later if you need more control.

**Don't start from scratch** unless you have a very good reason!
