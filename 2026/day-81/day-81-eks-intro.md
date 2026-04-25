# Day 81 -- Introduction to Amazon EKS with Terraform

### Task 1: Understand EKS Architecture
Research and write notes on:

1. **What does "managed Kubernetes" mean?**
   - AWS manages the **control plane** (API server, etcd, scheduler, controller manager)
   - You manage the **data plane** (worker nodes where your pods run)
   - AWS handles control plane upgrades, patching, and high availability across multiple AZs

2. **EKS components:**
   - **EKS Control Plane** -- managed by AWS, runs in AWS-owned VPC, accessible via API endpoint
   - **Node Groups** -- EC2 instances that run your pods
     - **Managed Node Groups** -- AWS handles provisioning, scaling, and updates
     - **Self-Managed Nodes** -- you manage the EC2 instances yourself
     - **Fargate Profiles** -- serverless, no nodes to manage at all
   - **VPC and Networking** -- EKS runs inside your VPC with subnets across AZs
   - **IAM Integration** -- EKS uses IAM roles for cluster access and pod-level permissions (IRSA)

3. **EKS add-ons the AI-BankApp uses** (from `terraform/eks.tf`):
   - `coredns` -- DNS resolution inside the cluster
   - `kube-proxy` -- network routing for services
   - `vpc-cni` -- AWS VPC CNI plugin, assigns VPC IPs to pods
   - `eks-pod-identity-agent` -- enables pod-level IAM roles
   - `aws-ebs-csi-driver` -- allows pods to use EBS volumes (needed for MySQL and Ollama storage)
   - `metrics-server` -- enables `kubectl top` and HPA

---

### Task 2: Study the AI-BankApp Terraform Configuration
Clone the repo and examine the `terraform/` directory:

```bash
git clone -b feat/gitops https://github.com/TrainWithShubham/AI-BankApp-DevOps.git
cd AI-BankApp-DevOps/terraform
ls
```

```
argocd.tf           # ArgoCD Helm release
eks.tf              # EKS cluster + node group + IRSA
outputs.tf          # Cluster info and helper commands
provider.tf         # AWS + Helm providers, locals
terraform.tfvars    # Default variable values
variables.tf        # Input variables
vpc.tf              # VPC with public/private/intra subnets
```

**Study each file and understand what it provisions:**

**`variables.tf` and `terraform.tfvars`:**
```hcl
# The defaults:
aws_region         = "us-west-2"
cluster_name       = "bankapp-eks"
cluster_version    = "1.35"
node_instance_type = "t3.medium"
node_desired_count = 3
node_max_count     = 5
```

**`vpc.tf`** -- Networking foundation:
- Uses the `terraform-aws-modules/vpc/aws` module
- 3 Availability Zones with:
  - **Public subnets** (10.0.1-3.0/24) -- for load balancers, tagged with `kubernetes.io/role/elb`
  - **Private subnets** (10.0.4-6.0/24) -- for worker nodes, tagged with `kubernetes.io/role/internal-elb`
  - **Intra subnets** (10.0.7-9.0/24) -- for EKS control plane ENIs
- NAT Gateway enabled for outbound internet from private subnets

**`eks.tf`** -- The cluster itself:
- Uses the `terraform-aws-modules/eks/aws` module (version ~> 21.0)
- AL2023 AMI for nodes (Amazon Linux 2023)
- 3x `t3.medium` instances (min 3, max 5)
- All 6 EKS add-ons installed as cluster add-ons
- IRSA configured for the EBS CSI driver
- Public + private API endpoint access

**`argocd.tf`** -- ArgoCD via Helm:
- Installs ArgoCD using the `argo-cd` Helm chart
- Exposed as a LoadBalancer service
- Depends on the EKS module (created after the cluster is ready)

**`outputs.tf`** -- Helper commands:
- Outputs the `aws eks update-kubeconfig` command
- Outputs the ArgoCD initial password retrieval command

**Document:** Draw the architecture: VPC -> Subnets -> EKS Control Plane -> Node Group -> Pods
<img width="1520" height="922" alt="WhatsApp Image 2026-04-22 at 6 03 03 PM" src="https://github.com/user-attachments/assets/c11ec900-198b-4762-b157-1777629df64d" />

---

### Task 3: Provision the EKS Cluster
Make sure you have the required tools:
```bash
terraform --version    # >= 1.0
aws --version          # AWS CLI v2
kubectl version --client
helm version
```

Configure AWS credentials:
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-west-2), Output (json)

# Verify
aws sts get-caller-identity
```

Initialize and apply:
```bash
cd terraform

