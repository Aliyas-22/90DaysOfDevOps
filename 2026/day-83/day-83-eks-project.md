# Day 83 -- EKS Project: Production Deployment of AI-BankApp

## Challenge Tasks

### Task 1: Deploy the Complete AI-BankApp Stack
Make sure your EKS cluster is running:
```bash
kubectl get nodes
```

If you destroyed the cluster, re-provision it:
```bash
cd AI-BankApp-DevOps/terraform
terraform apply
aws eks update-kubeconfig --name bankapp-eks --region us-west-2
```

Deploy the entire application stack in order:
```bash
cd AI-BankApp-DevOps

# 1. Namespace and storage
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/pv.yml
kubectl apply -f k8s/pvc.yml

# 2. Configuration
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secrets.yml

# 3. Database and AI service
kubectl apply -f k8s/mysql-deployment.yml
kubectl apply -f k8s/service.yml
kubectl apply -f k8s/ollama-deployment.yml

# 4. Wait for dependencies
echo "Waiting for MySQL..."
kubectl wait --for=condition=ready pod -l app=mysql -n bankapp --timeout=120s

echo "Waiting for Ollama (this takes 2-5 minutes for model pull)..."
kubectl wait --for=condition=ready pod -l app=ollama -n bankapp --timeout=600s

# 5. Application
kubectl apply -f k8s/bankapp-deployment.yml
kubectl apply -f k8s/hpa.yml

# 6. Wait for BankApp
echo "Waiting for BankApp..."
kubectl wait --for=condition=ready pod -l app=bankapp -n bankapp --timeout=300s
```
<img width="1508" height="784" alt="Screenshot (1072)" src="https://github.com/user-attachments/assets/aa4de181-9e04-4c4f-a900-47b92fe0d27b" />


Verify everything is running:
```bash
kubectl get all -n bankapp
kubectl get pvc -n bankapp
```

You should see:
- MySQL: 1 pod running with 5Gi PVC bound
- Ollama: 1 pod running with 10Gi PVC bound
- BankApp: 2-4 pods running (managed by HPA)
- Services: 3 ClusterIP services
<img width="1366" height="691" alt="Screenshot (1073)" src="https://github.com/user-attachments/assets/1b0ae3b9-830c-40b1-8261-744c7876dd5b" />


---

### Task 2: Set Up Gateway API and Access the App
Install Envoy Gateway (if not done on Day 82):
```bash
helm install envoy-gateway oci://docker.io/envoyproxy/gateway-helm \
  --version v1.4.0 \
  -n envoy-gateway-system --create-namespace \
  --wait 2>/dev/null || echo "Already installed"
```
<img width="1315" height="813" alt="Screenshot (1075)" src="https://github.com/user-attachments/assets/4d203e68-cd0b-4135-9a0f-d2c0bb7a2bae" />

Apply the Gateway configuration:
```bash
kubectl apply -f k8s/gateway.yml
```


Wait for the NLB:
```bash
kubectl get gateway -n bankapp -w
```
<img width="1500" height="442" alt="Screenshot (1076)" src="https://github.com/user-attachments/assets/6e157f60-be30-4a33-9db8-079a84aeb2a2" />

Get the external address:
```bash
export APP_URL=$(kubectl get gateway bankapp-gateway -n bankapp -o jsonpath='{.status.addresses[0].value}')
echo "AI-BankApp URL: http://$APP_URL"
```
<img width="1870" height="290" alt="Screenshot (1071)" src="https://github.com/user-attachments/assets/115f9983-927a-4cad-aebc-1c0c492214b4" />

Test the application:
```bash
# Health check (Spring Boot Actuator)
curl -s http://$APP_URL/actuator/health | python3 -m json.tool

# Load the home page
curl -s -o /dev/null -w "%{http_code}" http://$APP_URL
```
<img width="1351" height="340" alt="Screenshot (1080)" src="https://github.com/user-attachments/assets/58f40d51-23d3-4d5b-bf3f-66f2799fa498" />

Open `http://$APP_URL` in your browser:
1. Click "Register" and create an account
2. Log in with your credentials
3. Perform banking operations (deposit, withdraw, transfer)
4. Try the AI chatbot -- ask a financial question
5. Toggle dark/light mode

**The full stack is running on EKS:** Spring Boot serves the UI, MySQL stores accounts and transactions, Ollama's TinyLlama model powers the AI chatbot -- all on managed Kubernetes with persistent storage and autoscaling.
<img width="1920" height="1015" alt="Screenshot (1078)" src="https://github.com/user-attachments/assets/fb378db6-d450-446c-9356-0956ee19972f" />
<img width="1920" height="1025" alt="Screenshot (1082)" src="https://github.com/user-attachments/assets/2cf94109-3298-4270-a6b2-ddc35b1e9eb3" />
<img width="1920" height="1022" alt="Screenshot (1081)" src="https://github.com/user-attachments/assets/86e1bdfd-33c6-44fb-ae9d-41b62b4af523" />

