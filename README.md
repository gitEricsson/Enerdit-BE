# Enerdit Backend

Enerdit Backend is the server-side component of the Enerdit application, designed to handle user authentication, energy audit data management, and provide a RESTful API for the frontend. It is built using Django and Django REST Framework.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)

## Features

- User authentication with JWT tokens
- Management of energy audit data
- RESTful API for frontend integration
- Support for multiple building types and compartments
- Energy consumption calculations and recommendations

## Technologies Used

- **Django**: A high-level Python web framework for rapid development.
- **Django REST Framework**: A powerful toolkit for building Web APIs.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Django CORS Headers**: For handling Cross-Origin Resource Sharing (CORS).
- **Django Environ**: For managing environment variables.

## Installation

To set up the Enerdit backend, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/enerdit-backend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd enerdit-backend
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the root directory and add the following environment variables:

   ```
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/yourdbname
   ```

7. Run database migrations:

   ```bash
   python manage.py migrate
   ```

8. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

## Usage

To run the application, use the following command:

```bash
python manage.py runserver
```

This will start the development server at `http://127.0.0.1:8000/`.

## API Endpoints

The following are the main API endpoints available:

- **Authentication**

  - `POST /auth/login/`: Log in a user and receive a JWT token.
  - `POST /auth/signup/`: Register a new user.

- **Energy Audit**
  - `POST /energy-audit/`: Create a new energy audit report.

## Database Models

The backend includes the following key models:

- **User**: Represents the user of the application.
- **Building**: Represents a building with attributes like type, number of floors, and energy consumption.
- **Compartment**: Represents a compartment within a building, containing appliances.
- **Appliance**: Represents an appliance with attributes like power rating and usage time.
