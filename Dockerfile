# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for both services
EXPOSE 8000 8501

# Command to run both FastAPI and Streamlit
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port 8000 & streamlit run main.py --server.port 8501"]
