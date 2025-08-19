# Base image
FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Copy everything
COPY . /app

# Install system deps
RUN apt-get update && apt-get install -y build-essential

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