terraform init
terraform plan
```

Review the plan carefully. It will create:
- 1 VPC with 9 subnets, NAT gateway, internet gateway
- 1 EKS cluster with control plane
- 1 managed node group (3x t3.medium)
- 6 EKS add-ons
- IAM roles and policies for the cluster, nodes, and EBS CSI driver
- ArgoCD Helm release

```bash
terraform apply
```
<img width="1920" height="201" alt="Screenshot (1032)" src="https://github.com/user-attachments/assets/42cf4b19-4883-45e3-bfc1-977a7d12c7fd" />

This takes 15-20 minutes. While waiting, review the Terraform output for CloudFormation-like progress.

After completion, note the outputs:
```bash
terraform output
```
<img width="1920" height="530" alt="Screenshot (1033)" src="https://github.com/user-attachments/assets/0e1f3109-93cc-44b7-ad7e-073768d02bed" />

---

### Task 4: Connect to Your Cluster
Update kubeconfig using the Terraform output:
```bash
aws eks update-kubeconfig --name bankapp-eks --region us-west-2
```

Verify the connection:
```bash
# Check context
kubectl config current-context

# Cluster info
kubectl cluster-info

# List nodes
kubectl get nodes -o wide
```


You should see 3 nodes with status `Ready`, instance type `t3.medium`, spread across 3 AZs.
<img width="1920" height="572" alt="Screenshot (1034)" src="https://github.com/user-attachments/assets/0054b81e-84dc-4b73-a46f-46b9ce2f77db" />

Explore the cluster:
```bash
# System pods
kubectl get pods -n kube-system

# All the add-ons are running
kubectl get daemonsets -n kube-system

# EBS CSI driver
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-ebs-csi-driver

# Metrics server (enables kubectl top and HPA)
kubectl top nodes
```
<img width="1007" height="513" alt="Screenshot (1035)" src="https://github.com/user-attachments/assets/14e41f76-d53d-4ff7-a0fc-dbd245b92e64" />
<img width="1158" height="229" alt="Screenshot (1037)" src="https://github.com/user-attachments/assets/bda74faf-0e40-4c41-b0f2-52bed0842cc9" />
<img width="1920" height="586" alt="Screenshot (1036)" src="https://github.com/user-attachments/assets/5b103cca-9d09-4ffe-ae20-d61341a9c6f5" />

Check ArgoCD is running:
```bash
kubectl get pods -n argocd
kubectl get svc -n argocd
```
<img width="1920" height="640" alt="Screenshot (1038)" src="https://github.com/user-attachments/assets/25f250ce-7ea2-4c32-a1d1-93e33fd1f7ea" />

Get the ArgoCD admin password:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Get the ArgoCD LoadBalancer URL:
```bash
kubectl get svc -n argocd argocd-server -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```
<img width="1920" height="593" alt="Screenshot (1040)" src="https://github.com/user-attachments/assets/c94be16c-73e3-4c8d-b9b3-bf7e192207be" />


Open the URL in your browser and log in with `admin` and the password from above. You will use ArgoCD on Days 84-86.
<img width="1920" height="1030" alt="Screenshot (1039)" src="https://github.com/user-attachments/assets/74d3a8c0-8edc-4c19-928a-b59bcfaadf3f" />

---

### Task 5: Deploy the AI-BankApp Manually (Before ArgoCD)
Before setting up GitOps, deploy the app manually to validate the cluster works.

Apply the raw manifests from the `k8s/` directory:
```bash
cd ../  # Back to the repo root

kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/pv.yml
kubectl apply -f k8s/pvc.yml
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secrets.yml
kubectl apply -f k8s/mysql-deployment.yml
kubectl apply -f k8s/service.yml
kubectl apply -f k8s/ollama-deployment.yml
kubectl apply -f k8s/bankapp-deployment.yml
kubectl apply -f k8s/hpa.yml
```

Watch the pods come up:
```bash
kubectl get pods -n bankapp -w
```
<img width="991" height="297" alt="Screenshot (1041)" src="https://github.com/user-attachments/assets/ab203e4f-1884-492e-928b-0ecfecc17704" />

The startup order is:
1. MySQL starts and becomes healthy (15-30 seconds)
2. Ollama starts and pulls the TinyLlama model (2-5 minutes)
3. BankApp init containers wait for both, then the app starts (30-60 seconds after dependencies)

Check PVCs are bound to EBS volumes:
```bash
kubectl get pvc -n bankapp
kubectl get pv
```
<img width="1920" height="334" alt="Screenshot (1042)" src="https://github.com/user-attachments/assets/bd1fa13d-41fb-43e8-a0d7-4b15b3e42462" />

You should see 5Gi and 10Gi EBS volumes in the correct AZs.

Once all pods are running, access the app:
```bash
kubectl port-forward svc/bankapp-service -n bankapp 8080:8080
```
<img width="1920" height="1016" alt="Screenshot (1045)" src="https://github.com/user-attachments/assets/6c9b2452-6268-4bc8-b830-4254ef47c99f" />
<img width="1920" height="1021" alt="Screenshot (1043)" src="https://github.com/user-attachments/assets/822b50c0-0869-4f5a-82b0-eaf5d8354bf4" />
<img width="1920" height="1020" alt="Screenshot (1047)" src="https://github.com/user-attachments/assets/43daaa5e-5bce-4932-a368-3ed32782f8f6" />
<img width="1920" height="1016" alt="Screenshot (1046)" src="https://github.com/user-attachments/assets/36b6949e-e806-46b7-8490-126e5af01ed8" />

Open `http://localhost:8080` -- you should see the AI-BankApp login page. Register an account, log in, and try the AI chatbot.

