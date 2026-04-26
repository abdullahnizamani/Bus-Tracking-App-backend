# 🚌 Bus Safar — Backend & Admin Dashboard

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Firebase](https://img.shields.io/badge/Firebase-ffca28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)
[![Live](https://img.shields.io/badge/Live%20Dashboard-%E2%86%92-brightgreen?style=for-the-badge)](https://bus-tracking-app-zeta.vercel.app)

The backend and admin dashboard for **Bus Safar** — a real-time university bus tracking system. This repo covers the Django REST API, role-based admin panel, and Firebase integration layer. The mobile app (React Native + Expo) lives [here](https://github.com/abdullahnizamani/Bus-Safar).

---

## Architecture

Two databases, one system. **PostgreSQL** handles persistent relational data — users, buses, routes, assignments. **Firebase Realtime DB** handles high-frequency ephemeral data — live GPS coordinates, speed, trip status — bypassing Django entirely for low latency. The backend bridges them: authenticating users, minting scoped Firebase tokens, and keeping the admin dashboard in sync.

```
Admin Dashboard ──→ Django Backend ──→ PostgreSQL
                          │
                          └─────────→ Firebase RTDB ←── Mobile App
                                                        (Driver/Student)
```

Static assets and avatars are served from **Supabase Storage** via S3-compatible endpoints, keeping Vercel's serverless functions stateless.

---

## Features

**🖥️ Admin Dashboard**
- Fleet management — register, update, and delete buses with Mapbox route assignment
- Role-based access across `Admin`, `Driver`, and `Student` accounts
- Bulk CSV onboarding for students and drivers
- Activity log with severity levels tracking all admin actions
- Live fleet map — monitor all active buses in real time

**📡 REST API**
- Knox token authentication
- Firebase Custom Token generation scoped by role (`student`, `driver`)
- Bus, route, and profile endpoints consumed by the mobile app
- Bus status PATCH endpoint — the trigger point when a driver goes live

---

## Stack

| | |
|---|---|
| Framework | Django 6.0 + Django REST Framework |
| Auth | Knox Tokens + Firebase Custom Tokens |
| Realtime | Firebase Realtime Database |
| Storage | Supabase (S3-compatible) |
| Deployment | Vercel |
| Database | PostgreSQL (prod) · SQLite (dev) |

---

## Getting Started

**Prerequisites:** Python 3.10+, a Firebase project with Realtime DB enabled, a Supabase project with `avatars-bucket` and `static-bucket`.

```bash
git clone https://github.com/abdullahnizamani/Bus-Tracking-App-backend.git
cd Bus-Tracking-App-backend

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create `.env` in the project root. **Never commit this file.**

```env
# Django
DJANGO_SETTINGS_MODULE=BusCore.settings.development
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (production only)
DATABASE_URL=your_postgres_url

# Supabase
SUPABASE_ACCESS_KEY_ID=your_access_key
SUPABASE_SECRET_ACCESS_KEY=your_secret_key
SUPABASE_BUCKET_NAME=avatars-bucket
SUPABASE_STATIC_BUCKET_NAME=static-bucket
SUPABASE_REGION=your_region
SUPABASE_ENDPOINT_URL=https://<project-ref>.supabase.co/storage/v1/s3
SUPABASE_PROJECT_REF=your_project_ref

# Firebase Admin (base64 encoded service account JSON)
FIREBASE_SERVICE_ACCOUNT=your_base64_service_account
```

> For local dev, drop `serviceAccountKey.json` in the project root — it gets picked up automatically when running with development settings.

```bash
python manage.py migrate
python manage.py createsuperuser
DJANGO_SETTINGS_MODULE=BusCore.settings.development python manage.py runserver
```

Visit `http://127.0.0.1:8000/dashboard/login`

---

## Database Schema

| Model | Description |
|---|---|
| `users.User` | Custom `AbstractUser` with role field (`admin`, `driver`, `student`) |
| `users.Student` | 1-to-1 with User — `student_id`, home coordinates, assigned bus |
| `users.Driver` | 1-to-1 with User — `employee_id`, `license_id` |
| `transport.Bus` | Registration, capacity, active status, linked driver |
| `transport.Route` | 1-to-1 with Bus — GeoJSON path and route description |
| `dashboard.ActivityLog` | Audit trail with severity levels |

---

## CSV Upload Format

First row is treated as a header and skipped.

```
# Students
first_name, last_name, email, phone, student_id, bus_id

# Drivers  
first_name, last_name, email, phone, employee_id, license_id
```

---

## License

This project is licensed under the **MIT License** — you're free to use, modify, and distribute it. See the [LICENSE](LICENSE) file for details.

---

Built by [Abdullah Nizamani](https://github.com/abdullahnizamani)