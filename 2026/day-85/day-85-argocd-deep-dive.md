# Day 85 -- ArgoCD Deep Dive: Sync Strategies, Rollbacks, and Multi-App Management

## Firstt do this before starting the task
```
 step 1
  terraform apply

 step 2
   aws eks update-kubeconfig --name bankapp-eks --region us-west-2

 step 3
   kubectl apply -f k8s/namespace.yml
   kubectl apply -f k8s/gateway.yml

 step 4
   helm install envoy-gateway oci://docker.io/envoyproxy/gateway-helm \
  --version v1.4.0 \
  -n envoy-gateway-system --create-namespace \
  --wait

export APP_URL=$(kubectl get gateway bankapp-gateway -n bankapp -o jsonpath='{.status.addresses[0].value}')
echo "AI-BankApp URL: http://$APP_URL"

 step 5
   kubectl get pods -n envoy-gateway-system
   kubectl get gatewayclass

step 6
  kubectl get crd gateways.gateway.networking.k8s.io 2>/dev/null || \
  kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml

step 7
   helm repo add jetstack https://charts.jetstack.io
   helm repo update
   helm install cert-manager jetstack/cert-manager \

step 8
 helm install cert-manager jetstack/cert-manager \
  -n cert-manager --create-namespace \
  --set crds.enabled=true \
  --wait

step 9
  kubectl get pods -n cert-manager

step 10
  then go to ec2 instance -> load balencer -> and copy the dns
  nslookup <paste dns here>
  copy the ip
  and paste in gateway.yml file
  that inside the hostname

step 11
  kubectl apply -f gateway.yml

step 12
  git add .
  git commit -m "added:gatway.yml file to that"
  git push origin feat/gitops

step 13
  see your pipline will be running

```

### Task 1: Understand Sync Strategies
ArgoCD offers multiple ways to sync:

**Automated sync** (what the AI-BankApp uses):
```yaml
syncPolicy:
  automated:
    prune: true      # Delete resources removed from Git
    selfHeal: true   # Revert manual cluster changes
```
- Every Git change syncs automatically within 3 minutes
- No human approval needed
- Good for dev/staging environments

**Manual sync** (for production):
```yaml
syncPolicy: {}   # No automated section
```
- ArgoCD detects drift but does NOT auto-correct
- A human must click "Sync" or run `argocd app sync`
- Good for production where you want a review gate

**Try switching to manual sync:**
```bash
argocd app set bankapp --sync-policy none
```

Now make a change in Git (edit `k8s/configmap.yml` in your fork -- change `APP_NAME` or add a new key). Push the commit.

Wait 3 minutes and check:
```bash
argocd app get bankapp
```

<img width="1551" height="669" alt="Screenshot (1186)" src="https://github.com/user-attachments/assets/7f7ae2f9-c1fb-4fd3-b696-a1ebd2d61964" />


The status will show `OutOfSync` but ArgoCD will NOT apply the change. You can see exactly what differs:
```bash
argocd app diff bankapp
```
<img width="1474" height="388" alt="Screenshot (1189)" src="https://github.com/user-attachments/assets/f255650a-f9bb-41a2-86ce-d8e3104a7a17" />

**Preview before syncing:**
```bash
# Dry run -- show what would change
argocd app sync bankapp --dry-run
# Sync for real
argocd app sync bankapp


```
<img width="1478" height="606" alt="Screenshot (1190)" src="https://github.com/user-attachments/assets/d0352db1-ded3-4867-bf8f-a003f952eb9f" />
<img width="1555" height="724" alt="Screenshot (1192)" src="https://github.com/user-attachments/assets/e0a87288-d013-40fa-a0e3-27576d9a13ee" />
<img width="1477" height="711" alt="Screenshot (1191)" src="https://github.com/user-attachments/assets/24e7faea-2471-492d-a517-a136a5294025" />

In the UI, clicking "Sync" shows a preview dialog listing all resources that will change.

