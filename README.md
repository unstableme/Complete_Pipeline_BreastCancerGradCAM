This is a full-stack project with a **FastAPI backend** and a **Streamlit frontend**, fully containerized using **Docker**. The project includes **CI/CD automation** to build, push Docker images, and deploy them automatically on [Render](https://render.com).

In this project, I have used custom-27 layers **Convolutional Neural Networks (CNN)** to train the model on breast cancer histopathology images especially for **Invasive Ductal Carcinoma (IDC)** subtype. Along with that, I have used **Grad-CAM interpretability** to show how the model made such predictions. To see the demo, you can visit here: https://idc-frontend-latest.onrender.com/

## ✨ Features

* **Containerized Applications:** Backend and frontend run in separate Docker containers.
* **CI/CD Automation:** GitHub Actions builds, pushes Docker images, and deploys to Render automatically.
* **Docker Hub Integration:** Images are published under the `unstableme02` account.
* **Caching for Faster Builds:** Docker layer caching is used to speed up image building.
* **Multi-Branch Support:** `safe-dev` branch can be used for testing before merging to `main`.

---

## 🚀 Getting Started (Local Setup)

You can run the project locally using Docker and `docker-compose`:

1.  **Clone or Download `docker-compose.yml`** from this repository.

2.  **Pull Docker Images:**

```bash
docker pull unstableme02/idc-frontend:latest
docker pull unstableme02/idc-backend:latest
````

3.  **Start Services:**
    Make sure to have the `yml` file location and the current directory the same in order to run this command.

<!-- end list -->

```bash
docker compose up -d
```

4.  **Access the Application:**

<!-- end list -->

  * **Frontend:** `http://localhost:8501`
  * **Backend:** `http://localhost:8000`

-----

## ⚙️ CI/CD Workflow Overview

**Trigger:** On push to `main` or `safe-dev` branches.

### CI Steps:

1.  Checkout repository
2.  Build Docker images for frontend and backend
3.  Apply caching for faster rebuilds

### CD Steps:

1.  Push Docker images to Docker Hub
2.  Trigger deploy hooks on Render (only for `main` branch)

-----

## 🐳 Docker Hub

  * **Frontend:** `unstableme02/idc-frontend:latest`
  * **Backend:** `unstableme02/idc-backend:latest`
