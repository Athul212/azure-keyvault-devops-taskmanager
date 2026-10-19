
# 🚀 DevOps Task Manager – Azure Key Vault Project

A full-stack task management application deployed on Microsoft Azure, using Azure Key Vault and Managed Identity for secure database credential management.

## 🛠️ Technologies Used

- Microsoft Azure Virtual Machine (Ubuntu)
- NGINX – Web server and reverse proxy
- Python Flask – REST API
- Gunicorn – WSGI application server
- PostgreSQL – Database
- Azure Key Vault – Secret management
- Azure Managed Identity – Secure authentication
- systemd – Application service management
- HTML, CSS and JavaScript – Frontend

## 🏗️ Architecture

Browser
   |
   v
NGINX (Port 80)
   |
   +--> Frontend (HTML/CSS/JavaScript)
   |
   +--> Flask API via Gunicorn (127.0.0.1:5000)
            |
            +--> PostgreSQL (localhost:5432)
            |
            +--> Azure Key Vault
                  (Managed Identity authentication)

## ✨ Features

- Add new tasks
- View saved tasks
- Delete tasks
- Persistent PostgreSQL storage
- Secure database password retrieval from Azure Key Vault
- Automatic application startup using systemd
- NGINX reverse proxy

## 🔐 Security

The PostgreSQL password is stored in Azure Key Vault rather than hardcoded in the application.

The Azure VM uses a system-assigned Managed Identity with the Key Vault Secrets User role to retrieve the password.

PostgreSQL and Flask are accessible locally on the VM, rather than directly from the internet.

**Note:** This is a learning project. HTTPS and application authentication should be configured before public production use.

## 📁 Project Structure

```text
devops-taskmanager/
├── app.py
├── frontend/
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md
```

## 📚 Key Learnings

- Deploying a full-stack application on Azure
- Configuring NGINX as a reverse proxy
- Managing Python applications with Gunicorn and systemd
- Connecting Flask to PostgreSQL
- Using Azure Key Vault to manage secrets
- Authenticating securely with Azure Managed Identity
- Troubleshooting Linux services and networking

## 👨‍💻 Project Type

Hands-on Cloud and DevOps learning project.

