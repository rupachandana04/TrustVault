# TrustVault – Secure Document Sharing System

## 1. Project Overview

TrustVault is a secure document sharing web application developed using Python and Django.

It allows users to upload, manage, download, and share documents with other registered users based on permissions.

## 2. Objectives

- Provide secure user authentication.
- Allow users to upload and download documents.
- Manage document access permissions.
- Maintain an audit log of important activities.
- Protect documents from unauthorized access.

## 3. Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML
- **Database:** SQLite
- **Version Control:** Git and GitHub

## 4. Main Features

1. User Login and Authentication
2. Document Upload
3. Document Download
4. My Documents
5. Document Sharing
6. Read and Edit Permissions
7. Audit Logging
8. Django Admin Management
9. File Extension and Size Validation

## 5. Security Features

- Login protection for document operations.
- Document ownership verification.
- Permission-based document access.
- File extension validation.
- Maximum file size validation (5 MB).
- Audit logging for important activities.
- Environment variable-based Django secret key configuration.

**Note:** File extension validation is implemented. Additional file-content validation and production security hardening are planned.

## 6. Project Structure

```text
TrustVault/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── documents/
│   ├── migrations/
│   ├── templates/
│   │   └── documents/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── manage.py
├── .gitignore
└── README.md
```

## 7. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/rupachandana04/TrustVault.git
cd TrustVault
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the environment (Windows PowerShell)

```powershell
.\venv\Scripts\Activate
```

### Step 4: Install Django

```bash
pip install Django==5.2.19
```

### Step 5: Configure the secret key

Generate a secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set the generated key as an environment variable:

```powershell
$env:DJANGO_SECRET_KEY = "paste-your-generated-key-here"
```

### Step 6: Apply migrations

```bash
python manage.py migrate
```

### Step 7: Create an admin account

```bash
python manage.py createsuperuser
```

### Step 8: Run the development server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## 8. Project Status

Completed and Deployed. Security testing, documentation, and production deployment are part of the ongoing work.

## 9. Repository

https://github.com/rupachandana04/TrustVault