# ===========================
# Stage 1: Build Stage
# ===========================
FROM python:3.10-slim AS build

# Install minimal packages needed by Streamlit + OS-level deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Install dependencies for frontend only (no cache)
RUN pip install --no-cache-dir streamlit requests

# Copy application source
COPY ./Frontend/ /app/


# ===========================
# Stage 2: Final Runtime Image
# ===========================
FROM python:3.10-slim

# Install only essential runtime OS libs (same as build)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed dependencies from build stage
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy actual frontend code
COPY ./Frontend/ /app/

# Expose Streamlit port
EXPOSE 8501

# Launch Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
