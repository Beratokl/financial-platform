import requests
import json
import time
from datetime import datetime

BASE_URLS = {
    'users': 'http://localhost:8004',
    'accounts': 'http://localhost:8001',
    'payments': 'http://localhost:8002',
    'ledger': 'http://localhost:8003'
}

SAMPLE_USERS = [
    {"first_name": "Sarah", "last_name": "Johnson", "email": "sarah.johnson@example.com", "phone": "555-0101"},
    {"first_name": "Michael", "last_name": "Chen", "email": "michael.chen@example.com", "phone": "555-0202"},
    {"first_name": "Emily", "last_name": "Rodriguez", "email": "emily.rodriguez@example.com", "phone": "555-0303"},
    {"first_name": "James", "last_name": "Williams", "email": "james.williams@example.com", "phone": "555-0404"},
    {"first_name": "Maria", "last_name": "Garcia", "email": "maria.garcia@example.com", "phone": "555-0505"},
    {"first_name": "David", "last_name": "Brown", "email": "david.brown@example.com", "phone": "555-0606"},
    {"first_name": "Lisa", "last_name": "Anderson", "email": "lisa.anderson@example.com", "phone": "555-0707"},
    {"first_name": "Robert", "last_name": "Taylor", "email": "robert.taylor@example.com", "phone": "555-0808"},
    {"first_name": "Jennifer", "last_name": "Martinez", "email": "jennifer.martinez@example.com", "phone": "555-0909"},
    {"first_name": "William", "last_name": "Lee", "email": "william.lee@example.com", "phone": "555-1010"}
]

ACCOUNT_TYPES = ["checking", "savings", "business"]
PAYMENT_TYPES = ["transfer", "deposit", "withdrawal", "payment"]

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def create_users():
    print_header("👤 Creating Sample Users")
    users = []
    
    for user_data in SAMPLE_USERS:
        try:
            response = requests.post(f"{BASE_URLS['users']}/users", json=user_data)
            if response.status_code == 200:
                user = response.json()
                users.append(user)
                print(f"✅ Created: {user['first_name']} {user['last_name']} (ID: {user['user_id'][:8]}...)")
            else:
                print(f"❌ Failed to create {user_data['first_name']} {user_data['last_name']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return users

def create_accounts(users):
    print_header("💰 Creating Sample Accounts")
    accounts = []
    
    for user in users:
        # Create 1-2 accounts per user
        num_accounts = 2 if users.index(user) % 2 == 0 else 1
        
        for i in range(num_accounts):
            account_type = ACCOUNT_TYPES[i % len(ACCOUNT_TYPES)]
            account_data = {
                "user_id": user['user_id'],
                "account_type": account_type,
                "currency": "USD"
            }
            
            try:
                response = requests.post(f"{BASE_URLS['accounts']}/accounts", json=account_data)
                if response.status_code == 200:
                    account = response.json()
                    accounts.append(account)
                    print(f"✅ Created {account_type} account for {user['first_name']} {user['last_name']} (ID: {account['account_id'][:8]}...)")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    return accounts

def create_payments(accounts):
    print_header("💳 Creating Sample Payments")
    payments = []
    
    # Create 15 sample payments
    for i in range(15):
        if len(accounts) < 2:
            break
            
        from_account = accounts[i % len(accounts)]
        to_account = accounts[(i + 1) % len(accounts)]
        
        amount = round(50 + (i * 25.5), 2)
        
        payment_data = {
            "from_account": from_account['account_id'],
            "to_account": to_account['account_id'],
            "amount": amount,
            "currency": "USD",
            "payment_type": PAYMENT_TYPES[i % len(PAYMENT_TYPES)]
        }
        
        try:
            response = requests.post(f"{BASE_URLS['payments']}/payments", json=payment_data)
            if response.status_code == 200:
                payment = response.json()
                payments.append(payment)
                print(f"✅ Payment ${amount} - {payment['payment_type']} (ID: {payment['payment_id'][:8]}...)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return payments

def create_ledger_entries(accounts, payments):
    print_header("📒 Creating Ledger Entries")
    
    for payment in payments:
        ledger_data = {
            "account_id": payment['from_account'],
            "transaction_type": payment['payment_type'],
            "amount": payment['amount'],
            "balance_after": payment['amount'],
            "reference_id": payment['payment_id']
        }
        
        try:
            response = requests.post(f"{BASE_URLS['ledger']}/ledger/entries", json=ledger_data)
            if response.status_code == 200:
                entry = response.json()
                print(f"✅ Ledger entry created (ID: {entry['entry_id'][:8]}...)")
        except Exception as e:
            print(f"❌ Error: {e}")

def show_summary(users, accounts, payments):
    print_header("📊 Summary")
    print(f"👥 Total Users: {len(users)}")
    print(f"💰 Total Accounts: {len(accounts)}")
    print(f"💳 Total Payments: {len(payments)}")
    print(f"📒 Total Ledger Entries: {len(payments)}")
    print("\n✨ Sample data loaded successfully!")
    print("\n🌐 View the data:")
    print(f"   Users:    {BASE_URLS['users']}/docs")
    print(f"   Accounts: {BASE_URLS['accounts']}/docs")
    print(f"   Payments: {BASE_URLS['payments']}/docs")
    print(f"   Ledger:   {BASE_URLS['ledger']}/docs")

def main():
    print("\n🏦 Financial Platform - Sample Data Generator")
    print("=" * 60)
    
    # Check if services are running
    print("\n🔍 Checking services...")
    for service, url in BASE_URLS.items():
        try:
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ {service.capitalize()} service is running")
            else:
                print(f"⚠️  {service.capitalize()} service returned status {response.status_code}")
        except:
            print(f"❌ {service.capitalize()} service is not running on {url}")
            print(f"\n⚠️  Please start all services first!")
            print("   Run: start-all.bat")
            return
    
    time.sleep(1)
    
    # Create sample data
    users = create_users()
    time.sleep(0.5)
    
    accounts = create_accounts(users)
    time.sleep(0.5)
    
    payments = create_payments(accounts)
    time.sleep(0.5)
    
    create_ledger_entries(accounts, payments)
    
    show_summary(users, accounts, payments)

if __name__ == "__main__":
    main()
