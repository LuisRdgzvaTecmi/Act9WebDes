# Activity 9 - Custom Authentication System

A Django web application implementing a fully custom authentication system utilizing SHA-256 password hashing and token-based session management, completely replacing Django's built-in authentication mechanisms.

## Features

- **Custom User Model**: A lightweight customized user model designed specifically for this project.
- **SHA-256 Password Hashing**: Passwords undergo secure SHA-256 cryptography before storage, bypassing Django's default hasher.
- **Token-Based Authentication**: A unique cryptographic token is issued upon successful login and persists within the session.
- **Custom Middleware**: Every request passes through a specialized middleware that verifies the session token and fetches the corresponding authorized user context.
- **Landing Page**: A distinct interface exclusive to guest users. Redirects authenticated users.
- **Secure Dashboard**: A private user dashboard containing personal information, only accessible to authenticated individuals with active tokens.
- **Dynamic Navigation System**: The top navbar intelligently switches displayed options and views based on the user's active login state.

## Tech Stack

- Python
- Django
- SQLite3 (Default database)
- Vanilla CSS
- python-dotenv

## Setup & Installation

Follow these steps to deploy the application locally:

1. **Clone or download the repository.**

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add the required environmental variables, such as:
   ```env
   SECRET_KEY=your-secure-django-secret-key
   ```

5. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open a web browser and navigate to `http://127.0.0.1:8000/`.

## Architecture Overview

- `models.py`: Contains the `CustomUser` and `AuthToken` definitions.
- `middleware.py`: Integrates `TokenAuthMiddleware` which manages token verification during request/response lifecycles.
- `views.py`: Dedicated views logic regulating guest privileges (`landing_page`, `register`, `login`) versus authorized privileges (`dashboard`).
- `style.css`: All user interface layouts, modernized with custom gradients, SVG assets, and a responsive structure.
