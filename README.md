# 🔒 TrustLock

TrustLock is a **security event monitoring platform** designed to help organizations detect suspicious activity, monitor account usage, and maintain compliance — all through a simple, elegant web dashboard.

<img src="/dashboard/static/dashboard/images/trustlock_logoblanco.png" alt="Logo" width="600"/>

---

## 🚀 Features

- 🔐 User authentication (admin and standard roles)
- 🧾 Create and manage security events
- 📊 Dashboard with charts (bar & pie)
- 🔎 Event filtering by type, date, and keyword
- 📱 Fully responsive (mobile-friendly)
- 📤 Export events to CSV
- 🛡️ Role-based visibility (users only see their events)
- ✨ Clean UI with custom branding

---

## 🏢 Use Cases

- **IT departments** needing traceability for security audits
- **Banks or corporate teams** that track login anomalies or usage patterns
- **Startups or SaaS platforms** required to comply with data protection standards

---

## 🖼️ Screenshots

### 🔐 Login Page
<img src="screenshots/login.png" alt="Login Page" width="600"/>


### 📊 Dashboard
<img src="screenshots/dashboard.png" alt="Dashboard" width="600"/>

### 📋 Events
<img src="screenshots/events.png" alt="Events" width="600"/>

### ➕ Create Events
<img src="screenshots/create_events.png" alt="Create Event" width="600"/>

### 🚪 Logout
<img src="screenshots/logout.png" alt="Logout" width="600"/>

---

## ⚙️ Tech Stack

- Backend: `Django 5`, `SQLite`, `Django Authentication`, `Messages Framework`
- Frontend: `Bootstrap 5`, `Chart.js`, `widget-tweaks`
- Style: blue-gray-white color palette
- Export: `CSV` format

---

## 💻 Local Setup

```bash
git clone https://github.com/SaraPossoP/Trustlock.git
cd trustlock
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