---

### Task 3: Deploy the Monitoring Stack
Deploy Prometheus and Grafana to monitor the AI-BankApp on EKS.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  --set grafana.adminPassword=admin123 \
  --set prometheus.prometheusSpec.retention=3d \
  --set prometheus.prometheusSpec.resources.requests.memory=256Mi \
  --set prometheus.prometheusSpec.resources.requests.cpu=100m \
  --wait --timeout 600s
```
<img width="1498" height="749" alt="Screenshot (1083)" src="https://github.com/user-attachments/assets/6eaa90e8-8c41-45cd-b16e-92aaecbb6866" />


Verify:
```bash
kubectl get pods -n monitoring
```
<img width="1177" height="331" alt="Screenshot (1084)" src="https://github.com/user-attachments/assets/f770b909-cc3a-4d86-b205-7eec30755974" />

**Access Grafana:**
```bash
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```

Open `http://localhost:3000`. Login: `admin` / `admin123`.
<img width="1920" height="978" alt="Screenshot (1085)" src="https://github.com/user-attachments/assets/4fc49770-d606-4339-80cc-ecb1e280b7d6" />

**The AI-BankApp exposes Prometheus metrics natively.** The Spring Boot Actuator endpoint at `/actuator/prometheus` provides JVM metrics, HTTP request metrics, and more.

Create a ServiceMonitor to scrape the BankApp:
```yaml
# bankapp-servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: bankapp-monitor
  namespace: monitoring
  labels:
    release: monitoring
spec:
  namespaceSelector:
    matchNames:
      - bankapp
  selector:
    matchLabels:
      app: bankapp
  endpoints:
    - port: "8080"
      path: /actuator/prometheus
      interval: 15s
```

```bash
kubectl apply -f bankapp-servicemonitor.yaml
```

**Access Prometheus:**
```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus -n monitoring 9090:9090
```

Query AI-BankApp metrics:
```promql
# JVM memory usage
jvm_memory_used_bytes{namespace="bankapp"}
<img width="1920" height="957" alt="Screenshot (1109)" src="https://github.com/user-attachments/assets/87bffdfc-eaa3-4996-a47d-02d2cfb127b8" />

# HTTP request rate
rate(http_server_requests_seconds_count{namespace="bankapp"}[5m])
<img width="1920" height="984" alt="Screenshot (1107)" src="https://github.com/user-attachments/assets/bc67b296-f130-42eb-bb0f-456a399f3034" />

# HTTP request latency (95th percentile)
histogram_quantile(0.95, rate(http_server_requests_seconds_bucket{namespace="bankapp"}[5m]))
<img width="1920" height="966" alt="Screenshot (1111)" src="https://github.com/user-attachments/assets/a3809d89-e334-4cbf-844f-be3207620be5" />


```

Explore the pre-built Grafana dashboards:
- **Kubernetes / Compute Resources / Namespace (Pods)** -- select the `bankapp` namespace
- <img width="1920" height="977" alt="Screenshot (1091)" src="https://github.com/user-attachments/assets/1d47b65b-e6bc-46cb-b875-415129060674" />
<img width="1920" height="957" alt="Screenshot (1092)" src="https://github.com/user-attachments/assets/f2222247-b064-4bcc-a152-7fe90e7ea71e" />
<img width="1920" height="983" alt="Screenshot (1094)" src="https://github.com/user-attachments/assets/100342da-cbcc-4b8d-8d8b-42b9ab508958" />
<img width="1920" height="980" alt="Screenshot (1093)" src="https://github.com/user-attachments/assets/f38b7f25-f947-47c2-813e-5e01b95a682f" />

- **Kubernetes / Compute Resources / Pod** -- drill into individual pods
  <img width="1920" height="984" alt="Screenshot (1096)" src="https://github.com/user-attachments/assets/d4e1a7cf-5348-4554-919b-f578c14781b1" />
<img width="1920" height="970" alt="Screenshot (1095)" src="https://github.com/user-attachments/assets/1e01fd07-8331-4589-9672-917dfe010323" />
<img width="1920" height="994" alt="Screenshot (1097)" src="https://github.com/user-attachments/assets/25cf2c5c-a0f4-46d2-85ed-24e71409fc87" />

- **Node Exporter / Nodes** -- EKS worker node health<img 


---

### Task 4: End-to-End Validation Checklist
Run through the complete validation:

**Application layer:**
```bash
# All pods running and ready
kubectl get pods -n bankapp
echo "---"

# App responds on health endpoint
curl -s http://$APP_URL/actuator/health
echo "---"

# HPA is active and monitoring CPU
kubectl get hpa -n bankapp
echo "---"

# Prometheus metrics endpoint works
curl -s http://$APP_URL/actuator/prometheus | head -10
```
<img width="1920" height="833" alt="Screenshot (1099)" src="https://github.com/user-attachments/assets/fd5832cb-050d-4da7-b465-a6ff89e8bd6f" />