<img width="1588" height="727" alt="Screenshot (1200)" src="https://github.com/user-attachments/assets/6747d163-89e5-4e19-8fe9-8512a135b7ab" />
<img width="1598" height="709" alt="Screenshot (1199)" src="https://github.com/user-attachments/assets/fa6cc829-3e3e-44ff-890a-986a65d77deb" />
<img width="1669" height="738" alt="Screenshot (1201)" src="https://github.com/user-attachments/assets/09033502-3d5d-4f19-9c83-cd239a807952" />

**Switch back to automated:**
```bash
argocd app set bankapp --sync-policy automated --self-heal --auto-prune
```
<img width="1417" height="612" alt="Screenshot (1182)" src="https://github.com/user-attachments/assets/746376dc-061f-4687-8f2f-aa34acb544f1" />

---



### Task 2: Sync Waves and Resource Ordering

The AI-BankApp has dependencies: MySQL must be running before the BankApp starts. ArgoCD handles this with **sync waves** -- annotations that control the order of resource creation.

**Add sync wave annotations to the AI-BankApp manifests in your fork:**

Edit `k8s/namespace.yml`:
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: bankapp
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
```

Edit `k8s/pv.yml` (StorageClass):
```yaml
metadata:
  name: gp3
  annotations:
    argocd.argoproj.io/sync-wave: "-2"
```

Edit `k8s/pvc.yml` (both PVCs):
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
```

Edit `k8s/configmap.yml` and `k8s/secrets.yml`:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "-1"
```

Edit `k8s/mysql-deployment.yml`:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "0"
```

Edit `k8s/ollama-deployment.yml`:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "0"
```

Edit `k8s/service.yml` (all three services):
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "0"
```

Edit `k8s/bankapp-deployment.yml`:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "1"
```

Edit `k8s/hpa.yml`:
```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "2"
```

**The sync order becomes:**
```
Wave -2: Namespace, StorageClass          (infrastructure)
Wave -1: PVCs, ConfigMap, Secret          (configuration)
Wave  0: MySQL, Ollama, Services          (databases and networking)
Wave  1: BankApp Deployment               (application)
Wave  2: HPA                              (scaling)
```

ArgoCD processes each wave in order. Resources in the same wave sync in parallel. ArgoCD waits for each wave to be healthy before moving to the next.

Commit and push these changes. ArgoCD will re-sync and you will see the ordered deployment in the UI.
<img width="1920" height="1019" alt="Screenshot (1184)" src="https://github.com/user-attachments/assets/c5878f65-cc0e-4973-a72f-e030de7d690d" />
<img width="1920" height="1012" alt="Screenshot (1183)" src="https://github.com/user-attachments/assets/9b2b68f1-75ee-4f1b-8c13-dac4011e5fcb" />
<img width="1920" height="996" alt="Screenshot (1185)" src="https://github.com/user-attachments/assets/26010621-5c17-485f-aad1-e5cdcc209501" />


---

### Task 3: ArgoCD Rollbacks
ArgoCD tracks every sync as a revision. You can rollback to any previous state.

**Check the sync history:**
```bash
argocd app history bankapp
```
<img width="1920" height="229" alt="Screenshot (1206)" src="https://github.com/user-attachments/assets/a4a0470e-41ac-488d-9b06-af31e3468470" />

Output:
```
ID  DATE                 REVISION
1   2026-04-10 10:00:00  abc1234
2   2026-04-10 10:15:00  def5678   (sync wave annotations)
```

**Rollback to a previous revision:**

Via CLI:
```bash
argocd app rollback bankapp 1
```
<img width="1676" height="685" alt="Screenshot (1208)" src="https://github.com/user-attachments/assets/19acded2-a484-409b-b7a7-04aa48a2a3cf" />
<img width="1527" height="690" alt="Screenshot (1207)" src="https://github.com/user-attachments/assets/c4ba5b70-542e-4d3b-8e3a-ecd748e278fa" />

Via UI: Click the application > History > select a revision > "Rollback".

After rollback:
```bash
argocd app get bankapp
```
<img width="1545" height="654" alt="Screenshot (1209)" src="https://github.com/user-attachments/assets/2359c3b8-90a9-453e-a279-e4be3faffb45" />

The status will show `OutOfSync` because the cluster now matches an older Git commit, not the latest.

**Important:** Rollback is a temporary fix. It does not change Git. The proper GitOps rollback is:
```bash
# In your fork
git revert HEAD
git push
```

This creates a new commit that undoes the last change. ArgoCD syncs the revert and the cluster is updated. The Git history shows the full audit trail: deploy, then revert.

**Document:** What is the difference between ArgoCD rollback and `git revert`? Which is the GitOps-correct approach?

```
- ArgoCD rollback reverts the application to a previous deployed revision only inside the cluster, without changing the Git repository state.
- git revert creates a new commit that undoes changes in the Git repository, making the rollback part of version-controlled history.
- In GitOps, Git is the single source of truth, so any manual rollback via ArgoCD can be overwritten by the next sync.
- Therefore, the GitOps-correct approach is git revert, because it ensures the desired state is updated in Git and consistently applied by ArgoCD.
```

---

### Task 4: App of Apps Pattern
In production, you do not manage one application -- you manage dozens. The **App of Apps** pattern uses one parent ArgoCD Application that creates child Applications.

Create a directory for the pattern:
```bash
mkdir -p argocd-apps/
```

Create `argocd-apps/bankapp.yaml` (the BankApp application):
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: bankapp
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/<your-username>/AI-BankApp-DevOps.git
    targetRevision: feat/gitops
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: bankapp
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

Create `argocd-apps/monitoring.yaml` (Prometheus + Grafana):
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: monitoring
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://prometheus-community.github.io/helm-charts
    chart: kube-prometheus-stack
    targetRevision: "65.*"
    helm:
      values: |
        grafana:
          adminPassword: admin123
        prometheus:
          prometheusSpec:
            retention: 3d
            resources:
              requests:
                memory: 256Mi
                cpu: 100m
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - ServerSideApply=true
```

