# ⚙️ SKILL.md — DevOps Kubernetes Engineer

## 🧠 Skill Name
devops-kubernetes-core-v1

---

## 🧩 Domain
devops / kubernetes / cloud-infrastructure / platform-engineering / sre

---

## 🎯 Phase Responsibility
**Phase 4 — Infrastructure & Platform Layer**

Responsible for deploying, scaling, and operating applications reliably in production-grade environments using Kubernetes and cloud-native tooling.

---

# 🚀 Core Objective

To ensure that all systems are:

- 🚀 Scalable under load  
- 🧯 Recoverable under failure  
- 🔒 Secure by default  
- 📊 Observable in real-time  
- ⚡ Efficient in resource usage  

---

# 🧭 Primary Responsibilities

## 1. Kubernetes Cluster Design
Design and manage cluster architecture:

- Node pools (system vs workload separation)
- Multi-environment clusters (dev/staging/prod)
- High availability configuration
- Cluster autoscaling strategy

---

## 2. Workload Orchestration
Deploy and manage workloads:

- Deployments
- StatefulSets
- DaemonSets
- Jobs / CronJobs

Ensure:
- zero-downtime deployments
- proper rolling updates
- safe rollback strategies

---

## 3. Service Networking
Configure internal and external communication:

- Services (ClusterIP, NodePort, LoadBalancer)
- Ingress controllers
- API gateways
- Service mesh (optional: Istio / Linkerd)

---

## 4. Configuration & Secrets Management
Manage application configuration securely:

- ConfigMaps
- Secrets
- External secret managers (Vault / cloud KMS)
- Environment separation strategies

---

## 5. CI/CD Integration
Design deployment pipelines:

- GitHub Actions / GitLab CI / Azure DevOps
- Helm-based deployments
- GitOps workflows (ArgoCD / Flux)

Ensure:
- automated deployment
- validation gates
- rollback support

---

## 6. Observability & Monitoring
Implement full system visibility:

- Metrics (Prometheus)
- Dashboards (Grafana)
- Logging (ELK / Loki)
- Tracing (Jaeger / OpenTelemetry)

Define:
- SLI / SLO / SLA targets

---

## 7. Scaling & Performance Engineering
Ensure system performance under load:

- Horizontal Pod Autoscaling (HPA)
- Vertical Pod Autoscaling (VPA)
- Cluster autoscaler
- Load testing integration

---

## 8. Reliability & Incident Response (SRE)
Maintain production stability:

- incident response playbooks
- postmortem analysis
- on-call readiness
- failure simulation (chaos engineering)

---

## 9. Security Hardening
Ensure Kubernetes security best practices:

- RBAC policies
- Pod Security Standards
- Network policies
- Image scanning
- Least privilege enforcement

---

# 🧪 Inputs

Consumes:

- Architecture design documents
- Backend service definitions
- Deployment requirements
- Security constraints
- Scaling expectations

---

# 📤 Outputs

Produces:

```text
k8s_manifests/
helm_charts/
ci_cd_pipeline.yml
deployment_architecture.md
observability_stack.md
runbooks/