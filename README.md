This is a full-stack project with a FastAPI backend and a Streamlit frontend, fully containerized using Docker. The project includes CI/CD automation to build, push Docker images, and deploy them automatically on [Render](https://render.com).

## Features

- **Containerized Applications:** Backend and frontend run in separate Docker containers.
- **CI/CD Automation:** GitHub Actions builds, pushes Docker images, and deploys to Render automatically.
- **Docker Hub Integration:** Images are published under `unstableme02` account.
- **Caching for Faster Builds:** Docker layer caching is used to speed up image building.
- **Multi-Branch Support:** Safe-dev branch can be used for testing before merging to main.

---

## Getting Started (Local Setup)

You can run the project locally using Docker and `docker-compose`:

1. **Clone or Download `docker-compose.yml`** from this repository.

2. **Pull Docker Images:**

```bash
docker pull unstableme02/idc-frontend:latest
docker pull unstableme02/idc-backend:latest

Start services:
 docker compose up -d
Make sure to have yml file location and the current directory same in order to run this command.

Access the Application:

Frontend: http://localhost:8501
Backend: http://localhost:8000


CI/CD Workflow Overview

Trigger: On push to main or safe-dev branches.

CI Steps:

Checkout repository

Build Docker images for frontend and backend

Apply caching for faster rebuilds

CD Steps:

Push Docker images to Docker Hub

Trigger deploy hooks on Render (only for main branch)

Docker Hub

Frontend: unstableme02/idc-frontend:latest

Backend: unstableme02/idc-backend:latest
