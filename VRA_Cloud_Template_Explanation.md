# VMware Aria Automation Cloud Template - Code Explanation
## 2-Tier CAS Demo Application

---

## **Template Overview**

This Cloud Assembly template deploys a **2-tier web application** consisting of:
- **Frontend Tier**: Nginx web servers serving an Angular application
- **API Tier**: Python Flask API backend
- **Load Balancer**: (Optional) For high-availability frontend

The template is **multi-cloud capable** and can deploy to AWS, vSphere, Azure, VMC, or GCP.

---

## **Template Metadata**

```yaml
name: 2-Tier CAS Demo Application
version: 4
formatVersion: 1
```

| Field | Description |
|-------|-------------|
| `name` | Display name of the template |
| `version` | Template version (incremented with changes) |
| `formatVersion` | Cloud Assembly YAML format version |

---

## **Section 1: Inputs**

Inputs are parameters that users provide at deployment time.

### **Input: environment**

```yaml
inputs:
  environment:
    type: string
    enum:
      - AWS
      - vSphere
      - Azure
      - VMC
      - GCP
    default: vSphere
```

**What it does:**
- Presents a dropdown menu to select deployment target
- **enum**: Restricts choices to 5 cloud platforms
- **default**: Pre-selects vSphere if user doesn't choose
- **Used for**: Tagging resources to route them to correct cloud (via constraints)

**User sees:** Dropdown with 5 options

---

### **Input: sshKey**

```yaml
  sshKey:
    type: string
    encrypted: true
```

**What it does:**
- Accepts SSH public key for remote access to VMs
- **encrypted: true**: Masks the input in UI and logs for security
- **Used for**: SSH authentication to deployed VMs

**User sees:** Text field with masked input

**Example value:**
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC8... user@host
```

---

### **Input: envsize**

```yaml
  envsize:
    type: string
    enum:
      - Small
      - Large
```

**What it does:**
- Lets user choose deployment size
- **Small**: 1 frontend VM, no load balancer
- **Large**: 2 frontend VMs with load balancer
- **Used for**: Conditional resource creation using `count` property

**User sees:** Dropdown with 2 options

---

## **Section 2: Resources**

Resources are the infrastructure components to be deployed.

---

### **Resource 1: Cloud_LoadBalancer_1**

```yaml
resources:
  Cloud_LoadBalancer_1:
    type: Cloud.LoadBalancer
    properties:
      count: '${input.envsize == "Small" ? 0 : 1}'
```

#### **Conditional Deployment**

**Expression breakdown:**
```javascript
${input.envsize == "Small" ? 0 : 1}
```

| Condition | Result | What Happens |
|-----------|--------|--------------|
| envsize == "Small" | count: 0 | Load balancer NOT created |
| envsize == "Large" | count: 1 | Load balancer IS created |

This uses a **ternary operator** (condition ? if_true : if_false)

---

#### **Load Balancer Configuration**

```yaml
      name: lb
      routes:
        - port: '80'
          protocol: http
          instancePort: '80'
          instanceProtocol: http
```

**What it does:**
- **name**: Load balancer is named "lb"
- **routes**: Defines traffic routing rules
  - **port**: Load balancer listens on port 80
  - **protocol**: Uses HTTP protocol
  - **instancePort**: Forwards to port 80 on backend VMs
  - **instanceProtocol**: Uses HTTP to backend

**Traffic flow:**
```
User → Load Balancer:80 (HTTP) → Frontend VM:80 (HTTP)
```

---

#### **Network and Backend Configuration**

```yaml
      network: ${resource.Cloud_Network_1.name}
      instances:
        - ${resource.frontend.id}
      internetFacing: false
```

**What it does:**
- **network**: Attaches load balancer to the network defined later
  - `${resource.Cloud_Network_1.name}` - References network resource
- **instances**: Backend pool of VMs to load balance
  - `${resource.frontend.id}` - References frontend VM(s)
- **internetFacing: false**: Internal load balancer (not public)

**Dependency chain:**
```
Load Balancer depends on → Network + Frontend VMs
```

---

### **Resource 2: frontend (Web Tier)**

```yaml
  frontend:
    type: Cloud.Machine
    properties:
      folderName: '${input.environment == "VMC" ? "Workload" : ""}'
