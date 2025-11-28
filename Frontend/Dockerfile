FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip

# Install only what the frontend actually needs
RUN pip install --no-cache-dir streamlit requests

COPY ./Frontend/ /app/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
