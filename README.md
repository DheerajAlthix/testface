

## Project Overview
This project is a backend system built using Django and Django REST Framework (DRF).and i have already setup data base of postgreSQL access from Neon server.
## Tech StackN
- **Django**: Web framework
- **Django REST Framework**: API development
- **PostgreSQL**: Database
- **Google OAuth2**: Social authentication

## Installation and Setup

### Prerequisites
- Python
- PostgreSQL

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/backend.git
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate (optional because i  have configure in this repo)
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser (optional because i  have configure in this repo)
   ```

7. Start the Django server:
   ```bash
   python manage.py runserver
   ```
8. replace example.env to .env

## API Endpoints

### Authentication
- **Login with Google**: `POST /auth/google/login/`
- **JWT Token Refresh**: `POST /auth/token/refresh/`

### User Profile
- **Get Profile**: `GET /user-profile/`
- **Update Profile**: `PUT /user-profile/`


# backenAltix
# backenAltix