**Verify the HPA:**
```bash
kubectl get hpa -n bankapp
```
<img width="1267" height="173" alt="Screenshot (1048)" src="https://github.com/user-attachments/assets/576372c0-42a5-4511-9517-43cbf3ccb5a5" />

---

### Task 6: Understand EKS Costs and Clean Up Strategy
EKS is not free. The AI-BankApp cluster costs:

| Component | Cost (approximate) |
|-----------|-------------------|
| EKS Control Plane | $0.10/hr (~$73/month) |
| t3.medium nodes (3x) | ~$0.042/hr each (~$91/month total) |
| NAT Gateway | ~$0.045/hr + data transfer (~$33/month) |
| EBS volumes (15Gi total) | ~$1.50/month |
| LoadBalancer (ArgoCD) | ~$0.025/hr (~$18/month) |
| **Total for this lab** | **~$220/month (~$7/day)** |

**Important:** Do NOT leave the cluster running when you are not using it.

Delete the BankApp workload (keep the cluster for Days 82-83):
```bash
kubectl delete -f k8s/hpa.yml
kubectl delete -f k8s/bankapp-deployment.yml
kubectl delete -f k8s/ollama-deployment.yml
kubectl delete -f k8s/mysql-deployment.yml
kubectl delete -f k8s/service.yml
kubectl delete -f k8s/secrets.yml
kubectl delete -f k8s/configmap.yml
kubectl delete -f k8s/pvc.yml
kubectl delete -f k8s/pv.yml
kubectl delete -f k8s/namespace.yml
```
<img width="1920" height="578" alt="Screenshot (1049)" src="https://github.com/user-attachments/assets/f0ea0d42-d1a4-4728-9d5a-d937b6bfde3b" />



To destroy everything (do this at the end of Day 83 or if taking a break):
```bash
cd terraform
terraform destroy
```
<img width="1920" height="221" alt="Screenshot (1054)" src="https://github.com/user-attachments/assets/ebb162b9-f41a-4af5-b297-05dce20caa6a" />


**Document:** What are the cost components of the AI-BankApp EKS setup? Why is the NAT Gateway surprisingly expensive?

## Cost Components — AI-BankApp EKS Setup

---

### 1. EKS Control Plane

| Item | Cost |
|---|---|
| EKS Cluster Fee | ~$0.10/hour = **~$72/month** |

> AWS charges you just for **having** a cluster running — even if no apps are deployed.

---

### 2.  EC2 Worker Nodes (Node Group)

| Instance Type | Cost (Approx/month) |
|---|---|
| t3.medium × 2 nodes | ~$60–70 |
| t3.large × 2 nodes | ~$110–120 |

> Every node = one EC2 machine running 24/7. Usually the **biggest cost.**

---

### 3.  NAT Gateway — The Surprise Bill 

| Item | Cost |
|---|---|
| Hourly Fee | ~$0.045/hour = **~$32/month** |
| Data Processing | **$0.045 per GB** |

#### Why is NAT Gateway surprisingly expensive?

Worker nodes live in a **Private Subnet** with no direct internet access.  
Every time a pod pulls a Docker image, fetches dependencies, or calls an external API — it goes through the **NAT Gateway** and **you pay per GB.**

| Action | Data Cost |
|---|---|
| Pull Docker image (~500MB) | ~$0.02 |
| Maven/pip dependency download | per GB |
| CloudWatch log shipping | per GB |
| External API calls | per GB |

> In a Java/Maven app, every CI/CD pipeline run pulls hundreds of MBs — **costs stack up silently!**

---

### 4.  Other Cost Components

| Component | Reason |
|---|---|
| EBS Storage (Persistent Volumes) | Disk for pods — charged per GB/month |
| Load Balancer | ~$16–18/month just for existing |
| ECR (Container Registry) | Docker image storage |
| CloudWatch Logs | Log ingestion + storage fees |
| Data Transfer | Outbound internet traffic |

---

### Rough Monthly Total (Small EKS Setup)

| Item | Approx Cost |
|---|---|
| EKS Control Plane | $72 |
| 2× t3.medium Nodes | $60 |
| NAT Gateway | $32+ |
| Load Balancer | $18 |
| Storage + Logs | $10–20 |
| **Total** | **~$190–200/month** |

---

### Cost Saving Tips

| Tip | Benefit |
|---|---|
| Delete cluster when not in use | Saves ~$72/month |
| Use Spot Instances for nodes | 60–70% cheaper than On-Demand |
| Use VPC Endpoints instead of NAT Gateway | Eliminates NAT cost for AWS services |
| Set CloudWatch log retention limits | Reduces log storage cost |

---

>  **Key Takeaway:** NAT Gateway feels cheap per GB but CI/CD pipelines running 10–20 times/day
> silently stack up data costs. **Cost awareness is a core DevOps skill — build efficiently!** 
---
