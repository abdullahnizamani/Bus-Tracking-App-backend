
# 🚌 BusNaama Backend | Real-Time Transit Management System

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Firebase](https://img.shields.io/badge/firebase-ffca28?style=for-the-badge&logo=firebase&logoColor=black)](https://firebase.google.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

The official backend and administrative dashboard for **BusNaama**, a real-time university bus tracking and fleet management application. This system serves as the central hub for managing students, drivers, and transit routes, while seamlessly integrating with Firebase to orchestrate live GPS tracking.

## 🌟 Key Features

### 👨‍💻 Administrative Dashboard
- **Fleet Management:** Register, update, and delete buses. Assign specific routes with Mapbox geospatial coordinates.
- **Role-Based Access Control (RBAC):** Secure models and views differentiating between `Admin`, `Driver`, and `Student` accounts.
- **Bulk Onboarding (CSV):** Instantly upload and assign hundreds of students or drivers to their respective buses using CSV file parsing.
- **System Activity Logging:** Track all administrative actions (e.g., "Bus Registered", "Bulk Students Added") with a built-in audit trail.

### 📡 Real-Time Tracking Architecture
- **Firebase Bridge:** Acts as the source of truth for trip statuses. When an admin or driver initiates a trip, Django securely updates the Firebase Realtime Database.
- **Live Map Dashboard:** An integrated web view for admins to monitor the live locations of all active buses fleet-wide.
- **Custom Token Authentication:** Generates secure Firebase Custom Tokens for authenticated Django users to restrict database access.

---

## 🏗️ System Architecture



The backend utilizes a **Dual-Stream Data Model** to ensure scalability and low latency:
1. **PostgreSQL/SQLite (Django ORM):** Handles persistent, relational data (User profiles, Bus assignments, Route waypoints, Passwords).
2. **Firebase Realtime DB:** Handles high-frequency, ephemeral data (Live GPS coordinates, Speed, Active trip status).
---

## 🗄️ Core Database Schema

- **`users.User`**: Custom user model extending Django's `AbstractUser`, handling role-based access (Student, Driver, Admin).
- **`users.Student`**: Linked 1-to-1 with `User`; contains `student_id`, home coordinates, and assigned `bus`.
- **`users.Driver`**: Linked 1-to-1 with `User`; contains `employee_id` and `license_id`.
- **`transport.Bus`**: Contains registration details, capacity, active status, and is strictly linked to a `Driver`.
- **`transport.Route`**: Linked 1-to-1 with `Bus`; stores the GeoJSON/Coordinate `path` and string description for the transit route.
- **`dashboard.ActivityLog`**: System audit trail tracking administrative actions, user events, and severity levels.

---
## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- pip & virtualenv
- A Firebase Project (with Realtime Database enabled)

### 2. Local Installation

```bash
# Clone the repository
git clone [https://github.com/abdullahnizamani/Bus-Tracking-App-backend.git](https://github.com/abdullahnizamani/Bus-Tracking-App-backend.git)

# Navigate into the project directory
cd Bus-Tracking-App-backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

```

### 3. Environment Variables

Create a `.env` file in the root directory for your Django secrets. **Never commit this file to version control.**

```env
# Django Settings
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=[*]

```

*(Note: You will also need your `serviceAccountKey.json` from Firebase Admin placed in BusCore or configured via env variables so Django can communicate with Firebase securely).*

### 4. Frontend Firebase Setup

To enable the live map in the Django admin dashboard, you must provide your Firebase client configuration.

Open your `firebase-buses.js` file (located in your static files folder) and update the `firebaseConfig` object with your details:

```javascript
const firebaseConfig = {
  apiKey: "your_api_key_here",
  authDomain: "your_project.firebaseapp.com",
  databaseURL: "https://your_project-default-rtdb.firebaseio.com",
  projectId: "your_project_id",
  storageBucket: "your_project.appspot.com",
  messagingSenderId: "your_sender_id",
  appId: "your_app_id"
};

```

### 5. Database Setup & Run

```bash
# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser for the admin panel
python manage.py createsuperuser

# Run the development server
python manage.py runserver

```

Visit `http://127.0.0.1:8000` to access the login screen.

---

## 📂 CSV Bulk Upload Format

To use the bulk upload feature for Students or Drivers, ensure your CSV headers match the following format exactly. The system skips the first row assuming it is a header.

**For Students:**
`first_name, last_name, email, phone, student_id, bus_id`

**For Drivers:**
`first_name, last_name, email, phone, employee_id, license_id`

---

## 🛡️ Security

* **API Key Restrictions:** Since the Firebase configuration is stored directly in the frontend JavaScript, ensure your `apiKey` is restricted via the Google Cloud Console to only accept requests from your authorized domains (e.g., your production URL and localhost).
* **Route Protection:** All dashboard views are strictly protected by `@login_required` and staff-level authorization checks.
* **Password Hashing:** Handled securely via Django's `make_password` and standard PBKDF2 algorithms.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

