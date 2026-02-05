# Complete Step-by-Step Guide: Building a Kubernetes Operator on DigitalOcean

## Complete Hands-On Tutorial with Expected Outputs

This guide will walk you through creating a **real production-ready Kubernetes operator** from scratch on DigitalOcean, with every command, expected output, and troubleshooting step included.

---

## **What We'll Build**

A **Visitor Counter Operator** that:
- Manages a custom resource called `VisitorApp`
- Automatically deploys a web application with MySQL backend
- Scales the application based on specifications
- Manages the complete lifecycle of the application

---

## **Table of Contents**

1. [Prerequisites & Setup](#step-1-prerequisites--setup)
2. [Create DigitalOcean Kubernetes Cluster](#step-2-create-digitalocean-kubernetes-cluster)
3. [Install Development Tools](#step-3-install-development-tools)
4. [Initialize Operator Project](#step-4-initialize-operator-project)
5. [Create API and Controller](#step-5-create-api-and-controller)
6. [Define Custom Resource](#step-6-define-custom-resource)
7. [Implement Controller Logic](#step-7-implement-controller-logic)
8. [Test Locally](#step-8-test-locally)
9. [Build and Push Container Image](#step-9-build-and-push-container-image)
10. [Deploy to DigitalOcean](#step-10-deploy-to-digitalocean)
11. [Test the Operator](#step-11-test-the-operator)
12. [Troubleshooting](#step-12-troubleshooting)

---

## **Step 1: Prerequisites & Setup**

### **1.1 Create DigitalOcean Account**

**Actions:**
1. Go to https://cloud.digitalocean.com/
2. Sign up or log in
3. Add payment method (needed for Kubernetes cluster)

**Expected Screen:**
```
✓ You should see the DigitalOcean Dashboard
✓ Top navigation: Create → Droplets, Kubernetes, Databases, etc.
```

### **1.2 Prepare Your Local Machine**

**Required software:**
- Go 1.21+
- Docker
- kubectl
- doctl (DigitalOcean CLI)
- Operator SDK

**Installation Commands:**

#### **Install Go (if not installed)**

```bash
# Check if Go is installed
go version

# If not installed, download from https://go.dev/dl/
# For macOS:
brew install go

# For Linux:
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify installation
go version
```

**Expected Output:**
```
go version go1.21.5 linux/amd64
```

#### **Install Docker**

```bash
# For macOS:
brew install docker

# For Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker version
```

**Expected Output:**
```
Client:
 Version:           24.0.7
 API version:       1.43
 Go version:        go1.21.5
 ...
Server:
 Engine:
  Version:          24.0.7
  API version:      1.43 (minimum version 1.12)
```

#### **Install kubectl**

```bash
# For macOS:
brew install kubectl

# For Linux:
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify
kubectl version --client
```

**Expected Output:**
```
Client Version: v1.29.0
Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3
```

#### **Install doctl (DigitalOcean CLI)**

```bash
# For macOS:
brew install doctl

# For Linux:
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.104.0/doctl-1.104.0-linux-amd64.tar.gz
tar xf ~/doctl-1.104.0-linux-amd64.tar.gz
sudo mv ~/doctl /usr/local/bin

# Verify
doctl version
```

**Expected Output:**
```
doctl version 1.104.0-release
```

#### **Authenticate doctl**

```bash
# Get API token from DigitalOcean
# 1. Go to https://cloud.digitalocean.com/account/api/tokens
# 2. Click "Generate New Token"
# 3. Name: "kubectl-access"
# 4. Select: Read and Write
# 5. Click "Generate Token"
# 6. COPY THE TOKEN IMMEDIATELY (you won't see it again)

# Initialize doctl
doctl auth init
```

**Prompt:**
```
Please authenticate doctl for use with your DigitalOcean account. You can generate a token in the control panel at https://cloud.digitalocean.com/account/api/tokens

Enter your access token: 
```

**Action:** Paste your token and press Enter

**Expected Output:**
```
Validating token... OK
```

**Verify authentication:**
```bash
doctl account get
```

**Expected Output:**
```
Email                    Droplet Limit    Email Verified    UUID                                    Status
your-email@example.com   10               true              abc123def-4567-89ab-cdef-0123456789ab   active
```

#### **Install Operator SDK**

```bash
# For macOS:
brew install operator-sdk

# For Linux:
export ARCH=$(case $(uname -m) in x86_64) echo -n amd64 ;; aarch64) echo -n arm64 ;; *) echo -n $(uname -m) ;; esac)
export OS=$(uname | awk '{print tolower($0)}')
export OPERATOR_SDK_DL_URL=https://github.com/operator-framework/operator-sdk/releases/download/v1.34.1
curl -LO ${OPERATOR_SDK_DL_URL}/operator-sdk_${OS}_${ARCH}
chmod +x operator-sdk_${OS}_${ARCH}
sudo mv operator-sdk_${OS}_${ARCH} /usr/local/bin/operator-sdk

# Verify
operator-sdk version
```

**Expected Output:**
```
operator-sdk version: "v1.34.1", commit: "fe25e0fb2ef2aa9c1ea496aa9e0db36b41b42383", kubernetes version: "v1.28.0", go version: "go1.21.5", GOOS: "linux", GOARCH: "amd64"
```

---

## **Step 2: Create DigitalOcean Kubernetes Cluster**

### **2.1 Create Cluster via Web UI**

**Actions:**

1. **Navigate to Kubernetes section**
   - Click "Create" button (top right)
   - Select "Kubernetes"

2. **Configure cluster**
   
   **Cluster Configuration Screen:**
   ```
   Choose a Kubernetes version
   ├─ Select: 1.29.0-do.0 (or latest stable)
   
   Choose a datacenter region
   ├─ Select: New York 1 (or closest to you)
   
   Choose cluster capacity
   ├─ Node pool name: worker-pool
   ├─ Machine type: Basic nodes
   ├─ Node plan: 
   │  └─ Select: $12/month (2 GB RAM / 1 vCPU)
   └─ Number of nodes: 2
   
   Finalize and create
   ├─ Name your cluster: visitor-operator-cluster
   └─ Tags: operator, tutorial
   ```

3. **Click "Create Cluster"**

**Expected Screen After Creation:**
```
✓ Cluster Status: Creating...
✓ Progress bar showing: "Provisioning nodes"
✓ Wait time: 3-5 minutes
```

**When complete:**
```
✓ Cluster Status: Running
✓ Green checkmark indicator
✓ Download config button visible
```

### **2.2 Configure kubectl Access**

**Method 1: Via Web UI**

1. Click "Download Config File" button
2. Save to `~/.kube/config-do` (or any location)

```bash
# Set KUBECONFIG environment variable
export KUBECONFIG=~/.kube/config-do

# Or merge with existing config
mkdir -p ~/.kube
mv ~/Downloads/visitor-operator-cluster-kubeconfig.yaml ~/.kube/config-do
export KUBECONFIG=~/.kube/config-do
```

**Method 2: Via doctl (Recommended)**

```bash
# List clusters
doctl kubernetes cluster list
```

**Expected Output:**
```
ID                                      Name                       Region    Version        Auto Upgrade    Status     Node Pools
abc12345-6789-0abc-def0-123456789012    visitor-operator-cluster   nyc1      1.29.0-do.0    false          running    worker-pool
```

```bash
# Get cluster ID (from above output)
CLUSTER_ID="abc12345-6789-0abc-def0-123456789012"

# Configure kubectl
doctl kubernetes cluster kubeconfig save $CLUSTER_ID
```

**Expected Output:**
```
Notice: Adding cluster credentials to kubeconfig file found in "/home/user/.kube/config"
Notice: Setting current-context to do-nyc1-visitor-operator-cluster
```

### **2.3 Verify Cluster Access**

```bash
# Test connection
kubectl cluster-info
```

**Expected Output:**
```
Kubernetes control plane is running at https://abc12345-6789-0abc-def0-123456789012.k8s.ondigitalocean.com
CoreDNS is running at https://abc12345-6789-0abc-def0-123456789012.k8s.ondigitalocean.com/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

```bash
# View nodes
kubectl get nodes
```

**Expected Output:**
```
NAME                   STATUS   ROLES    AGE     VERSION
worker-pool-abc123     Ready    <none>   5m30s   v1.29.0
worker-pool-def456     Ready    <none>   5m25s   v1.29.0
```

```bash
# View all pods (should see system pods running)
kubectl get pods -A
```

**Expected Output:**
```
NAMESPACE     NAME                                      READY   STATUS    RESTARTS   AGE
kube-system   cilium-operator-5d4f7c9d9f-8xhqw         1/1     Running   0          6m
kube-system   cilium-xjkl4                             1/1     Running   0          6m
kube-system   coredns-7db6d8ff4d-kwmzp                 1/1     Running   0          6m
kube-system   coredns-7db6d8ff4d-rh8bn                 1/1     Running   0          6m
kube-system   csi-do-node-4zmhp                        2/2     Running   0          6m
kube-system   csi-do-node-xkwpl                        2/2     Running   0          6m
kube-system   do-node-agent-9pzc7                      1/1     Running   0          6m
kube-system   do-node-agent-fkwxn                      1/1     Running   0          6m
kube-system   kube-proxy-7njcw                         1/1     Running   0          6m
kube-system   kube-proxy-xvwqk                         1/1     Running   0          6m
```

**✅ Checkpoint:** You now have a working Kubernetes cluster on DigitalOcean!

---

## **Step 3: Install Development Tools**

### **3.1 Set Up Project Directory**

```bash
# Create workspace
mkdir -p ~/operator-projects
cd ~/operator-projects

# Verify you're in the right place
pwd
```

**Expected Output:**
```
/home/user/operator-projects
```

### **3.2 Install Make (if not installed)**

```bash
# Check if make is installed
make --version

# If not installed:
# Ubuntu/Debian:
sudo apt-get install build-essential

# macOS:
# (Usually pre-installed)
```

**Expected Output:**
```
GNU Make 4.3
Built for x86_64-pc-linux-gnu
```

---

## **Step 4: Initialize Operator Project**

### **4.1 Create Project Directory**

```bash
# Create and enter project directory
mkdir visitor-operator
cd visitor-operator

# Verify empty directory
ls -la
```

**Expected Output:**
```
total 8
drwxr-xr-x  2 user user 4096 Feb  5 10:00 .
drwxr-xr-x  3 user user 4096 Feb  5 10:00 ..
```

### **4.2 Initialize Operator Project**

```bash
# Initialize with Operator SDK
operator-sdk init \
  --domain=example.com \
  --repo=github.com/yourname/visitor-operator \
  --plugins=go/v4
```

**Expected Output:**
```
Writing kustomize manifests for you to edit...
Writing scaffold for you to edit...
Get controller runtime:
$ go get sigs.k8s.io/controller-runtime@v0.16.3
Update dependencies:
$ go mod tidy
Next: define a resource with:
$ operator-sdk create api
```

### **4.3 Examine Generated Files**

```bash
# List all files
ls -la
```

**Expected Output:**
```
total 56
drwxr-xr-x  8 user user  4096 Feb  5 10:05 .
drwxr-xr-x  3 user user  4096 Feb  5 10:00 ..
-rw-r--r--  1 user user   154 Feb  5 10:05 .dockerignore
-rw-r--r--  1 user user   367 Feb  5 10:05 .gitignore
-rw-r--r--  1 user user  1070 Feb  5 10:05 Dockerfile
-rw-r--r--  1 user user  5835 Feb  5 10:05 Makefile
-rw-r--r--  1 user user   156 Feb  5 10:05 PROJECT
-rw-r--r--  1 user user  3264 Feb  5 10:05 README.md
drwxr-xr-x  2 user user  4096 Feb  5 10:05 cmd
drwxr-xr-x  2 user user  4096 Feb  5 10:05 config
-rw-r--r--  1 user user  2105 Feb  5 10:05 go.mod
-rw-r--r--  1 user user 89456 Feb  5 10:05 go.sum
drwxr-xr-x  2 user user  4096 Feb  5 10:05 hack
```

**View the PROJECT file:**
```bash
cat PROJECT
```

**Expected Output:**
```yaml
domain: example.com
layout:
- go.kubebuilder.io/v4
plugins:
  manifests.sdk.operatorframework.io/v2: {}
  scorecard.sdk.operatorframework.io/v2: {}
projectName: visitor-operator
repo: github.com/yourname/visitor-operator
version: "3"
```

**✅ Checkpoint:** Project structure is initialized!

---

## **Step 5: Create API and Controller**

### **5.1 Generate API**

```bash
# Create API for VisitorApp resource
operator-sdk create api \
  --group app \
  --version v1 \
  --kind VisitorApp \
  --resource \
  --controller
```

**Prompts:**
```
Create Resource [y/n]
```
**Type:** `y` and press Enter

```
Create Controller [y/n]
```
**Type:** `y` and press Enter

**Expected Output:**
```
Writing kustomize manifests for you to edit...
Writing scaffold for you to edit...
api/v1/visitorapp_types.go
api/v1/groupversion_info.go
internal/controller/suite_test.go
internal/controller/visitorapp_controller.go
Update dependencies:
$ go mod tidy
Running make:
$ make generate
mkdir -p /home/user/operator-projects/visitor-operator/bin
test -s /home/user/operator-projects/visitor-operator/bin/controller-gen && /home/user/operator-projects/visitor-operator/bin/controller-gen --version | grep -q v0.13.0 || \
GOBIN=/home/user/operator-projects/visitor-operator/bin go install sigs.k8s.io/controller-tools/cmd/controller-gen@v0.13.0
/home/user/operator-projects/visitor-operator/bin/controller-gen object:headerFile="hack/boilerplate.go.txt" paths="./..."
Next: implement your new API and generate the manifests (e.g. CRDs,CRs) with:
$ make manifests
```

### **5.2 Verify Generated Files**

```bash
# Check directory structure
tree -L 3 .
```

**Expected Output:**
```
.
├── api
│   └── v1
│       ├── groupversion_info.go
│       ├── visitorapp_types.go
│       └── zz_generated.deepcopy.go
├── cmd
│   └── main.go
├── config
│   ├── crd
│   ├── default
│   ├── manager
│   ├── manifests
│   ├── prometheus
│   ├── rbac
│   └── samples
│       └── app_v1_visitorapp.yaml
├── internal
│   └── controller
│       ├── suite_test.go
│       └── visitorapp_controller.go
├── Dockerfile
├── go.mod
├── go.sum
├── Makefile
├── PROJECT
└── README.md
```

**✅ Checkpoint:** API and Controller scaffolded successfully!

---

## **Step 6: Define Custom Resource**

### **6.1 Edit VisitorApp Types**

```bash
# Open the types file
nano api/v1/visitorapp_types.go
# Or use your preferred editor: vim, code, etc.
```

**Find this section:**
```go
// VisitorAppSpec defines the desired state of VisitorApp
type VisitorAppSpec struct {
    // INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
    // Important: Run "make" to regenerate code after modifying this file

    // Foo is an example field of VisitorApp. Edit visitorapp_types.go to remove/update
    Foo string `json:"foo,omitempty"`
}
```

**Replace with:**
```go
// VisitorAppSpec defines the desired state of VisitorApp
type VisitorAppSpec struct {
    // Size is the number of replicas for the frontend
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    Size int32 `json:"size"`

    // Title is the title displayed on the webpage
    // +kubebuilder:validation:MinLength=1
    Title string `json:"title"`
}
```

**Find this section:**
```go
// VisitorAppStatus defines the observed state of VisitorApp
type VisitorAppStatus struct {
    // INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
    // Important: Run "make" to regenerate code after modifying this file
}
```

**Replace with:**
```go
// VisitorAppStatus defines the observed state of VisitorApp
type VisitorAppStatus struct {
    // BackendImage is the image used for the backend
    BackendImage string `json:"backendImage,omitempty"`

    // FrontendImage is the image used for the frontend
    FrontendImage string `json:"frontendImage,omitempty"`
}
```

**Add status subresource marker** (find the VisitorApp struct):
```go
// VisitorApp is the Schema for the visitorapps API
// +kubebuilder:subresource:status
type VisitorApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   VisitorAppSpec   `json:"spec,omitempty"`
    Status VisitorAppStatus `json:"status,omitempty"`
}
```

**Save and exit** (Ctrl+X, then Y, then Enter if using nano)

### **6.2 Generate Manifests**

```bash
# Generate CRD manifests
make manifests
```

**Expected Output:**
```
mkdir -p /home/user/operator-projects/visitor-operator/bin
test -s /home/user/operator-projects/visitor-operator/bin/controller-gen || GOBIN=/home/user/operator-projects/visitor-operator/bin go install sigs.k8s.io/controller-tools/cmd/controller-gen@v0.13.0
/home/user/operator-projects/visitor-operator/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
```

### **6.3 View Generated CRD**

```bash
# View the CRD YAML
cat config/crd/bases/app.example.com_visitorapps.yaml
```

**Expected Output (partial):**
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: visitorapps.app.example.com
spec:
  group: app.example.com
  names:
    kind: VisitorApp
    listKind: VisitorAppList
    plural: visitorapps
    singular: visitorapp
  scope: Namespaced
  versions:
  - name: v1
    schema:
      openAPIV3Schema:
        properties:
          spec:
            properties:
              size:
                format: int32
                maximum: 10
                minimum: 1
                type: integer
              title:
                minLength: 1
                type: string
            required:
            - size
            - title
            type: object
          status:
            properties:
              backendImage:
                type: string
              frontendImage:
                type: string
            type: object
        type: object
    served: true
    storage: true
    subresources:
      status: {}
```

**✅ Checkpoint:** Custom Resource Definition is ready!

---

## **Step 7: Implement Controller Logic**

### **7.1 Edit Controller**

```bash
# Open controller file
nano internal/controller/visitorapp_controller.go
```

**Find the Reconcile function** (around line 50):

**Replace the entire Reconcile function with this implementation:**

```go
func (r *VisitorAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    // Fetch the VisitorApp instance
    visitorApp := &appv1.VisitorApp{}
    err := r.Get(ctx, req.NamespacedName, visitorApp)
    if err != nil {
        if errors.IsNotFound(err) {
            // Object not found, return
            log.Info("VisitorApp resource not found. Ignoring since object must be deleted")
            return ctrl.Result{}, nil
        }
        // Error reading the object
        log.Error(err, "Failed to get VisitorApp")
        return ctrl.Result{}, err
    }

    // Define backend MySQL deployment
    backend := r.backendDeployment(visitorApp)
    
    // Check if backend deployment exists
    foundBackend := &appsv1.Deployment{}
    err = r.Get(ctx, types.NamespacedName{Name: backend.Name, Namespace: backend.Namespace}, foundBackend)
    if err != nil && errors.IsNotFound(err) {
        log.Info("Creating MySQL Deployment", "Deployment.Namespace", backend.Namespace, "Deployment.Name", backend.Name)
        err = r.Create(ctx, backend)
        if err != nil {
            log.Error(err, "Failed to create MySQL Deployment", "Deployment.Namespace", backend.Namespace, "Deployment.Name", backend.Name)
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    } else if err != nil {
        log.Error(err, "Failed to get MySQL Deployment")
        return ctrl.Result{}, err
    }

    // Define backend MySQL service
    backendService := r.backendService(visitorApp)
    foundBackendService := &corev1.Service{}
    err = r.Get(ctx, types.NamespacedName{Name: backendService.Name, Namespace: backendService.Namespace}, foundBackendService)
    if err != nil && errors.IsNotFound(err) {
        log.Info("Creating MySQL Service", "Service.Namespace", backendService.Namespace, "Service.Name", backendService.Name)
        err = r.Create(ctx, backendService)
        if err != nil {
            log.Error(err, "Failed to create MySQL Service")
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    } else if err != nil {
        log.Error(err, "Failed to get MySQL Service")
        return ctrl.Result{}, err
    }

    // Define frontend deployment
    frontend := r.frontendDeployment(visitorApp)
    
    // Check if frontend deployment exists
    foundFrontend := &appsv1.Deployment{}
    err = r.Get(ctx, types.NamespacedName{Name: frontend.Name, Namespace: frontend.Namespace}, foundFrontend)
    if err != nil && errors.IsNotFound(err) {
        log.Info("Creating Frontend Deployment", "Deployment.Namespace", frontend.Namespace, "Deployment.Name", frontend.Name)
        err = r.Create(ctx, frontend)
        if err != nil {
            log.Error(err, "Failed to create Frontend Deployment")
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    } else if err != nil {
        log.Error(err, "Failed to get Frontend Deployment")
        return ctrl.Result{}, err
    }

    // Update frontend deployment if size changed
    size := visitorApp.Spec.Size
    if *foundFrontend.Spec.Replicas != size {
        foundFrontend.Spec.Replicas = &size
        err = r.Update(ctx, foundFrontend)
        if err != nil {
            log.Error(err, "Failed to update Frontend Deployment", "Deployment.Namespace", foundFrontend.Namespace, "Deployment.Name", foundFrontend.Name)
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    }

    // Define frontend service
    frontendService := r.frontendService(visitorApp)
    foundFrontendService := &corev1.Service{}
    err = r.Get(ctx, types.NamespacedName{Name: frontendService.Name, Namespace: frontendService.Namespace}, foundFrontendService)
    if err != nil && errors.IsNotFound(err) {
        log.Info("Creating Frontend Service", "Service.Namespace", frontendService.Namespace, "Service.Name", frontendService.Name)
        err = r.Create(ctx, frontendService)
        if err != nil {
            log.Error(err, "Failed to create Frontend Service")
            return ctrl.Result{}, err
        }
        return ctrl.Result{Requeue: true}, nil
    } else if err != nil {
        log.Error(err, "Failed to get Frontend Service")
        return ctrl.Result{}, err
    }

    // Update status
    visitorApp.Status.BackendImage = "mysql:5.7"
    visitorApp.Status.FrontendImage = "jdob/visitors-webui:latest"
    err = r.Status().Update(ctx, visitorApp)
    if err != nil {
        log.Error(err, "Failed to update VisitorApp status")
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

**Add helper functions** (add these after the Reconcile function, before SetupWithManager):

```go
// backendDeployment creates the MySQL deployment
func (r *VisitorAppReconciler) backendDeployment(v *appv1.VisitorApp) *appsv1.Deployment {
    labels := map[string]string{
        "app":             "visitors",
        "visitorssite_cr": v.Name,
        "tier":            "backend",
    }

    size := int32(1)

    dep := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "mysql-backend",
            Namespace: v.Namespace,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &size,
            Selector: &metav1.LabelSelector{
                MatchLabels: labels,
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: labels,
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{{
                        Image: "mysql:5.7",
                        Name:  "visitors-mysql",
                        Ports: []corev1.ContainerPort{{
                            ContainerPort: 3306,
                            Name:          "mysql",
                        }},
                        Env: []corev1.EnvVar{
                            {
                                Name:  "MYSQL_ROOT_PASSWORD",
                                Value: "password",
                            },
                            {
                                Name:  "MYSQL_DATABASE",
                                Value: "visitors_db",
                            },
                        },
                    }},
                },
            },
        },
    }

    controllerutil.SetControllerReference(v, dep, r.Scheme)
    return dep
}

// backendService creates the MySQL service
func (r *VisitorAppReconciler) backendService(v *appv1.VisitorApp) *corev1.Service {
    labels := map[string]string{
        "app":             "visitors",
        "visitorssite_cr": v.Name,
        "tier":            "backend",
    }

    svc := &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "mysql-service",
            Namespace: v.Namespace,
        },
        Spec: corev1.ServiceSpec{
            Selector: labels,
            Ports: []corev1.ServicePort{{
                Port: 3306,
            }},
            ClusterIP: "None",
        },
    }

    controllerutil.SetControllerReference(v, svc, r.Scheme)
    return svc
}

// frontendDeployment creates the web app deployment
func (r *VisitorAppReconciler) frontendDeployment(v *appv1.VisitorApp) *appsv1.Deployment {
    labels := map[string]string{
        "app":             "visitors",
        "visitorssite_cr": v.Name,
        "tier":            "frontend",
    }

    size := v.Spec.Size

    dep := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "frontend",
            Namespace: v.Namespace,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &size,
            Selector: &metav1.LabelSelector{
                MatchLabels: labels,
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: labels,
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{{
                        Image: "jdob/visitors-webui:latest",
                        Name:  "visitors-webui",
                        Ports: []corev1.ContainerPort{{
                            ContainerPort: 8000,
                            Name:          "visitors",
                        }},
                        Env: []corev1.EnvVar{
                            {
                                Name:  "MYSQL_DATABASE",
                                Value: "visitors_db",
                            },
                            {
                                Name:  "MYSQL_SERVICE_HOST",
                                Value: "mysql-service",
                            },
                            {
                                Name:  "MYSQL_PASSWORD",
                                Value: "password",
                            },
                            {
                                Name:  "MYSQL_USERNAME",
                                Value: "root",
                            },
                        },
                    }},
                },
            },
        },
    }

    controllerutil.SetControllerReference(v, dep, r.Scheme)
    return dep
}

// frontendService creates the web app service
func (r *VisitorAppReconciler) frontendService(v *appv1.VisitorApp) *corev1.Service {
    labels := map[string]string{
        "app":             "visitors",
        "visitorssite_cr": v.Name,
        "tier":            "frontend",
    }

    svc := &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "frontend-service",
            Namespace: v.Namespace,
        },
        Spec: corev1.ServiceSpec{
            Type:     corev1.ServiceTypeLoadBalancer,
            Selector: labels,
            Ports: []corev1.ServicePort{{
                Port:       80,
                TargetPort: intstr.FromInt(8000),
            }},
        },
    }

    controllerutil.SetControllerReference(v, svc, r.Scheme)
    return svc
}
```

**Add required imports at the top of the file:**

Find the import section and add these:

```go
import (
    "context"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    "k8s.io/apimachinery/pkg/util/intstr"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
    "sigs.k8s.io/controller-runtime/pkg/log"

    appv1 "github.com/yourname/visitor-operator/api/v1"
)
```

**Update RBAC markers** (find the existing markers and add these):

```go
//+kubebuilder:rbac:groups=app.example.com,resources=visitorapps,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=app.example.com,resources=visitorapps/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=app.example.com,resources=visitorapps/finalizers,verbs=update
//+kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=pods,verbs=get;list;watch
```

**Save and exit**

### **7.2 Update SetupWithManager**

Find the `SetupWithManager` function and update it to watch Deployments and Services:

```go
// SetupWithManager sets up the controller with the Manager.
func (r *VisitorAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&appv1.VisitorApp{}).
        Owns(&appsv1.Deployment{}).
        Owns(&corev1.Service{}).
        Complete(r)
}
```

### **7.3 Generate Code and Manifests**

```bash
# Generate code
make generate
```

**Expected Output:**
```
mkdir -p /home/user/operator-projects/visitor-operator/bin
/home/user/operator-projects/visitor-operator/bin/controller-gen object:headerFile="hack/boilerplate.go.txt" paths="./..."
```

```bash
# Generate manifests (CRDs, RBAC, etc.)
make manifests
```

**Expected Output:**
```
/home/user/operator-projects/visitor-operator/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
```

**✅ Checkpoint:** Controller logic is implemented!

---

## **Step 8: Test Locally**

### **8.1 Install CRDs**

```bash
# Install CRDs into the cluster
make install
```

**Expected Output:**
```
/home/user/operator-projects/visitor-operator/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
kubectl apply -k config/crd
customresourcedefinition.apiextensions.k8s.io/visitorapps.app.example.com created
```

**Verify CRD installation:**
```bash
kubectl get crds
```

**Expected Output:**
```
NAME                            CREATED AT
visitorapps.app.example.com     2024-02-05T15:30:00Z
```

### **8.2 Run Operator Locally**

```bash
# Run operator outside the cluster (for testing)
make run
```

**Expected Output:**
```
/home/user/operator-projects/visitor-operator/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
/home/user/operator-projects/visitor-operator/bin/controller-gen object:headerFile="hack/boilerplate.go.txt" paths="./..."
go fmt ./...
go vet ./...
go run ./cmd/main.go
2024-02-05T15:31:00Z    INFO    setup    starting manager
2024-02-05T15:31:00Z    INFO    controller-runtime.metrics    Starting metrics server
2024-02-05T15:31:00Z    INFO    controller-runtime.metrics    Serving metrics server    {"bindAddress": ":8080", "secure": false}
2024-02-05T15:31:00Z    INFO    Starting server    {"path": "/metrics", "kind": "metrics", "addr": "[::]:8080"}
2024-02-05T15:31:00Z    INFO    Starting server    {"kind": "health probe", "addr": "[::]:8081"}
2024-02-05T15:31:00Z    INFO    Starting EventSource    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "source": "kind source: *v1.VisitorApp"}
2024-02-05T15:31:00Z    INFO    Starting EventSource    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "source": "kind source: *v1.Deployment"}
2024-02-05T15:31:00Z    INFO    Starting EventSource    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "source": "kind source: *v1.Service"}
2024-02-05T15:31:00Z    INFO    Starting Controller    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp"}
2024-02-05T15:31:00Z    INFO    Starting workers    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "worker count": 1}
```

**✅ The operator is now running!** Keep this terminal open.

### **8.3 Create Sample Custom Resource**

**Open a NEW terminal** and navigate to your project:

```bash
cd ~/operator-projects/visitor-operator
```

**Edit the sample CR:**
```bash
nano config/samples/app_v1_visitorapp.yaml
```

**Replace contents with:**
```yaml
apiVersion: app.example.com/v1
kind: VisitorApp
metadata:
  labels:
    app.kubernetes.io/name: visitorapp
    app.kubernetes.io/instance: visitorapp-sample
    app.kubernetes.io/part-of: visitor-operator
    app.kubernetes.io/managed-by: kustomize
    app.kubernetes.io/created-by: visitor-operator
  name: visitorapp-sample
