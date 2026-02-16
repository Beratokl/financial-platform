# Local Development Setup

## Prerequisites

- Docker Desktop installed and running
- VS Code with Docker extension
- At least 8GB RAM available for Docker

## Quick Start

1. **Start the platform:**
   ```bash
   scripts\start-local.bat
   ```

2. **Verify services are running:**
   ```bash
   docker-compose ps
   ```

3. **Access services:**
   - Keycloak Admin: http://localhost:8080 (admin/admin)
   - Accounts API: http://localhost:8001/docs
   - Payments API: http://localhost:8002/docs
   - Ledger API: http://localhost:8003/docs
   - User Profile API: http://localhost:8004/docs

## Service Architecture

```
┌─────────────────┐
│   Keycloak      │  Identity & Auth
└────────┬────────┘
         │
    ┌────┴────────────────────┐
    │                         │
┌───▼────────┐      ┌────────▼───┐
│  Accounts  │      │   Users    │
│  Service   │      │  Service   │
└───┬────────┘      └────────────┘
    │
    │         ┌──────────────┐
    ├────────►│   Payments   │
    │         │   Service    │
    │         └──────┬───────┘
    │                │
    │         ┌──────▼───────┐
    └────────►│   Ledger     │
              │   Service    │
              └──────────────┘
```

## Testing APIs

### Create a User
```bash
curl -X POST http://localhost:8004/users \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","first_name":"John","last_name":"Doe"}'
```

### Create an Account
```bash
curl -X POST http://localhost:8001/accounts \
  -H "Content-Type: application/json" \
  -d '{"user_id":"<USER_ID>","account_type":"checking"}'
```

### Create a Payment
```bash
curl -X POST http://localhost:8002/payments \
  -H "Content-Type: application/json" \
  -d '{"from_account":"<ACCOUNT_ID>","to_account":"<ACCOUNT_ID>","amount":100.00,"payment_type":"transfer"}'
```

## Troubleshooting

### Services won't start
```bash
docker-compose down -v
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f <service-name>
```

### Reset everything
```bash
docker-compose down -v
docker system prune -a
```
