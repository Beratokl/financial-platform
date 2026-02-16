# AWS Deployment Guide

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (>= 1.0)
- kubectl installed
- Docker for building images

## Deployment Steps

### 1. Deploy Infrastructure

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

This creates:
- VPC with public/private subnets
- EKS cluster
- RDS PostgreSQL database
- Security groups
- IAM roles
- Secrets Manager entries

### 2. Configure kubectl

```bash
aws eks update-kubeconfig --name fintech-platform-cluster --region us-east-1
```

### 3. Build and Push Docker Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repositories
aws ecr create-repository --repository-name accounts-service
aws ecr create-repository --repository-name payments-service
aws ecr create-repository --repository-name ledger-service
aws ecr create-repository --repository-name user-profile-service

# Build and push
docker build -t accounts-service services/accounts-service
docker tag accounts-service:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/accounts-service:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/accounts-service:latest

# Repeat for other services
```

### 4. Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f infra/k8s/namespace.yaml

# Create secrets
kubectl create secret generic db-credentials \
  --from-literal=connection_string="postgresql://..." \
  -n fintech

# Deploy services
kubectl apply -f infra/k8s/accounts-service.yaml
```

## Architecture on AWS

```
┌─────────────────────────────────────────┐
│              AWS Cloud                   │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │           VPC                       │ │
│  │                                     │ │
│  │  ┌──────────────────────────────┐  │ │
│  │  │      EKS Cluster             │  │ │
│  │  │                              │  │ │
│  │  │  ┌────────┐  ┌────────┐     │  │ │
│  │  │  │ Accts  │  │ Pymts  │     │  │ │
│  │  │  └────────┘  └────────┘     │  │ │
│  │  │  ┌────────┐  ┌────────┐     │  │ │
│  │  │  │ Ledger │  │ Users  │     │  │ │
│  │  │  └────────┘  └────────┘     │  │ │
│  │  └──────────────────────────────┘  │ │
│  │                                     │ │
│  │  ┌──────────────────────────────┐  │ │
│  │  │      RDS PostgreSQL          │  │ │
│  │  │      (Private Subnet)        │  │ │
│  │  └──────────────────────────────┘  │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │    Secrets Manager                 │ │
│  │    - DB Credentials                │ │
│  │    - API Keys                      │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Security Considerations

1. **Network Security**
   - Services run in private subnets
   - RDS not publicly accessible
   - Security groups restrict traffic

2. **Data Encryption**
   - RDS encryption at rest enabled
   - TLS for data in transit
   - KMS for key management

3. **Access Control**
   - IAM roles for service accounts
   - Least privilege principle
   - MFA for admin access

4. **Monitoring**
   - CloudWatch for logs and metrics
   - AWS X-Ray for tracing
   - CloudTrail for audit logs

## Cost Optimization

- Use t3.medium for EKS nodes (dev)
- Enable RDS auto-scaling
- Use Spot instances for non-critical workloads
- Set up budget alerts

## Cleanup

```bash
# Delete Kubernetes resources
kubectl delete namespace fintech

# Destroy infrastructure
cd infra/terraform
terraform destroy
```
