ext Direction : Spin K8s Self Managed Cluster on GCP

1. Set Project in gcloud

gcloud config set project <myProject>


2. Set the zone property in the compute section

gcloud config set compute/zone us-east1-b


3. Create the VPC

gcloud compute networks create k8s-cluster --subnet-mode custom


4. Create the k8s-nodes subnet in the k8s-cluster VPC network

    gcloud compute networks subnets create k8s-nodes \
      --network k8s-cluster \
      --range 10.240.0.0/24


5. Create a firewall rule that allows internal communication across TCP, UDP, ICMP and IP in IP.

    gcloud compute firewall-rules create k8s-cluster-allow-internal \
      --allow tcp,udp,icmp,ipip \
      --network k8s-cluster \
      --source-ranges 10.240.0.0/24


6. Create a firewall rule that allows external SSH, ICMP, and HTTPS

    gcloud compute firewall-rules create k8s-cluster-allow-external \
      --allow tcp:22,tcp:6443,icmp \
      --network k8s-cluster \
      --source-ranges 0.0.0.0/0


7. Create the controller VM (Master Node)

    gcloud compute instances create master-node \
        --async \
        --boot-disk-size 200GB \
        --can-ip-forward \
        --image-family ubuntu-1804-lts \
        --image-project ubuntu-os-cloud \
        --machine-type n1-standard-2 \
        --private-network-ip 10.240.0.11 \
        --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
        --subnet k8s-nodes \
        --zone us-east1-b \
        --tags k8s-cluster,master-node,controller


8. Create Two worker VMs

    for i in 0 1; do
      gcloud compute instances create workernode-${i} \
        --async \
        --boot-disk-size 200GB \
        --can-ip-forward \
        --image-family ubuntu-1804-lts \
        --image-project ubuntu-os-cloud \
        --machine-type n1-standard-2 \
        --private-network-ip 10.240.0.2${i} \
        --scopes compute-rw,storage-ro,service-management,service-control,logging-write,monitoring \
        --subnet k8s-nodes \
        --zone us-east1-b \
        --tags k8s-cluster,worker
    done


9. Install Docker on the controller VM and each worker VM.

    sudo apt update
    sudo apt install -y docker.io 
    sudo systemctl enable docker.service
    sudo apt install -y apt-transport-https curl


10. Install kubeadm, kubelet, and kubectl on the controller VM and each worker VM.

    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
    deb https://apt.kubernetes.io/ kubernetes-xenial main
    EOF
    sudo apt-get update
    sudo apt-get install -y kubelet kubeadm kubectl
    sudo apt-mark hold kubelet kubeadm kubectl


11. Create the controller node of a new cluster. On the controller VM, execute:

sudo kubeadm init --pod-network-cidr 192.168.0.0/16


12. To set up kubectl for the ubuntu user, run:

    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config


13. On Worker Nodes Execute the Join Command


14. Verify the Cluster Status

kubectl get nodes


15. On the controller, install Calico from the manifest:

curl https://docs.projectcalico.org/manifests/calico.yaml -O

kubectl apply -f calico.yaml 