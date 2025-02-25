# AI Startup Idea Generator

## Link to GitHub
https://github.com/themugiwaraya/Final_Back_End.git

This is a Flask-based web application that generates startup ideas using AI (Ollama). The project includes user authentication, idea generation, history tracking, and feedback management.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Local Installation](#local-installation)
  - [Environment Variables Configuration](#environment-variables-configuration)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
  - [Deploying on Render](#deploying-on-render)
  - [Connecting to MongoDB Atlas](#connecting-to-mongodb-atlas)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Frontend](#frontend)

## Features

- **User Authentication**: Secure registration and login using JWT.
- **Idea Generation**: Integration with Ollama to generate startup ideas based on user preferences and selected categories.
- **Idea and Feedback History**: Users can view past generated ideas and leave feedback.
- **MongoDB Atlas Support**: Cloud-based database storage.

## Technologies

- **Flask** – Web framework for Python.
- **Flask-PyMongo** – MongoDB integration.
- **Flask-JWT-Extended** – JWT-based authentication.
- **Gunicorn** – WSGI server for production.
- **python-dotenv** – Environment variable management.

## Installation and Setup

### Prerequisites

- Python 3.8+
- Git
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (or local MongoDB)
- (Optional) Docker for deploying Ollama

### Local Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables Configuration

Create a `.env` file in the root directory and add the following variables:

```env
MONGO_URI="mongodb+srv://yourusername:yourpassword@yourcluster.mongodb.net/ai_startup_db?retryWrites=true&w=majority"
JWT_SECRET_KEY="your_secret_key"
OLLAMA_URL="http://localhost:11434/api/generate"
```

Replace `yourusername`, `yourpassword`, `yourcluster`, and `your_secret_key` with your actual values.

## Running the Application

Run the application with:

```bash
python run.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Deployment

### Deploying on Render

1. **Prepare the project:**

   ```bash
   pip freeze > requirements.txt
   ```

2. **Create a `Procfile` in the root directory:**

   ```Procfile
   web: gunicorn run:app
   ```

   If using `start.sh`, then:

   ```Procfile
   web: ./start.sh
   ```

3. **(Optional) Create `start.sh` script**

   ```bash
   #!/bin/bash
   gunicorn -w 4 -b 0.0.0.0:$PORT run:app
   ```

   Make it executable:

   ```bash
   chmod +x start.sh
   ```

4. **Push the project to GitHub.**

5. **Create a web service on Render:**

   - Go to [Render Dashboard](https://render.com/) and click `New Web Service`.
   - Select the GitHub repository.
   - Configure settings:
     - `Build Command`: `pip install -r requirements.txt`
     - `Start Command`: `gunicorn run:app` (or `./start.sh` if using a script)
     - `Region`: Choose the closest to your users (e.g., Frankfurt)
     - `Plan`: Free (or another plan if more resources are needed)
   - Add environment variables:
     - `MONGO_URI`
     - `JWT_SECRET_KEY`
     - `OLLAMA_URL` (if applicable)
   - Click `Create Web Service` and wait for deployment.

## Connecting to MongoDB Atlas

Ensure the `MONGO_URI` environment variable contains the correct MongoDB Atlas connection string. If set up correctly, all data will be stored in the cloud database.

## API Endpoints

- `POST /register` – User registration
- `POST /login` – User login
- `POST /generate-idea` – Generate an idea
- `GET /my-ideas` – Get idea history
- `DELETE /my-ideas` – Delete idea history
- `POST /feedback` – Submit feedback
- `GET /my-feedback` – Get feedback history
- `GET /categories` – Get available categories
- `POST /categories` – Add a new category

## Project Structure

```bash
ai_startup/
├── app/
│   ├── __init__.py        # Initialize Flask and extensions
│   ├── config.py          # Environment-based configuration
│   ├── models.py          # MongoDB models
│   ├── routes.py          # API endpoints
│   ├── helpers.py         # Hash password
│   └── services/
│       └── ollama_service.py  # Ollama API integration
├── frontend/              # Frontend files
│   ├── img/               # Images
│   ├── feedback.html      # Feedback page
│   ├── index.html         # Main page
│   ├── login.html         # Login page
│   ├── my-ideas.html      # User's idea history
│   ├── register.html      # Registration page
│   ├── script.js          # Frontend JavaScript
│   ├── styles.css         # Main CSS file
│   ├── styles1.css        # Additional CSS file
├── .env                   # Environment variables (not in repository)
├── Procfile               # Render deployment file
├── requirements.txt       # Project dependencies
├── run.py                 # Entry point
└── start.sh               # Startup script (optional)
```

## Frontend

The project includes a simple frontend built with HTML, CSS, and JavaScript:

- `index.html` – Main landing page.
- `login.html` – User login page.
- `register.html` – User registration page.
- `my-ideas.html` – Displays saved startup ideas.
- `feedback.html` – Page for submitting feedback.
- `script.js` – Handles UI interactions and API requests.
- `styles.css` – Main styles for the frontend.
- `styles1.css` – Additional styling.
- `img/` – Directory for images.

The frontend interacts with the backend via RESTful API calls.