spec:
  size: 2
  title: "Visitors Counter"
```

**Save and exit**

### **8.4 Apply the Custom Resource**

```bash
kubectl apply -f config/samples/app_v1_visitorapp.yaml
```

**Expected Output:**
```
visitorapp.app.example.com/visitorapp-sample created
```

### **8.5 Watch Operator Logs**

**Switch back to the terminal running the operator** (the one with `make run`)

**You should see new log output:**
```
2024-02-05T15:32:00Z    INFO    Creating MySQL Deployment    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "abc123", "Deployment.Namespace": "default", "Deployment.Name": "mysql-backend"}
2024-02-05T15:32:01Z    INFO    Creating MySQL Service    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "def456", "Service.Namespace": "default", "Service.Name": "mysql-service"}
2024-02-05T15:32:02Z    INFO    Creating Frontend Deployment    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "ghi789", "Deployment.Namespace": "default", "Deployment.Name": "frontend"}
2024-02-05T15:32:03Z    INFO    Creating Frontend Service    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "jkl012", "Service.Namespace": "default", "Service.Name": "frontend-service"}
```

### **8.6 Verify Resources**

**In the second terminal:**

```bash
# Check the VisitorApp resource
kubectl get visitorapps
```

**Expected Output:**
```
NAME                AGE
visitorapp-sample   2m
```

```bash
# Check deployments
kubectl get deployments
```

**Expected Output:**
```
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
mysql-backend    0/1     1            0           2m
frontend         0/2     2            0           2m
```

```bash
# Check services
kubectl get services
```

**Expected Output:**
```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
kubernetes         ClusterIP      10.245.0.1       <none>          443/TCP        30m
mysql-service      ClusterIP      None             <none>          3306/TCP       2m
frontend-service   LoadBalancer   10.245.123.45    <pending>       80:30123/TCP   2m
```

```bash
# Check pods
kubectl get pods
```

**Expected Output:**
```
NAME                             READY   STATUS    RESTARTS   AGE
mysql-backend-5d6f7c9d8f-abc12   1/1     Running   0          2m
frontend-7b8d9c5f6g-def34        1/1     Running   0          2m
frontend-7b8d9c5f6g-ghi56        1/1     Running   0          2m
```

**Wait for LoadBalancer to get external IP:**
```bash
kubectl get service frontend-service -w
```

**After 1-2 minutes, you should see:**
```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
frontend-service   LoadBalancer   10.245.123.45    174.138.45.67    80:30123/TCP   3m
```

**Press Ctrl+C to stop watching**

### **8.7 Test the Application**

```bash
# Get the external IP
EXTERNAL_IP=$(kubectl get service frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Application URL: http://$EXTERNAL_IP"
```

**Expected Output:**
```
Application URL: http://174.138.45.67
```

**Open your browser and navigate to that URL**

**Expected Browser Screen:**
```
╔═══════════════════════════════════╗
║       Visitors Counter            ║
║                                   ║
║  Number of visitors: 1            ║
║                                   ║
║  [Refresh Page]                   ║
╚═══════════════════════════════════╝
```

**Each time you refresh, the counter should increment!**

### **8.8 Test Scaling**

```bash
# Update the CR to scale to 3 replicas
kubectl patch visitorapp visitorapp-sample --type='merge' -p '{"spec":{"size":3}}'
```

**Expected Output:**
```
visitorapp.app.example.com/visitorapp-sample patched
```

**Check operator logs** (in the `make run` terminal):
```
2024-02-05T15:35:00Z    INFO    Updating Frontend Deployment    {"controller": "visitorapp", "Deployment.Namespace": "default", "Deployment.Name": "frontend"}
```

**Verify scaling:**
```bash
kubectl get deployments frontend
```

**Expected Output:**
```
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
frontend   3/3     3            3           5m
```

**✅ Checkpoint:** Operator works locally! Now let's deploy it to the cluster.

**Stop the operator** (Ctrl+C in the terminal running `make run`)

---

## **Step 9: Build and Push Container Image**

### **9.1 Create Docker Hub Account (if you don't have one)**

1. Go to https://hub.docker.com/
2. Sign up for free account
3. Note your username (e.g., `yourdockerusername`)

### **9.2 Login to Docker Hub**

```bash
docker login
```

**Prompts:**
```
Username: yourdockerusername
Password: 
```

**Expected Output:**
```
Login Succeeded
```

### **9.3 Build Operator Image**

```bash
# Set your Docker Hub username
export IMG=yourdockerusername/visitor-operator:v1.0.0

# Build the image
make docker-build IMG=$IMG
```

**Expected Output:**
```
docker build -t yourdockerusername/visitor-operator:v1.0.0 .
[+] Building 45.2s (17/17) FINISHED
 => [internal] load .dockerignore                                          0.0s
 => => transferring context: 154B                                          0.0s
 => [internal] load build definition from Dockerfile                       0.0s
 => [builder 1/9] FROM gcr.io/distroless/static:nonroot                   1.2s
 => [internal] load build context                                          0.1s
 => [builder 2/9] WORKDIR /workspace                                       0.0s
 => [builder 3/9] COPY go.mod go.mod                                       0.0s
 => [builder 4/9] COPY go.sum go.sum                                       0.0s
 => [builder 5/9] RUN go mod download                                     15.3s
 => [builder 6/9] COPY cmd/main.go cmd/main.go                            0.0s
 => [builder 7/9] COPY api/ api/                                           0.0s
 => [builder 8/9] COPY internal/controller/ internal/controller/          0.0s
 => [builder 9/9] RUN CGO_ENABLED=0 GOOS=linux go build -a -o manager cmd/main.go  25.5s
 => [stage-1 2/3] COPY --from=builder /workspace/manager .                0.0s
 => exporting to image                                                     0.1s
 => => exporting layers                                                    0.1s
 => => writing image sha256:abc123...                                      0.0s
 => => naming to docker.io/yourdockerusername/visitor-operator:v1.0.0     0.0s
```

### **9.4 Push Image to Docker Hub**

```bash
make docker-push IMG=$IMG
```

**Expected Output:**
```
docker push yourdockerusername/visitor-operator:v1.0.0
The push refers to repository [docker.io/yourdockerusername/visitor-operator]
abc123: Pushed
def456: Pushed
ghi789: Pushed
v1.0.0: digest: sha256:abc123def456... size: 1234
```

### **9.5 Verify Image on Docker Hub**

1. Go to https://hub.docker.com/
2. Click on your username
3. You should see `visitor-operator` repository
4. Click on it - you should see tag `v1.0.0`

**✅ Checkpoint:** Image is built and pushed!

---

## **Step 10: Deploy to DigitalOcean**

### **10.1 Clean Up Local Test**

```bash
# Delete the test custom resource
kubectl delete -f config/samples/app_v1_visitorapp.yaml
```

**Expected Output:**
```
visitorapp.app.example.com "visitorapp-sample" deleted
```

**Wait for resources to be deleted:**
```bash
kubectl get all
```

**Expected Output (only Kubernetes service should remain):**
```
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.245.0.1   <none>        443/TCP   45m
```

### **10.2 Deploy Operator to Cluster**

```bash
# Deploy the operator
make deploy IMG=$IMG
```

**Expected Output:**
```
cd config/manager && /home/user/operator-projects/visitor-operator/bin/kustomize edit set image controller=yourdockerusername/visitor-operator:v1.0.0
/home/user/operator-projects/visitor-operator/bin/kustomize build config/default | kubectl apply -f -
namespace/visitor-operator-system created
customresourcedefinition.apiextensions.k8s.io/visitorapps.app.example.com unchanged
serviceaccount/visitor-operator-controller-manager created
role.rbac.authorization.k8s.io/visitor-operator-leader-election-role created
clusterrole.rbac.authorization.k8s.io/visitor-operator-manager-role created
clusterrole.rbac.authorization.k8s.io/visitor-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/visitor-operator-proxy-role created
rolebinding.rbac.authorization.k8s.io/visitor-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/visitor-operator-manager-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/visitor-operator-proxy-rolebinding created
service/visitor-operator-controller-manager-metrics-service created
deployment.apps/visitor-operator-controller-manager created
```

### **10.3 Verify Operator Deployment**

```bash
# Check operator namespace
kubectl get all -n visitor-operator-system
```

**Expected Output:**
```
NAME                                                           READY   STATUS    RESTARTS   AGE
pod/visitor-operator-controller-manager-5d6f7c9d8f-abc12      2/2     Running   0          30s

NAME                                                              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/visitor-operator-controller-manager-metrics-service      ClusterIP   10.245.234.12   <none>        8443/TCP   30s

NAME                                                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/visitor-operator-controller-manager      1/1     1            1           30s

NAME                                                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/visitor-operator-controller-manager-5d6f7c9d8f      1         1         1       30s
```

### **10.4 Check Operator Logs**

```bash
kubectl logs -n visitor-operator-system deployment/visitor-operator-controller-manager -c manager
```

**Expected Output:**
```
2024-02-05T16:00:00Z    INFO    setup    starting manager
2024-02-05T16:00:00Z    INFO    controller-runtime.metrics    Starting metrics server
2024-02-05T16:00:00Z    INFO    Starting server    {"kind": "health probe", "addr": "[::]:8081"}
2024-02-05T16:00:00Z    INFO    Starting server    {"path": "/metrics", "kind": "metrics", "addr": "127.0.0.1:8080"}
2024-02-05T16:00:00Z    INFO    Starting EventSource    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "source": "kind source: *v1.VisitorApp"}
2024-02-05T16:00:00Z    INFO    Starting EventSource    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "source": "kind source: *v1.Deployment"}
2024-02-05T16:00:00Z    INFO    Starting EventSource    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "source": "kind source: *v1.Service"}
2024-02-05T16:00:00Z    INFO    Starting Controller    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp"}
2024-02-05T16:00:00Z    INFO    Starting workers    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "worker count": 1}
```

**✅ Checkpoint:** Operator is running in the cluster!

---

## **Step 11: Test the Operator**

### **11.1 Create VisitorApp Instance**

```bash
# Apply the sample CR
kubectl apply -f config/samples/app_v1_visitorapp.yaml
```

**Expected Output:**
```
visitorapp.app.example.com/visitorapp-sample created
```

### **11.2 Watch Resources Being Created**

```bash
# Watch pods
kubectl get pods -w
```

**Expected progression:**
```
NAME                             READY   STATUS              RESTARTS   AGE
mysql-backend-5d6f7c9d8f-abc12   0/1     ContainerCreating   0          5s
mysql-backend-5d6f7c9d8f-abc12   1/1     Running             0          15s
frontend-7b8d9c5f6g-def34        0/1     ContainerCreating   0          5s
frontend-7b8d9c5f6g-ghi56        0/1     ContainerCreating   0          5s
frontend-7b8d9c5f6g-def34        1/1     Running             0          20s
frontend-7b8d9c5f6g-ghi56        1/1     Running             0          22s
```

**Press Ctrl+C to stop watching**

### **11.3 Check Operator Logs**

```bash
kubectl logs -n visitor-operator-system deployment/visitor-operator-controller-manager -c manager --tail=20
```

**Expected Output:**
```
2024-02-05T16:05:00Z    INFO    Creating MySQL Deployment    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "abc123", "Deployment.Namespace": "default", "Deployment.Name": "mysql-backend"}
2024-02-05T16:05:01Z    INFO    Creating MySQL Service    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "def456", "Service.Namespace": "default", "Service.Name": "mysql-service"}
2024-02-05T16:05:02Z    INFO    Creating Frontend Deployment    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "ghi789", "Deployment.Namespace": "default", "Deployment.Name": "frontend"}
2024-02-05T16:05:03Z    INFO    Creating Frontend Service    {"controller": "visitorapp", "controllerGroup": "app.example.com", "controllerKind": "VisitorApp", "VisitorApp": {"name":"visitorapp-sample","namespace":"default"}, "namespace": "default", "name": "visitorapp-sample", "reconcileID": "jkl012", "Service.Namespace": "default", "Service.Name": "frontend-service"}
```

### **11.4 Check All Resources**

```bash
# Check custom resource
kubectl get visitorapps
```

**Expected Output:**
```
NAME                AGE
visitorapp-sample   2m
```

```bash
# Check custom resource details
kubectl describe visitorapp visitorapp-sample
```

**Expected Output:**
```
Name:         visitorapp-sample
Namespace:    default
Labels:       app.kubernetes.io/created-by=visitor-operator
              app.kubernetes.io/instance=visitorapp-sample
              app.kubernetes.io/managed-by=kustomize
              app.kubernetes.io/name=visitorapp
              app.kubernetes.io/part-of=visitor-operator