**Data layer:**
```bash
# MySQL is healthy with persistent storage
kubectl exec -n bankapp deploy/mysql -- mysqladmin ping -h localhost -uroot -pTest@123
echo "---"

# PVCs are bound to EBS volumes
kubectl get pvc -n bankapp
echo "---"

# Ollama has the model loaded
kubectl exec -n bankapp deploy/ollama -- ollama list
```
<img width="1920" height="340" alt="Screenshot (1101)" src="https://github.com/user-attachments/assets/f06d7015-3d4b-4011-aef7-c9a7957efd2e" />

**Infrastructure layer:**
```bash
# Nodes are healthy
kubectl get nodes
kubectl top nodes
echo "---"

# Gateway is serving traffic
kubectl get gateway -n bankapp
echo "---"

# Monitoring is running
kubectl get pods -n monitoring | head -5
```
<img width="1920" height="507" alt="Screenshot (1102)" src="https://github.com/user-attachments/assets/7cb5f823-42b4-4b56-b409-e6a1a28b2036" />

**Security layer:**
```bash
# BankApp runs as non-root (devsecops user)
kubectl exec -n bankapp deploy/bankapp -- whoami

# Secrets are not exposed in environment
kubectl get secret bankapp-secret -n bankapp -o yaml | grep -c "MYSQL_ROOT_PASSWORD"
```
<img width="1920" height="168" alt="Screenshot (1100)" src="https://github.com/user-attachments/assets/afa13962-b2ee-4fc7-8a2b-951f692311e8" />

---

### Task 5: Reflect on the Full EKS Journey
Map each concept to the day you learned it:

| Day | What You Built | AI-BankApp Connection |
|-----|---------------|----------------------|
| 81 | EKS cluster via Terraform, kubectl connection, manual deploy | Used the project's `terraform/` configs to provision infra |
| 82 | Gateway API, Envoy, TLS, EBS storage, session persistence | Used `k8s/gateway.yml`, `k8s/cert-manager.yml`, `k8s/pv.yml` |
| 83 | Full production deployment, monitoring, validation | Complete stack: app + DB + AI + networking + observability |

**What the AI-BankApp's EKS setup includes that you have now seen:**
- Terraform-provisioned VPC with 3-AZ networking
- Managed node group with auto-scaling
- 6 EKS add-ons (CoreDNS, VPC CNI, kube-proxy, Pod Identity, EBS CSI, Metrics Server)
- ArgoCD pre-installed (used on Days 84-86)
- Gateway API with Envoy for traffic management
- cert-manager for automated HTTPS
- Cookie-based session persistence for stateful app
- EBS persistent storage for MySQL and Ollama
- HPA with scale-up/down policies
- Spring Boot Actuator metrics for Prometheus
- Init containers for dependency ordering
- PostStart lifecycle hooks for Ollama model pull

**What you would add for a real production deployment:**
- DNS with Route 53 and ExternalDNS
- Network Policies for pod-to-pod isolation
- Pod Disruption Budgets for safe node draining
- External Secrets Operator for AWS Secrets Manager integration
- Database backups (automated MySQL dumps to S3)
- Log aggregation with Loki (you built this on Day 75)
- Multi-environment clusters (dev + prod)

---

### Task 6: Complete Teardown
**This is critical -- do not leave resources running.**

Delete workloads first:
```bash
# Delete monitoring
helm uninstall monitoring -n monitoring

# Delete Gateway resources (releases the NLB)
kubectl delete -f k8s/gateway.yml 2>/dev/null

# Delete the BankApp stack
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

# Delete Envoy Gateway
helm uninstall envoy-gateway -n envoy-gateway-system 2>/dev/null

# Delete cert-manager
helm uninstall cert-manager -n cert-manager 2>/dev/null

# Delete namespaces
kubectl delete namespace monitoring envoy-gateway-system cert-manager 2>/dev/null
```

Wait for all LoadBalancers and EBS volumes to be released:
```bash
# Check for lingering load balancers
kubectl get svc -A | grep LoadBalancer

# Check for lingering PVCs
kubectl get pvc -A
```

**Destroy the infrastructure with Terraform:**
```bash
cd terraform
terraform destroy
```

This takes 10-15 minutes. It deletes:
- EKS cluster and control plane
- All node groups and EC2 instances
- ArgoCD Helm release
- VPC, subnets, NAT gateway, internet gateway
- IAM roles and policies

**Verify in the AWS Console:**
- EKS: no clusters
- EC2: no instances, no load balancers, no EBS volumes
- VPC: the `bankapp-eks` VPC is gone
- CloudFormation: no lingering stacks

**Check your AWS bill** in the Billing Dashboard. All charges should stop within the hour.

**Cost for this 3-day lab (approximate):** $15-25 depending on how long you kept the cluster running.

---
