# API Gateway & Service Mesh

## Overview

The platform uses a microservices architecture with the following API endpoints:

## Service Endpoints

### User Profile Service (Port 8004)
- `POST /users` - Create user profile
- `GET /users/{user_id}` - Get user profile
- `GET /health` - Health check

### Accounts Service (Port 8001)
- `POST /accounts` - Create account
- `GET /accounts/{account_id}` - Get account details
- `GET /accounts/user/{user_id}` - Get user's accounts
- `GET /health` - Health check

### Payments Service (Port 8002)
- `POST /payments` - Create payment
- `GET /payments/{payment_id}` - Get payment details
- `GET /health` - Health check

### Ledger Service (Port 8003)
- `POST /ledger/entries` - Create ledger entry
- `GET /ledger/account/{account_id}` - Get account ledger
- `GET /health` - Health check

## Authentication Flow

1. User authenticates with Keycloak
2. Receives JWT token
3. Includes token in Authorization header
4. Services validate token with Keycloak

```
Authorization: Bearer <jwt-token>
```

## Event-Driven Architecture

Services communicate via Kafka topics:

- `account.created` - New account created
- `payment.initiated` - Payment started
- `payment.completed` - Payment finished
- `ledger.entry.created` - New ledger entry

## API Gateway (Future)

Consider adding AWS API Gateway or Kong for:
- Rate limiting
- Request routing
- API versioning
- Centralized authentication
- Monitoring and analytics