```

#### **Conditional Folder Placement**

**Expression:**
```javascript
${input.environment == "VMC" ? "Workload" : ""}
```

| Environment | Folder Name | Why |
|-------------|-------------|-----|
| VMC | "Workload" | VMC requires VMs in "Workload" folder |
| All others | "" (empty) | Uses default folder location |

---

#### **VM Sizing and Count**

```yaml
      image: ubuntu
      flavor: medium
      count: '${input.envsize == "Small" ? 1 : 2}'
```

**What it does:**
- **image**: Uses Ubuntu OS image (mapped in Cloud Assembly)
- **flavor**: Medium VM size (CPU/RAM defined in flavor mapping)
- **count**: Conditional VM count
  - Small environment: 1 frontend VM
  - Large environment: 2 frontend VMs for HA

---

#### **SSH Access Configuration**

```yaml
      remoteAccess:
        authentication: publicPrivateKey
        sshKey: ${input.sshKey}
```

**What it does:**
- **authentication**: Uses SSH key-based auth (not password)
- **sshKey**: Injects the user-provided SSH public key
- **Result**: User can SSH as: `ssh ubuntu@<vm-ip>`

---

#### **Cloud-Init Bootstrap Script**

The `cloudConfig` section contains cloud-init commands that run on VM first boot.

```yaml
      cloudConfig: |
        runcmd:
