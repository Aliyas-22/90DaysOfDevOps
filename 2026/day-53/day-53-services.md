# Day 53 – Kubernetes Services
## Challenge Tasks

### Task 1: Deploy the Application
First, create a Deployment that you will expose with Services. Create `app-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
```

```bash
kubectl apply -f app-deployment.yaml
kubectl get pods -o wide
```

Note the individual Pod IPs. These will change if pods restart — that is the problem Services fix.

**Verify:** Are all 3 pods running? Note down their IP addresses.
<img width="1449" height="208" alt="Screenshot (416)" src="https://github.com/user-attachments/assets/ed6d2786-4981-45a2-8ca4-ac0d1f0d63f6" />

---

### Task 2: ClusterIP Service (Internal Access)
ClusterIP is the default Service type. It gives your Pods a stable internal IP that is only reachable from within the cluster.

Create `clusterip-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-clusterip
spec:
  type: ClusterIP
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
```
Key fields:
- `selector.app: web-app` — this Service routes traffic to all Pods with the label `app: web-app`
- `port: 80` — the port the Service listens on
- `targetPort: 80` — the port on the Pod to forward traffic to

```bash
kubectl apply -f clusterip-service.yaml
kubectl get services
```

You should see `web-app-clusterip` with a CLUSTER-IP address. This IP is stable — it will not change even if Pods restart.

Now test it from inside the cluster:
```bash
# Run a temporary pod to test connectivity
kubectl run test-client --image=busybox:latest --rm -it --restart=Never -- sh

# Inside the test pod, run:
wget -qO- http://web-app-clusterip
exit
```

You should see the Nginx welcome page. The Service load-balanced your request to one of the 3 Pods.

**Verify:** Does the Service respond? Try running the wget command multiple times — the Service distributes traffic across all healthy Pods.
<img width="1920" height="189" alt="Screenshot (417)" src="https://github.com/user-attachments/assets/b94af154-8e58-439f-829e-9cc35ae564c6" />

---

---
<img width="1920" height="641" alt="Screenshot (418)" src="https://github.com/user-attachments/assets/316c0bf6-c2b3-4bcf-855c-eb82e5384be1" />

---
### Task 3: Discover Services with DNS
Kubernetes has a built-in DNS server. Every Service gets a DNS entry automatically:

```
<service-name>.<namespace>.svc.cluster.local
```

Test this:
```bash
kubectl run dns-test --image=busybox:latest --rm -it --restart=Never -- sh

# Inside the pod:
# Short name (works within the same namespace)
wget -qO- http://web-app-clusterip

# Full DNS name
wget -qO- http://web-app-clusterip.default.svc.cluster.local

# Look up the DNS entry
nslookup web-app-clusterip
exit
```

Both the short name and the full DNS name resolve to the same ClusterIP. In practice, you use the short name when communicating within the same namespace and the full name when reaching across namespaces.

**Verify:** What IP does `nslookup` return? Does it match the CLUSTER-IP from `kubectl get services`?


<img width="1920" height="591" alt="Screenshot (419)" src="https://github.com/user-attachments/assets/c192bc16-d634-435b-a178-34b085332e6e" />

---

### Task 4: NodePort Service (External Access via Node)
A NodePort Service exposes your application on a port on every node in the cluster. This lets you access the Service from outside the cluster.

Create `nodeport-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-nodeport
spec:
  type: NodePort
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30080
```

- `nodePort: 30080` — the port opened on every node (must be in range 30000-32767)
- Traffic flow: `<NodeIP>:30080` -> Service -> Pod:80

```bash
kubectl apply -f nodeport-service.yaml
kubectl get services
```

Access the service:
```bash
# If using Minikube
minikube service web-app-nodeport --url

# If using Kind, get the node IP first
kubectl get nodes -o wide
# Then curl <node-internal-ip>:30080

# If using Docker Desktop
curl http://localhost:30080
```

**Verify:** Can you see the Nginx welcome page from your browser or terminal using the NodePort?
<img width="1920" height="552" alt="Screenshot (421)" src="https://github.com/user-attachments/assets/1b7f38e0-01a1-40d4-9ea5-efad1871e178" />

