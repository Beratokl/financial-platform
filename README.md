# Financial Platform

A cloud-ready, open-source-powered financial platform for modern fintech capabilities.

## 🧱 Core Components

- **Apache Fineract** - Core banking features (accounts, loans, savings, ledgers)
- **Moov** - Payments infrastructure (ACH, wallets, card issuing)
- **Keycloak** - Identity and access management (authentication, authorization, MFA)
- **Kafka** - Event streaming for real-time financial workflows
- **Custom Microservices** - Business logic orchestration

## 📁 Repository Structure

```
├── services/              # Custom microservices
│   ├── accounts-service/
│   ├── payments-service/
│   ├── ledger-service/
│   └── user-profile-service/
├── infra/                 # Infrastructure as code
│   ├── terraform/         # AWS infrastructure
│   └── k8s/              # Kubernetes manifests
├── docker/               # Docker configurations
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## 🐳 Local Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ AWS Deployment

Deploy to AWS using EKS:
```bash
cd infra/terraform
terraform init
terraform apply
```

## 🔐 Security

- Encrypted data at rest and in transit
- IAM roles and policies
- Secrets Manager integration
- Audit logging
- Private VPC networking

## 📚 Documentation

See `/docs` for detailed guides on:
- Local setup
- Service development
- AWS deployment
- Security configuration