```

**What is runcmd?**
- Cloud-init directive that runs shell commands during VM initialization
- Commands execute in order, sequentially
- VM is "ready" after all commands complete

---

#### **Frontend Bootstrap - Step by Step**

**Step 1: Echo API server IP**
```bash
- echo ${resource.apitier.networks[0].address}
```
- Prints API tier IP address to console/logs
- `${resource.apitier.networks[0].address}` - Gets first network IP of API VM

---

**Step 2: Install Nginx**
```bash
- apt install -y nginx
```
- Installs Nginx web server
- `-y` flag: Auto-confirms installation prompts

---

**Step 3: Clone Frontend Application**
```bash
- /usr/bin/git clone https://github.com/codyde/frontend-demoapp /tmp/cas-demo-application
```
- Downloads Angular frontend code from GitHub
- Saves to `/tmp/cas-demo-application`

---

**Step 4: Clean Nginx Defaults**
```bash
- /bin/rm -rf /etc/nginx/conf.d/*
- /bin/rm -rf /usr/share/nginx/html/*
```
- Removes default Nginx configuration files
- Removes default HTML files
- Prepares for custom application deployment

---

**Step 5: Install Node.js & Angular CLI**
```bash
- /usr/bin/curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
- /usr/bin/apt install nodejs -y
- /usr/bin/npm install -g @angular/cli
```
- Downloads and installs Node.js 10.x repository
- Installs Node.js and npm
- Installs Angular CLI globally (`@angular/cli`)

---

**Step 6: Build Angular Application**
```bash
- cd /tmp/cas-demo-application && /usr/bin/npm install
- /usr/bin/ng build --prod
```
- `npm install`: Downloads application dependencies
- `ng build --prod`: Compiles Angular app for production
  - Creates optimized, minified JavaScript bundles
  - Output goes to `/tmp/cas-demo-application/dist/cas-demo-app/`

---

**Step 7: Deploy Application to Nginx**
```bash
- /bin/cp -R /tmp/cas-demo-application/dist/cas-demo-app/* /usr/share/nginx/html/
```
- Copies compiled Angular files to Nginx web root
- Now accessible at `http://<vm-ip>/`

---

**Step 8: Configure Nginx**
```bash
- /bin/sed -i "s@root /var/www/html@root /usr/share/nginx/html@" /etc/nginx/sites-available/default
- /bin/cp /tmp/cas-demo-application/nginx/default.conf /etc/nginx/conf.d/default.conf
```
- Updates default Nginx root directory
- Copies custom Nginx configuration

---

**Step 9: Configure API Backend Proxy**
```bash
- /bin/sed -i "s@pyapi@${resource.apitier.networks[0].address}@" /etc/nginx/conf.d/default.conf
```

**Critical Step!** This configures the API proxy.

**Before:**
```nginx
proxy_pass http://pyapi/api/;
```

**After (example):**
```nginx
proxy_pass http://192.168.1.50/api/;
```

- Replaces placeholder "pyapi" with actual API tier IP
- Frontend can now communicate with backend API
- Uses `${resource.apitier.networks[0].address}` for dynamic IP injection

---

**Step 10: Finalize Nginx Configuration**
```bash
- /bin/rm -rf /etc/nginx/sites-available/default
- /bin/sed -i "s@include /etc/nginx/sites-enabled/*@# include /etc/nginx/sites-enabled/*@" /etc/nginx/nginx.conf
- /bin/systemctl restart nginx
```
- Removes default site configuration
- Comments out sites-enabled include (using conf.d instead)
- Restarts Nginx to apply all changes

---

#### **Placement Constraints**

```yaml
      constraints:
        - tag: ${"env:" + to_lower(input.environment)}
```

**What it does:**
- **Constraints**: Rules that determine WHERE VMs are placed
- **tag**: Matches cloud zones with specific tags

**Expression breakdown:**
```javascript
${"env:" + to_lower(input.environment)}
```

**Example transformations:**

| User Input | Constraint Tag |
|-----------|---------------|
| vSphere | `env:vsphere` |
| AWS | `env:aws` |
| Azure | `env:azure` |
| VMC | `env:vmc` |

**How it works:**
1. `to_lower(input.environment)` - Converts "vSphere" to "vsphere"
2. Concatenates "env:" prefix
3. Result: `env:vsphere`
4. Cloud Assembly looks for cloud zones tagged with `env:vsphere`
5. Deploys VM to matching zone

**In Cloud Assembly:**
- Cloud Zones must be tagged: `env:vsphere`, `env:aws`, etc.
- This enables multi-cloud deployments with single template

---

#### **Network Assignment**

```yaml
      networks:
        - name: ${resource.Cloud_Network_1.name}
```

**What it does:**
- Attaches VM to the network defined later
- Uses dynamic reference to network resource
- VM gets IP from this network's subnet

---

### **Resource 3: apitier (API Backend)**

```yaml
  apitier:
    type: Cloud.Machine
    properties:
      folderName: '${input.environment == "VMC" ? "Workload" : ""}'
      image: ubuntu
      flavor: small
```

**Differences from frontend:**
- **flavor: small** - Smaller VM (less CPU/RAM)
- **No count property** - Always deploys exactly 1 API server
- **No load balancer** - Single backend instance

---

#### **API Tier Bootstrap Script**

```yaml
      cloudConfig: |
        runcmd:
```

**Step 1: Enable Universe Repository**
```bash
- add-apt-repository universe
- apt update -y
```
- Enables Ubuntu Universe repository (more packages)
- Updates package lists

---

**Step 2: Install Python Dependencies**
```bash
- apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools supervisor
```

**Packages installed:**
- `python3-pip` - Python package manager
- `python3-dev` - Python development headers
- `build-essential` - C/C++ compilers (for native extensions)
- `libssl-dev` - SSL/TLS library
- `libffi-dev` - Foreign Function Interface library
- `python3-setuptools` - Python package tools
- `supervisor` - Process manager for keeping Flask app running

---

**Step 3: Install Python Frameworks**
```bash
- pip3 install gunicorn flask flask_cors requests
```

**What is installed:**
- **gunicorn** - Production WSGI HTTP server for Python
- **flask** - Web framework for building APIs
- **flask_cors** - Cross-Origin Resource Sharing support
- **requests** - HTTP library for making API calls

---

**Step 4: Configure Firewall**
```bash
- ufw allow 80
```
- Opens port 80 in Ubuntu firewall
- Allows HTTP traffic to Flask application

---

**Step 5: Clone API Application**
```bash
- git clone https://github.com/codyde/api-tier-demoapp /app
```
- Downloads Flask API code from GitHub
- Saves to `/app` directory

---

**Step 6: Configure Supervisor**
```bash
- cp /app/app.conf /etc/supervisor/conf.d/app.conf
- supervisorctl reread
- systemctl restart supervisor
- supervisorctl status
```

**What this does:**
- Copies supervisor configuration for Flask app
- **supervisorctl reread** - Loads new configuration
- **systemctl restart supervisor** - Restarts supervisor service
- **supervisorctl status** - Verifies app is running

**Supervisor ensures:**
- Flask app starts automatically on boot
- Restarts app if it crashes
- Manages logging

---

#### **API Tier Constraints**

```yaml
      constraints:
        - tag: ${"env:" + to_lower(input.environment)}
      networks:
        - name: ${resource.Cloud_Network_1.name}
```

**Same as frontend:**
- Deploys to same cloud zone
- Attached to same network
- Ensures frontend and backend are co-located

---

### **Resource 4: Cloud_Network_1**

```yaml
  Cloud_Network_1:
    type: Cloud.Network
    properties:
      name: Default
      networkType: existing
      constraints:
        - tag: ${"env:" + to_lower(input.environment)}
```

#### **Network Configuration**

**What it does:**
- **type: Cloud.Network** - Network resource
- **name: "Default"** - Looks for network named "Default"
- **networkType: existing** - Uses pre-existing network (doesn't create new)
- **constraints** - Finds network in selected cloud zone

**How it works:**
1. User selects environment (e.g., "vSphere")
2. Constraint becomes `env:vsphere`
3. Cloud Assembly finds existing network with tag `env:vsphere`
4. VMs attach to that network

**Network must exist and be tagged correctly in Cloud Assembly!**

---

## **Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────┐
│                      USER REQUEST                           │
│                           ↓                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Cloud_LoadBalancer_1 (Large only)          │    │
│  │              Port 80 → Port 80                     │    │
│  └───────────────────────┬────────────────────────────┘    │
│                          │                                  │
│              ┌───────────┴────────────┐                    │
│              ↓                        ↓                     │
│  ┌─────────────────────┐   ┌─────────────────────┐        │
│  │   frontend (VM 1)   │   │   frontend (VM 2)   │        │
│  │   Ubuntu + Nginx    │   │   Ubuntu + Nginx    │        │
│  │   Angular App       │   │   Angular App       │        │
│  │   Port 80           │   │   Port 80           │        │
│  └──────────┬──────────┘   └──────────┬──────────┘        │
│             │                          │                    │
│             └───────────┬──────────────┘                    │
│                         ↓                                   │
│             /api/* requests proxied to                      │
│                         ↓                                   │
│              ┌──────────────────────┐                       │
│              │   apitier (VM 1)     │                       │
│              │   Ubuntu             │                       │
│              │   Python Flask API   │                       │
│              │   Gunicorn + Supervisor                      │
│              │   Port 80            │                       │
│              └──────────────────────┘                       │
│                                                              │
│              All VMs on Cloud_Network_1                     │
└──────────────────────────────────────────────────────────────┘
```

---

## **Deployment Flow**

### **Step 1: User Input**
1. User requests deployment
2. Selects:
   - Environment: vSphere
   - Size: Large
   - SSH Key: (provides public key)

### **Step 2: Resource Resolution**
1. Cloud Assembly processes template
2. Evaluates all expressions:
   - `count: ${input.envsize == "Small" ? 0 : 1}` → 1 (Load balancer created)
   - `count: ${input.envsize == "Small" ? 1 : 2}` → 2 (Two frontend VMs)
   - Constraint tags → `env:vsphere`

### **Step 3: Resource Provisioning**

**Order matters! Dependencies:**
```
1. Cloud_Network_1 (network created first)
   ↓
2. apitier (API VM needs network)
   ↓
3. frontend (Frontend needs API IP for cloud-init)
   ↓
4. Cloud_LoadBalancer_1 (Load balancer needs frontend VMs)
```

### **Step 4: VM Initialization**

**API Tier (apitier):**
1. VM powers on
2. Cloud-init runs bootstrap script
3. Installs Python, Flask, Gunicorn
4. Clones API code
5. Starts Flask app via Supervisor
6. VM reports "ready" to Cloud Assembly

**Frontend Tier (frontend):**
1. VM powers on
2. Cloud-init runs bootstrap script
3. Waits for API tier IP: `${resource.apitier.networks[0].address}`
4. Installs Nginx, Node.js, Angular CLI
5. Builds Angular application
6. Configures Nginx to proxy /api/* to API tier IP
7. Starts Nginx
8. VM reports "ready"

**Load Balancer:**
1. Waits for both frontend VMs to be "ready"
2. Creates load balancer
3. Adds frontend VMs to backend pool
4. Starts routing traffic

### **Step 5: Application Ready**
- User can access: `http://<load-balancer-ip>/`
- Frontend serves Angular app
- API calls proxied to backend: `http://<load-balancer-ip>/api/*`

---

## **Key VMware Aria Concepts Used**

### **1. Expressions (Cloud Assembly Template Language)**

**Syntax:** `${...}`

**Examples:**
```yaml
${input.environment}                    # Variable reference
${input.envsize == "Small" ? 0 : 1}    # Ternary operator
${"env:" + to_lower(input.environment)} # String concatenation
${resource.apitier.networks[0].address} # Resource reference
```

---

### **2. Resource References**

**Syntax:** `${resource.RESOURCE_NAME.property}`

**Dependencies created automatically:**
```yaml
network: ${resource.Cloud_Network_1.name}
# Frontend depends on Cloud_Network_1 existing first
```

**Cross-resource references:**
```yaml
${resource.apitier.networks[0].address}
# Frontend depends on apitier having an IP address
```

---

### **3. Constraints & Tags**

**Purpose:** Intelligent placement of resources

**Example:**
```yaml
constraints:
  - tag: env:vsphere
```

**Matches cloud zones/resources tagged:**
- `env:vsphere`
- `env:aws`
- `env:azure`

**Benefits:**
- Single template works across multiple clouds
- Resources automatically placed in correct infrastructure
- Enables governance and policy enforcement

---

### **4. Conditional Resources**

**count property:**
```yaml
count: '${input.envsize == "Small" ? 0 : 1}'
```

| Count | Result |
|-------|--------|
| 0 | Resource not created |
| 1 | One instance created |
| 2+ | Multiple instances created |

---

### **5. Cloud-Init Integration**

**cloudConfig property:**
- Industry-standard VM initialization framework
- Runs during first boot
- Supports multiple directives:
  - `runcmd` - Shell commands
  - `packages` - Package installation
  - `users` - User creation
  - `write_files` - File creation

**In this template:**
- Installs software
- Configures services
- Deploys applications
- All automated, no manual steps

---

## **Advanced Features Explained**

### **Dynamic IP Injection**

```yaml
- /bin/sed -i "s@pyapi@${resource.apitier.networks[0].address}@" /etc/nginx/conf.d/default.conf
```

**Problem:** Frontend needs to know API IP, but IP is dynamic
**Solution:** Cloud Assembly injects actual IP at deployment time

**Process:**
1. API tier gets IP: 192.168.1.50
2. Cloud Assembly evaluates: `${resource.apitier.networks[0].address}`
3. Returns: "192.168.1.50"
4. sed command replaces "pyapi" with "192.168.1.50"
5. Frontend can now communicate with backend

---

### **Multi-Cloud Portability**

**Same template works on 5 clouds!**

**How?**
1. **Abstraction:** Uses generic resource types
   - `Cloud.Machine` (not AWS::EC2::Instance)
   - `Cloud.Network` (not vSphere::PortGroup)
   - `Cloud.LoadBalancer` (not AWS::ELB)

2. **Constraints:** Routes to correct infrastructure
   - `tag: env:aws` → Deploys to AWS
   - `tag: env:vsphere` → Deploys to vSphere

3. **Image/Flavor Mapping:** (configured in Cloud Assembly)
   - "ubuntu" → maps to Ubuntu AMI in AWS
   - "ubuntu" → maps to Ubuntu template in vSphere
   - "medium" → maps to t2.medium in AWS
   - "medium" → maps to 2 vCPU, 4GB RAM in vSphere

---

### **High Availability Architecture**

**Small Environment:**
- 1 frontend VM
- 1 API VM
- No load balancer
- Cost-effective for dev/test

**Large Environment:**
- 2 frontend VMs (redundancy)
- 1 API VM
- 1 load balancer (distributes traffic)
- High availability for production

**Scaling Strategy:**
- Frontend tier scales horizontally (add more VMs)
- API tier is single instance (could be enhanced for HA)
- Load balancer ensures no single point of failure

---

## **Potential Issues & Considerations**

### **Issue 1: Dependency Timing**

**Problem:**
```yaml
- echo ${resource.apitier.networks[0].address}
```

If API tier VM isn't ready yet, IP might not be available.

**Solution:** Cloud Assembly waits for dependencies to complete before proceeding.

---

### **Issue 2: Cloud-Init Failures**

If bootstrap script fails:
- VM powers on but application not installed
- Need to SSH in and troubleshoot
- Check: `/var/log/cloud-init-output.log`

**Best Practice:**
- Test cloud-init scripts separately
- Add error handling
- Use idempotent commands

---

### **Issue 3: Network Connectivity**

VMs need internet access for:
- `apt install` (package downloads)
- `git clone` (GitHub access)
- `npm install` (Node.js packages)

**Solution:** Ensure network has NAT/internet gateway configured

---

### **Issue 4: Single API Instance**

API tier has no redundancy:
- Single point of failure
- No load balancing
- No auto-scaling

**Enhancement:**
```yaml
apitier:
  count: '${input.envsize == "Small" ? 1 : 2}'
```

Then add API load balancer.

---

## **Summary**

### **What This Template Does**

1. ✅ Deploys 2-tier web application (Angular + Flask)
2. ✅ Supports 5 cloud platforms with single template
3. ✅ Offers 2 sizing options (Small/Large)
4. ✅ Fully automated deployment (no manual steps)
5. ✅ Includes optional load balancer for HA
6. ✅ Uses cloud-init for application installation
7. ✅ Implements dynamic service discovery (API IP injection)

### **Technologies Used**

| Layer | Technology |
|-------|-----------|
| **Frontend** | Angular, Nginx, Node.js |
| **Backend** | Python Flask, Gunicorn, Supervisor |
| **Infrastructure** | Ubuntu VMs, Load Balancer, Network |
| **Automation** | Cloud-init, Cloud Assembly |
| **Clouds** | AWS, vSphere, Azure, VMC, GCP |

### **Best Practices Demonstrated**

- ✅ Infrastructure as Code
- ✅ Multi-cloud abstraction
- ✅ Declarative configuration
- ✅ Automated provisioning
- ✅ Conditional deployment
- ✅ Dynamic configuration
- ✅ High availability (Large mode)

---

## **How to Use This Template**

### **Prerequisites**

1. **VMware Aria Automation** configured with:
   - Cloud zones tagged with `env:vsphere`, `env:aws`, etc.
   - Network tagged appropriately in each zone
   - Ubuntu image mappings configured
   - Flavor mappings (small, medium) defined

2. **Network Requirements:**
   - VMs need internet access for package downloads
   - GitHub access (ports 443, 22)
   - Internal VM-to-VM communication

3. **SSH Key:**
   - Generate SSH key pair: `ssh-keygen -t rsa`
   - Use public key (id_rsa.pub) in template

### **Deployment Steps**

1. Import template to Cloud Assembly
2. Publish template version
3. Share to Service Broker catalog
4. User requests deployment:
   - Selects environment
   - Chooses size
   - Provides SSH key
5. Click "Deploy"
6. Wait 5-10 minutes for completion
7. Access application at load balancer IP (Large) or frontend VM IP (Small)

### **Testing**

```bash
# Get deployment details
# Find frontend VM or load balancer IP

# Test frontend
curl http://<IP>/

# Test API (via frontend proxy)
curl http://<IP>/api/

# SSH to frontend
ssh ubuntu@<frontend-ip> -i ~/.ssh/id_rsa

# Check Nginx status
sudo systemctl status nginx

# View cloud-init logs
sudo cat /var/log/cloud-init-output.log
```

---

## **Conclusion**

This template demonstrates VMware Aria Automation's power for multi-cloud infrastructure automation. It combines:
- Declarative infrastructure definition
- Automated application deployment  
- Multi-cloud portability
- Conditional logic for flexible sizing
- Service discovery and dynamic configuration

It's an excellent reference for building production cloud templates!
