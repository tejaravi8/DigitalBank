## 🏦 Digital Bank Management System

A full-stack Digital Banking application built using Django, Django REST Framework, HTML, CSS, and JavaScript.
This project simulates real-world banking operations with secure authentication, role-based access, and transaction handling.

## 🚀 Features Overview
### 👤 User Features

- User Registration & Login (Token-based Authentication)

- Profile Management

- KYC Status Handling (Pending / Approved / Rejected)

- Account Overview (Savings / Current)

- Balance Tracking

- Money Transfers:

- Send to Bank Account

- Send to Mobile Number

- Internal Account Transfers

- Secure Operations (Blocked when KYC not approved)

### 🛠️ Admin Features

- Admin Login

- User Management (Activate / Deactivate Users)

- KYC Approval System

- Account Management

- Admin Credit / Debit (Bank Pool Concept)

- Reports-ready backend structure

## 🧱 Tech Stack
- Backend

- Python

- Django

- Django REST Framework

- SQLite (can be switched to PostgreSQL/MySQL)

- Frontend

- HTML5

- CSS3

- JavaScript (Fetch API)

- Authentication

- Token-based Authentication (DRF TokenAuth)

## 🧩 Project Structure
```
Digital_Bank/
│
├── banking/
│   ├── api/
│   │   ├── transfers.py
│   │   ├── serializers.py
│   │   └── views.py
│   │
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│
├── templates/
│   └── banking/
│       ├── dashboard.html
│       ├── profile.html
│       ├── transfers.html
│       └── settings.html
│
├── bank_proj/
│   └── settings.py
│
└── manage.py
```

## 🔐 Authentication Flow

- Users authenticate using username & password

- On successful login, a token is generated

- Token is stored in localStorage

- All protected APIs require:

- Authorization: Token <user_token>

## 🔄 Money Transfer Logic

- Transfers are atomic using database transactions

- Balance updates are safely handled with rollback protection

- Each transfer creates debit and credit records

- KYC approval is required before transfers

## 📌 Current Status

✅ Core banking features implemented <br>
✅ Admin & User workflows completed <br>
✅ Secure backend logic <br>
⏸️ Transaction history UI & analytics planned for future versions

The project focuses on stability and core banking operations rather than overloading features.

## 🧪 How to Run Locally

### Clone repository
```
git clone https://github.com/tejaravi8/Digital_Bank.git
cd Digital_Bank
```
### Create virtual environment
```
python -m venv bank
bank\Scripts\activate   # Windows
```
### Install dependencies
```
pip install django djangorestframework
```
### Migrate database
```
python manage.py migrate
```
### Create superuser
```
python manage.py createsuperuser
```
### Run server
```
python manage.py runserver
```

Visit:
```
👉 http://127.0.0.1:8000/dashboard/
```
## 🎯 Learning Outcomes

- Django REST Framework API design

- Token-based authentication

- Role-based access control

- Atomic database transactions

- Frontend–Backend integration

- Real-world banking logic simulation

## 📌 Future Enhancements

- Transaction History UI

- CSV / PDF Statement Export

- Analytics & Charts

- Email Notifications

- Improved Admin Reports

## 👨‍💻 Author

**Teja Raviteja**
<br><br>
Aspiring Backend / Full Stack Developer

### Social :
🔗 GitHub:  [tejaravi8](https://github.com/tejaravi8) <br>
🔗 LinkedIn: [ravitejabotsa](https://www.linkedin.com/in/ravitejabotsa) <br>
🔗 Instagram: [teja41863](https://github.com/tejaravi8)
