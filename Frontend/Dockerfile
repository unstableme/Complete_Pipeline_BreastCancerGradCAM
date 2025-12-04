FROM python:3.10-slim

# Install only essential OS dependencies for Streamlit + PIL
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Streamlit + required client packages directly
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir streamlit requests pillow

# Copy all frontend files
COPY ./Frontend/ /app/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
