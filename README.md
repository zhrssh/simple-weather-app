# Simple Weather App

[![CI workflow](https://github.com/zhrssh/simple-weather-app/actions/workflows/ci.yml/badge.svg)](https://github.com/zhrssh/simple-weather-app/actions/workflows/ci.yml)

A simple Flask-based weather application that fetches current weather data using the [OpenWeatherMap API](https://openweathermap.org/api). Built to practice DevOps concepts including containerization, reverse proxying with Traefik, and CI workflows.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Setup](#setup)
  - [Option A: Local (via setup.sh)](#option-a-local-via-setupsh)
  - [Option B: Docker (via Docker Compose)](#option-b-docker-via-docker-compose)
- [Project Structure](#project-structure)
- [License](#license)

---

## Prerequisites

Before running the app, make sure you have the following installed:

| Tool                                  | Version | Purpose                                        |
| ------------------------------------- | ------- | ---------------------------------------------- |
| Python                                | >= 3.12 | Runtime                                        |
| pip                                   | latest  | Bootstraps `uv`                                |
| [uv](https://github.com/astral-sh/uv) | latest  | Dependency management                          |
| openssl                               | any     | Generates self-signed TLS certs (local setup)  |
| apache2-utils                         | any     | Provides `htpasswd` for Traefik dashboard auth |
| Docker + Docker Compose               | latest  | Required for Option B only                     |

> **Note:** `uv` is installed automatically by `setup.sh`. You do not need to install it manually for Option A.

---

## Environment Variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

| Variable            | Description                                                                  |
| ------------------- | ---------------------------------------------------------------------------- |
| `SERVER_SECRET_KEY` | Flask secret key used for session signing                                    |
| `WEATHER_API_KEY`   | Your API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys) |

> **Docker note:** When running via Docker Compose, secrets are loaded from `./secrets/api_key.txt` and `./secrets/server_secret.txt` instead of `.env`. The `setup.sh` script creates these files for you.

---

## Setup

### Option A: Local (via setup.sh)

1. Clone the repository:

   ```bash
   git clone https://github.com/zhrssh/simple-weather-app.git
   cd simple-weather-app
   ```

2. Copy and configure environment variables:

   ```bash
   cp .env.example .env
   # Edit .env and set your WEATHER_API_KEY and SERVER_SECRET_KEY
   ```

3. Run the setup script:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   The script will:
   - Install and upgrade `pip` and `uv`
   - Install dependencies via `uv sync`
   - Create `./secrets/` with placeholder API key and server secret files
   - Generate a self-signed TLS certificate in `./certs/`
   - Optionally generate hashed credentials for the Traefik dashboard

4. Update the generated secret files with your real values:

   ```bash
   echo "your-openweathermap-api-key" > ./secrets/api_key.txt
   echo "your-server-secret" > ./secrets/server_secret.txt
   ```

5. Run the app:

   ```bash
   uv run gunicorn -c ./gunicorn.conf.py "flaskr:create_app()"
   ```

---

### Option B: Docker (via Docker Compose)

1. Clone the repository:

   ```bash
   git clone https://github.com/zhrssh/simple-weather-app.git
   cd simple-weather-app
   ```

2. Run the setup script to generate required secrets and certificates:

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Update the generated secret files with your real values:

   ```bash
   echo "your-openweathermap-api-key" > ./secrets/api_key.txt
   echo "your-server-secret" > ./secrets/server_secret.txt
   ```

4. Start the stack:

   ```bash
   docker compose up -d
   ```

   This starts:
   - **Traefik** — reverse proxy with TLS termination and dashboard at `https://dashboard.gamma.localhost`
   - **weather-app** — Flask app served via Gunicorn at `https://server.gamma.localhost`, with 2 replicas

5. To stop the stack:

   ```bash
   docker compose down
   ```

> **Traefik dashboard:** The default credentials are `admin` / the hashed password generated during `setup.sh`. To change it, update the `basicauth.users` label in `docker-compose.yml`.

---

## Project Structure

```
simple-weather-app/
├── .github/workflows/   # CI pipeline definitions
├── dynamic/             # Traefik dynamic config (TLS settings)
├── flaskr/              # Flask application package
├── .env.example         # Example environment variable file
├── .python-version      # Pinned Python version for uv
├── config.py            # App configuration
├── docker-compose.yml   # Docker stack definition
├── Dockerfile           # Container image definition
├── gunicorn.conf.py     # Gunicorn server configuration
├── pyproject.toml       # Python project metadata and dependencies
├── setup.sh             # Local environment setup script
└── uv.lock              # Locked dependency versions
```

---

## License

This project is licensed under the [MIT License](LICENSE).