Create `argocd-apps/envoy-gateway.yaml`:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: envoy-gateway
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: docker.io/envoyproxy
    chart: gateway-helm
    targetRevision: "v1.4.*"
  destination:
    server: https://kubernetes.default.svc
    namespace: envoy-gateway-system
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

**Create the parent Application** that manages all child apps:
```yaml
# argocd-apps/root-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/<your-username>/AI-BankApp-DevOps.git
    targetRevision: feat/gitops
    path: argocd-apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Push the `argocd-apps/` directory to your fork and apply the root app:
```bash
kubectl apply -f argocd-apps/root-app.yaml
```

ArgoCD will:
1. Read the `argocd-apps/` directory from Git
2. Find `bankapp.yaml`, `monitoring.yaml`, and `envoy-gateway.yaml`
3. Create three child Applications
4. Each child Application syncs independently

**In the ArgoCD UI,** you now see 4 applications: `root-app`, `bankapp`, `monitoring`, `envoy-gateway`. Adding a new app to the cluster is as simple as adding a new YAML file to the `argocd-apps/` directory.

```bash
argocd app list
```
<img width="1699" height="636" alt="Screenshot (1214)" src="https://github.com/user-attachments/assets/916a4fe4-5070-4703-bb0e-c4206b83ba15" />

---

### Task 5: ArgoCD Notifications
Get notified when deployments succeed, fail, or drift.

Install ArgoCD Notifications (included in modern ArgoCD versions):
```bash
# Check if notifications controller is running
kubectl get pods -n argocd -l app.kubernetes.io/component=notifications-controller
```

**Configure a Slack or webhook notification** (using a generic webhook example):

Create a notification config:
```bash
kubectl apply -n argocd -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  trigger.on-sync-succeeded: |
    - when: app.status.operationState.phase in ['Succeeded']
      send: [app-sync-succeeded]
  trigger.on-sync-failed: |
    - when: app.status.operationState.phase in ['Error', 'Failed']
      send: [app-sync-failed]
  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-health-degraded]
  template.app-sync-succeeded: |
    message: "Application {{.app.metadata.name}} sync succeeded. Revision: {{.app.status.sync.revision}}"
  template.app-sync-failed: |
    message: "Application {{.app.metadata.name}} sync FAILED! Check ArgoCD for details."
  template.app-health-degraded: |
    message: "Application {{.app.metadata.name}} health is DEGRADED. Investigate immediately."
