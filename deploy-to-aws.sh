#!/bin/bash

echo "========================================="
echo "  AWS Deployment - FinTech Platform"
echo "========================================="
echo ""

# Variables
AWS_REGION="us-east-1"
CLUSTER_NAME="fintech-platform"
ECR_REPO_PREFIX="fintech"

echo "Step 1: Creating ECR Repositories..."
aws ecr create-repository --repository-name ${ECR_REPO_PREFIX}-accounts --region ${AWS_REGION}
aws ecr create-repository --repository-name ${ECR_REPO_PREFIX}-payments --region ${AWS_REGION}
aws ecr create-repository --repository-name ${ECR_REPO_PREFIX}-ledger --region ${AWS_REGION}
aws ecr create-repository --repository-name ${ECR_REPO_PREFIX}-users --region ${AWS_REGION}

echo ""
echo "Step 2: Building Docker Images..."
docker build -t ${ECR_REPO_PREFIX}-accounts:latest ./services/accounts-service
docker build -t ${ECR_REPO_PREFIX}-payments:latest ./services/payments-service
docker build -t ${ECR_REPO_PREFIX}-ledger:latest ./services/ledger-service
docker build -t ${ECR_REPO_PREFIX}-users:latest ./services/user-profile-service

echo ""
echo "Step 3: Deploying Infrastructure with Terraform..."
cd infra/terraform
terraform init
terraform plan
terraform apply -auto-approve

echo ""
echo "Step 4: Configuring kubectl..."
aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}

echo ""
echo "Step 5: Deploying to Kubernetes..."
kubectl apply -f ../k8s/namespace.yaml
kubectl apply -f ../k8s/

echo ""
echo "========================================="
echo "  Deployment Complete!"
echo "========================================="
echo ""
echo "Get service URLs:"
echo "kubectl get services -n fintech"
echo ""
echo "View pods:"
echo "kubectl get pods -n fintech"
echo ""
