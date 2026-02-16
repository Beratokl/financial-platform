# Testing Guide - Financial Platform

## Step 1: Start Services

Open terminal in VS Code (Ctrl + `) and run:

```bash
cd c:\Users\User\Financial_platform
docker-compose up -d
```

Wait 30-60 seconds for services to start.

## Step 2: Check Services Are Running

```bash
docker-compose ps
```

You should see services with "Up" status.

## Step 3: Open Dashboard

Double-click: `c:\Users\User\Financial_platform\dashboard.html`

## Step 4: Test User Profile Service

1. Click "👤 User Profile Service" in dashboard
2. You'll see API documentation page
3. Click "POST /users" 
4. Click "Try it out"
5. Paste this JSON:
```json
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "555-1234"
}
```
6. Click "Execute"
7. You should see a response with a user_id

## Step 5: Test Accounts Service

1. Click "💰 Accounts Service" in dashboard
2. Click "POST /accounts"
3. Click "Try it out"
4. Paste this (use the user_id from step 4):
```json
{
  "user_id": "PASTE_USER_ID_HERE",
  "account_type": "checking",
  "currency": "USD"
}
```
5. Click "Execute"
6. You should see account created with account_id

## Step 6: Test Payments Service

1. Click "💳 Payments Service" in dashboard
2. Click "POST /payments"
3. Click "Try it out"
4. Paste this (use account_ids from step 5):
```json
{
  "from_account": "PASTE_ACCOUNT_ID_HERE",
  "to_account": "PASTE_ACCOUNT_ID_HERE",
  "amount": 100.00,
  "currency": "USD",
  "payment_type": "transfer"
}
```
5. Click "Execute"
6. You should see payment completed

## Troubleshooting

### Services won't start?
```bash
docker-compose down
docker-compose up -d
```

### Can't connect to localhost?
Make sure Docker Desktop is running

### See errors?
```bash
docker-compose logs user-profile-service
```