API Version:  app.example.com/v1
Kind:         VisitorApp
Metadata:
  Creation Timestamp:  2024-02-05T16:05:00Z
  Generation:          1
  Resource Version:    12345
  UID:                 abc-123-def-456
Spec:
  Size:   2
  Title:  Visitors Counter
Status:
  Backend Image:   mysql:5.7
  Frontend Image:  jdob/visitors-webui:latest
Events:            <none>
```

```bash
# Check all resources
kubectl get all
```

**Expected Output:**
```
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mysql-backend-5d6f7c9d8f-abc12   1/1     Running   0          2m
pod/frontend-7b8d9c5f6g-def34        1/1     Running   0          2m
pod/frontend-7b8d9c5f6g-ghi56        1/1     Running   0          2m

NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
service/kubernetes         ClusterIP      10.245.0.1       <none>           443/TCP        1h
service/mysql-service      ClusterIP      None             <none>           3306/TCP       2m
service/frontend-service   LoadBalancer   10.245.123.45    174.138.45.67    80:30123/TCP   2m

NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/mysql-backend   1/1     1            1           2m
deployment.apps/frontend        2/2     2            2           2m

NAME                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/mysql-backend-5d6f7c9d8f   1         1         1       2m
replicaset.apps/frontend-7b8d9c5f6g        2         2         2       2m
```

### **11.5 Access the Application**

```bash
# Get external IP
kubectl get service frontend-service
```

**Expected Output:**
```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
frontend-service   LoadBalancer   10.245.123.45    174.138.45.67    80:30123/TCP   3m
```

```bash
# Get the URL
EXTERNAL_IP=$(kubectl get service frontend-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "Application URL: http://$EXTERNAL_IP"
```

**Open browser to that URL**

**Expected Browser Screen:**
```
╔═══════════════════════════════════╗
║       Visitors Counter            ║
║                                   ║
║  Number of visitors: 1            ║
║                                   ║
║  [Refresh Page]                   ║
╚═══════════════════════════════════╝
```

### **11.6 Test Scaling**

```bash
# Scale to 4 replicas
kubectl patch visitorapp visitorapp-sample --type='merge' -p '{"spec":{"size":4}}'
```

**Expected Output:**
```
visitorapp.app.example.com/visitorapp-sample patched
```

```bash
# Watch scaling
kubectl get pods -l tier=frontend -w
```

**Expected Output:**
```
NAME                        READY   STATUS              RESTARTS   AGE
frontend-7b8d9c5f6g-def34   1/1     Running             0          5m
frontend-7b8d9c5f6g-ghi56   1/1     Running             0          5m
frontend-7b8d9c5f6g-jkl78   0/1     ContainerCreating   0          2s
frontend-7b8d9c5f6g-mno90   0/1     ContainerCreating   0          2s
frontend-7b8d9c5f6g-jkl78   1/1     Running             0          15s
frontend-7b8d9c5f6g-mno90   1/1     Running             0          17s
```

**Press Ctrl+C**

```bash
# Verify final state
kubectl get deployment frontend
```

**Expected Output:**
```
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
frontend   4/4     4            4           6m
```

### **11.7 Test Deletion**

```bash
# Delete the VisitorApp
kubectl delete visitorapp visitorapp-sample
```

**Expected Output:**
```
visitorapp.app.example.com "visitorapp-sample" deleted
```

```bash
# Watch resources being cleaned up
kubectl get all
```

**Expected Output (after a few seconds):**
```
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.245.0.1   <none>        443/TCP   1h
```

**All managed resources should be gone!**

### **11.8 Create Multiple Instances**

```bash
# Create first instance
cat <<EOF | kubectl apply -f -
apiVersion: app.example.com/v1
kind: VisitorApp
metadata:
  name: visitors-prod
spec:
  size: 3
  title: "Production Visitors"
EOF
```

**Expected Output:**
```
visitorapp.app.example.com/visitors-prod created
```

```bash
# Create second instance
cat <<EOF | kubectl apply -f -
apiVersion: app.example.com/v1
kind: VisitorApp
metadata:
  name: visitors-dev
spec:
  size: 1
  title: "Development Visitors"
EOF
```

**Expected Output:**
```
visitorapp.app.example.com/visitors-dev created
```

```bash
# View both
kubectl get visitorapps
```

**Expected Output:**
```
NAME            AGE
visitors-prod   1m
visitors-dev    30s
```

```bash
# View all resources
kubectl get all
```

**Expected Output (should show resources for BOTH apps):**
```
NAME                                 READY   STATUS    RESTARTS   AGE
pod/mysql-backend-5d6f7c9d8f-abc12   1/1     Running   0          1m
pod/frontend-7b8d9c5f6g-def34        1/1     Running   0          1m
pod/frontend-7b8d9c5f6g-ghi56        1/1     Running   0          1m
pod/frontend-7b8d9c5f6g-jkl78        1/1     Running   0          1m
pod/mysql-backend-8e7g8d0e9g-pqr90   1/1     Running   0          30s
pod/frontend-9f8h9e1f0h-stu12        1/1     Running   0          30s

NAME                          TYPE           CLUSTER-IP       EXTERNAL-IP       PORT(S)        AGE
service/kubernetes            ClusterIP      10.245.0.1       <none>            443/TCP        2h
service/mysql-service         ClusterIP      None             <none>            3306/TCP       1m
service/frontend-service      LoadBalancer   10.245.123.45    174.138.45.67     80:30123/TCP   1m
service/mysql-service         ClusterIP      None             <none>            3306/TCP       30s
service/frontend-service      LoadBalancer   10.245.234.56    174.138.98.76     80:31456/TCP   30s
...
```

**✅ Success! Your operator is managing multiple application instances!**

---

## **Step 12: Troubleshooting**

### **Common Issues and Solutions**

#### **Issue 1: Operator Pod Not Starting**

**Symptoms:**
```bash
kubectl get pods -n visitor-operator-system
```
```
NAME                                                       READY   STATUS             RESTARTS   AGE
visitor-operator-controller-manager-5d6f7c9d8f-abc12      0/2     ImagePullBackOff   0          2m
```

**Solution:**
```bash
# Check pod logs
kubectl describe pod -n visitor-operator-system <pod-name>

# Common causes:
# 1. Image doesn't exist in Docker Hub
# 2. Image is private (need to create imagePullSecrets)
# 3. Wrong image name

# Verify image exists
docker pull yourdockerusername/visitor-operator:v1.0.0

# If image is private, create secret:
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=yourdockerusername \
  --docker-password=yourpassword \
  --docker-email=your@email.com \
  -n visitor-operator-system

# Add to deployment
kubectl patch deployment visitor-operator-controller-manager \
  -n visitor-operator-system \
  -p '{"spec":{"template":{"spec":{"imagePullSecrets":[{"name":"regcred"}]}}}}'
```

#### **Issue 2: CRD Not Found**

**Symptoms:**
```bash
kubectl apply -f config/samples/app_v1_visitorapp.yaml
```
```
error: unable to recognize "config/samples/app_v1_visitorapp.yaml": no matches for kind "VisitorApp" in version "app.example.com/v1"
```

**Solution:**
```bash
# Reinstall CRDs
make install

# Or manually apply
kubectl apply -f config/crd/bases/app.example.com_visitorapps.yaml

# Verify CRD exists
kubectl get crds | grep visitorapp
```

#### **Issue 3: LoadBalancer Stuck in Pending**

**Symptoms:**
```bash
kubectl get service frontend-service
```
```
NAME               TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
frontend-service   LoadBalancer   10.245.123.45    <pending>     80:30123/TCP   10m
```

**Solution:**
```bash
# Check if DigitalOcean has load balancer quota
doctl compute load-balancer list

# Check service events
kubectl describe service frontend-service

# Common causes in DigitalOcean:
# 1. Region doesn't support load balancers
# 2. Account doesn't have load balancer enabled
# 3. Quota exceeded

# Temporary workaround - use NodePort
kubectl patch service frontend-service -p '{"spec":{"type":"NodePort"}}'

# Get NodePort
kubectl get service frontend-service

# Access via node IP:nodeport
kubectl get nodes -o wide
```

#### **Issue 4: Pods Not Starting**

**Symptoms:**
```bash
kubectl get pods
```
```
NAME                             READY   STATUS             RESTARTS   AGE
mysql-backend-5d6f7c9d8f-abc12   0/1     CrashLoopBackOff   5          5m
```

**Solution:**
```bash
# Check pod logs
kubectl logs mysql-backend-5d6f7c9d8f-abc12

# Check pod events
kubectl describe pod mysql-backend-5d6f7c9d8f-abc12

# Common causes:
# 1. Image doesn't exist
# 2. Resource limits too low
# 3. Environment variables wrong
# 4. Volume mount issues

# Check image
docker pull mysql:5.7

# Check resource usage
kubectl top pods
```

#### **Issue 5: Application Not Accessible**

**Symptoms:**
```bash
curl http://174.138.45.67
```
```
curl: (7) Failed to connect to 174.138.45.67 port 80: Connection refused
```

**Solution:**
```bash
# Verify service has external IP
kubectl get service frontend-service

# Check if pods are running
kubectl get pods -l tier=frontend

# Check pod logs
kubectl logs -l tier=frontend

# Port-forward for testing
kubectl port-forward service/frontend-service 8080:80

# Access at http://localhost:8080

# Check firewall rules in DigitalOcean
# Go to Networking > Firewalls
# Ensure port 80 is open
```

#### **Issue 6: Operator Not Reconciling**

**Symptoms:**
- Creating VisitorApp doesn't create resources
- No log messages in operator

**Solution:**
```bash
# Check operator is running
kubectl get pods -n visitor-operator-system

# Check operator logs for errors
kubectl logs -n visitor-operator-system deployment/visitor-operator-controller-manager -c manager

# Check RBAC permissions
kubectl auth can-i create deployments --as=system:serviceaccount:visitor-operator-system:visitor-operator-controller-manager

# Restart operator
kubectl rollout restart deployment -n visitor-operator-system visitor-operator-controller-manager
```

### **Useful Debugging Commands**

```bash
# Get all resources in all namespaces
kubectl get all -A

# Describe a resource
kubectl describe <resource-type> <resource-name>

# Get pod logs
kubectl logs <pod-name>

# Get previous pod logs (if restarted)
kubectl logs <pod-name> --previous

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port forward to test connectivity
kubectl port-forward <pod-name> 8080:8000

# View operator logs in real-time
kubectl logs -n visitor-operator-system deployment/visitor-operator-controller-manager -c manager -f

# Check API resources
kubectl api-resources | grep visitor

# Check cluster events
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top nodes
kubectl top pods
```

---

## **Cleanup**

### **Delete All Resources**

```bash
# Delete VisitorApp instances
kubectl delete visitorapps --all

# Wait for resources to be cleaned up
kubectl get all

# Uninstall operator
make undeploy

# Delete CRDs
make uninstall

# Verify cleanup
kubectl get all -A
```

### **Delete DigitalOcean Cluster**

**Via Web UI:**
1. Go to https://cloud.digitalocean.com/kubernetes
2. Click on your cluster name
3. Click "Settings" tab
4. Scroll to "Destroy"
5. Click "Destroy" button
6. Type cluster name to confirm
7. Click "Destroy Cluster"

**Via CLI:**
```bash
# List clusters
doctl kubernetes cluster list

# Delete cluster
doctl kubernetes cluster delete visitor-operator-cluster
```

**Confirm:**
```
Warning: Are you sure you want to delete this Kubernetes cluster? (y/N) 
```
**Type:** `y`

**Expected Output:**
```
Notice: Cluster deleted, but load balancers may still exist. Check load balancer list for more info.
```

**Delete any remaining load balancers:**
```bash
doctl compute load-balancer list
doctl compute load-balancer delete <load-balancer-id>
```

---

## **Next Steps**

Congratulations! You've successfully built and deployed a Kubernetes operator on DigitalOcean! 🎉

### **What You Learned**

✅ Set up DigitalOcean Kubernetes cluster  
✅ Install operator development tools  
✅ Create custom resources (CRDs)  
✅ Implement controller reconciliation logic  
✅ Test operator locally  
✅ Build and push container images  
✅ Deploy operator to production  
✅ Manage multiple application instances  
✅ Troubleshoot common issues  

### **Enhancements You Can Make**

1. **Add Finalizers** - Proper cleanup when VisitorApp is deleted
2. **Add Status Conditions** - Better status reporting
3. **Add Webhooks** - Validation and mutation
4. **Add Metrics** - Prometheus metrics for monitoring
5. **Add Tests** - Unit and integration tests
6. **Add CI/CD** - Automated builds and deployments
7. **Add OLM Bundle** - Package for OperatorHub
8. **Add Documentation** - Better README and examples

### **Resources**

- **Operator SDK Docs**: https://sdk.operatorframework.io/
- **Kubebuilder Book**: https://book.kubebuilder.io/
- **DigitalOcean Docs**: https://docs.digitalocean.com/products/kubernetes/
- **Sample Operators**: https://github.com/operator-framework/awesome-operators

---

## **Summary**

This guide walked you through the complete process of creating a Kubernetes operator from scratch on DigitalOcean. You now have a working operator that can manage complex application deployments, handle scaling, and maintain the desired state of your applications.

The operator pattern is powerful for:
- Automating application management
- Encoding operational knowledge
- Extending Kubernetes capabilities
- Building cloud-native applications

Keep building and happy operating! 🚀
