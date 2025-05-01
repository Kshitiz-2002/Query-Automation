# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the .env file into the container (if you have it in your project)
COPY .env /app/.env

# Install the dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8501 for Streamlit app
EXPOSE 8501

# Set the environment variable for Streamlit to run
ENV STREAMLIT_SERVER_HEADLESS=true

# Command to run the app (start Streamlit for the frontend and FastAPI for the backend)
CMD ["streamlit", "run", "your_streamlit_app.py"]  # Update with your Streamlit app filename

