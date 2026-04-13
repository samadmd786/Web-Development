# Web Development

A **Flask** + **Flask-SocketIO** web application with real-time WebSocket support, MySQL database integration, and full Docker containerization for both development and production environments.

## Features

| Feature | Description |
|---------|-------------|
| **Real-Time WebSockets** | Bidirectional communication via Flask-SocketIO and eventlet |
| **Docker Ready** | Separate `Dockerfile` and `Dockerfile-dev` for prod and dev |
| **Docker Compose** | One-command local startup with `docker-compose up` |
| **MySQL Integration** | Database support via `mysql-connector-python` |
| **Gunicorn** | Production-grade WSGI server included |
| **Flask-Failsafe** | Safer hot-reloading during development |
| **App Factory Pattern** | Modular Flask structure via `flask_app/create_app` |

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- *Or* Python 3.x + a running MySQL instance for local setup

### Running with Docker *(Recommended)*

```bash
# Clone the repo
git clone https://github.com/samadmd786/Web-Development.git
cd Web-Development

# Build and start
docker-compose up --build
```

Navigate to **http://localhost:8080** in your browser.

### Running Locally *(without Docker)*

```bash
pip install -r requirements.txt
python app.py
```

> Configure your MySQL connection settings in the Flask app config before running locally.

### Dev Mode *(with hot-reloading)*

```bash
docker build -f Dockerfile-dev -t web-dev .
docker run -p 8080:8080 web-dev
```

## Project Structure

| Path | Description |
|------|-------------|
| `app.py` | Application entry point — initializes SocketIO and runs the server |
| `flask_app/` | App factory, routes, and SocketIO event handlers |
| `Dockerfile` | Production container image |
| `Dockerfile-dev` | Development container with live reload |
| `docker-compose.yml` | Multi-container orchestration config |
| `requirements.txt` | Python dependencies |

## Tech Stack

- **Language:** Python 3.x
- **Framework:** [Flask](https://flask.palletsprojects.com/) + [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- **Database:** MySQL via `mysql-connector-python`
- **Real-Time:** eventlet
- **Server:** Gunicorn (production)
- **Containerization:** Docker, Docker Compose