EOF
```

**Subscribe an application to notifications:**
```bash
kubectl annotate application bankapp -n argocd \
  notifications.argoproj.io/subscribe.on-sync-succeeded.webhook="" \
  notifications.argoproj.io/subscribe.on-sync-failed.webhook="" \
  notifications.argoproj.io/subscribe.on-health-degraded.webhook=""
```
<img width="1720" height="386" alt="Screenshot (1221)" src="https://github.com/user-attachments/assets/cb8af1c2-27a0-44ad-a4a8-00e3facf8abf" />
<img width="1920" height="333" alt="Screenshot (1226)" src="https://github.com/user-attachments/assets/4c66adf9-bb0e-470b-a351-2747bc4de2d6" />

For Slack integration, you would add a Slack service to the ConfigMap with your webhook URL. The pattern is the same -- triggers fire on events, templates format the message, services deliver it.

**View notification history:**
```bash
kubectl get applications bankapp -n argocd -o jsonpath='{.status.operationState.message}'
```

<img width="1920" height="580" alt="Screenshot (1229)" src="https://github.com/user-attachments/assets/cd7f680a-daab-4468-ac55-de36e492fb4f" />

---


### Task 6: ArgoCD Projects and RBAC
In production, you do not give every team access to every application. ArgoCD **Projects** provide multi-tenancy.

Create a project for the BankApp team:
```bash
argocd proj create bankapp-team \
  --description "AI-BankApp team project" \
  --src "https://github.com/<your-username>/AI-BankApp-DevOps.git" \
  --dest "https://kubernetes.default.svc,bankapp" \
  --dest "https://kubernetes.default.svc,monitoring"
```
<img width="1517" height="542" alt="Screenshot (1231)" src="https://github.com/user-attachments/assets/7c1aec61-8c28-47bf-b49b-9a24735f9c4a" />

This project:
- Can only source from the AI-BankApp repo
- Can only deploy to the `bankapp` and `monitoring` namespaces
- Cannot deploy to `kube-system`, `argocd`, or other namespaces

Move the bankapp Application to this project:
```bash
argocd app set bankapp --project bankapp-team
```

**Verify restrictions work:**
```bash
# This should fail -- cert-manager namespace is not allowed
argocd proj add-destination bankapp-team https://kubernetes.default.svc kube-system 2>&1 || echo "Restricted!"
```

**RBAC policies** (in `argocd-rbac-cm` ConfigMap):
```yaml
policy.csv: |
  p, role:bankapp-dev, applications, get, bankapp-team/*, allow
  p, role:bankapp-dev, applications, sync, bankapp-team/*, allow
  p, role:bankapp-dev, applications, rollback, bankapp-team/*, deny
  g, bankapp-developers, role:bankapp-dev
```

This gives the `bankapp-developers` group permission to view and sync but NOT rollback. Rollback requires a senior team member.

**Document:** How do Projects and RBAC prevent one team from accidentally affecting another team's applications?
```
ArgoCD Projects enforce multi-tenancy by restricting which Git repositories and Kubernetes namespaces an application can deploy to.
In this setup, the bankapp-team project only allows deployments to the bankapp and monitoring namespaces.

When attempting to deploy resources to kube-system and other restricted cluster-level resources,
ArgoCD correctly blocked the sync operation. 
This confirms that project-level RBAC policies are working as expected and prevent unauthorized or accidental deployments to sensitive namespaces and cluster-wide resources.
```
---








  
