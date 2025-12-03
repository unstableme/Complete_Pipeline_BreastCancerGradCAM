# UnstableMe

This is a full-stack project with a FastAPI backend and a Streamlit frontend, fully containerized using Docker. The project includes CI/CD automation to build, push Docker images, and deploy them automatically on Render (https://render.com). The backend and frontend run in separate Docker containers. GitHub Actions is used to build, push Docker images, and deploy to Render automatically. Docker layer caching is applied to speed up builds, and a safe-dev branch can be used for testing before merging to main.

## Local Setup

To run the project locally using Docker and docker-compose, clone or download the docker-compose.yml file from this repository. Then pull the Docker images using `docker pull unstableme02/idc-frontend:latest` and `docker pull unstableme02/idc-backend:latest`. After that, start the services using `docker-compose up -d`. Ensure the docker-compose.yml file is in your current directory when running this command. Once running, you can access the frontend at http://localhost:8501 and the backend at http://localhost:8000.

## CI/CD Workflow

The CI/CD workflow triggers on push to the main or safe-dev branches. It performs continuous integration (CI) by checking out the repository, building Docker images for frontend and backend, and applying caching for faster rebuilds. Continuous deployment (CD) is performed by pushing Docker images to Docker Hub and triggering deploy hooks on Render, which occurs only for the main branch. Docker images are published under the unstableme02 account. Frontend image: unstableme02/idc-frontend:latest. Backend image: unstableme02/idc-backend:latest.