---

### Task 5: LoadBalancer Service (Cloud External Access)
In a cloud environment (AWS, GCP, Azure), a LoadBalancer Service provisions a real external load balancer that routes traffic to your nodes.

Create `loadbalancer-service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 80
```

```bash
kubectl apply -f loadbalancer-service.yaml
kubectl get services
```

On a local cluster (Minikube, Kind, Docker Desktop), the EXTERNAL-IP will show `<pending>` because there is no cloud provider to create a real load balancer. This is expected.

If you are using Minikube:
```bash
# Minikube can simulate a LoadBalancer
minikube tunnel
# In another terminal, check again:
kubectl get services
```

In a real cloud cluster, the EXTERNAL-IP would be a public IP address or hostname provisioned by the cloud provider.

**Verify:** What does the EXTERNAL-IP column show? Why is it `<pending>` on a local cluster?

---
<img width="1367" height="779" alt="Screenshot (422)" src="https://github.com/user-attachments/assets/56c18cd4-f63b-4f85-bb2c-3563166aec9a" />

---
### Task 6: Understand the Service Types Side by Side
Check all three services:

```bash
kubectl get services -o wide
```

Compare them:

| Type | Accessible From | Use Case |
|------|----------------|----------|
| ClusterIP | Inside the cluster only | Internal communication between services |
| NodePort | Outside via `<NodeIP>:<NodePort>` | Development, testing, direct node access |
| LoadBalancer | Outside via cloud load balancer | Production traffic in cloud environments |

Each type builds on the previous one:
- LoadBalancer creates a NodePort, which creates a ClusterIP
- So a LoadBalancer service also has a ClusterIP and a NodePort

Verify this:
```bash
kubectl describe service web-app-loadbalancer
```

You should see all three: a ClusterIP, a NodePort, and the LoadBalancer configuration.

**Verify:** Does the LoadBalancer service also have a ClusterIP and NodePort assigned?
<img width="1502" height="165" alt="Screenshot (423)" src="https://github.com/user-attachments/assets/f74ec201-4a8c-4a99-9abc-5dc1d760d654" />

   **yes!! its have ClusterIp and nodeport assigned**
   
---
### Task 7: Clean Up
```bash
kubectl delete -f app-deployment.yaml
kubectl delete -f clusterip-service.yaml
kubectl delete -f nodeport-service.yaml
kubectl delete -f loadbalancer-service.yaml

kubectl get pods
kubectl get services
```

Only the built-in `kubernetes` service in the default namespace should remain.

**Verify:** Is everything cleaned up?

  **yes everything is cleaned**
 
---

## Documentation
Create `day-53-services.md` with:
- What problem Services solve and how they relate to Pods and Deployments

  + Pods in Kubernetes are not stable They can restart, die, or get new IP So their IP keeps changing
  + Service gives a fixed IP and name So we don’t talk to Pods directly we talk to the Service
  + Deployment → creates & manages Pods
  + Pods → run your app
  + Service → connects users to Pods
    
- Your three Service manifests with an explanation of each type
  
    1) ClusterIP:-
        + Works only inside cluster
        +  Used for internal communication

    2) NodePort:-
        + Exposes app outside cluster
        + Uses Node IP + Port

    3) loadBalancer:-
        + Used in cloud (AWS, Azure, GCP)
        + Gives public IP
        
  
- The difference between ClusterIP, NodePort, and LoadBalancer
  

| Type         | Where it works       | Use         |
|--------------|---------------------|-------------|
| ClusterIP    | Inside only         | Pod-to-Pod  |
| NodePort     | Outside (NodeIP)    | Testing     |
| LoadBalancer | Public internet     | Production  |


- How Kubernetes DNS works for service discovery
     + Kubernetes gives automatic DNS name Instead of IP
     + Kubernetes runs DNS
     + maps: Service Name → Service IP
     + DNS lets Pods talk using name not IP
       
- What Endpoints are and how to inspect them
    + Endpoints = actual Pod IPs behind a Service
    + Service → forwards request → Endpoints → Pods
    + These are real Pods serving traffic
  
--- 


