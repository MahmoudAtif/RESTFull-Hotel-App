# # Use an official Python runtime as a parent image
# FROM python:3.10.5-slim-buster

# # Set the working directory to /app
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# COPY . /app

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Set the environment variable for Celery and Celery-Beat
# ENV CELERY_BROKER_URL redis://redis:6379/0
# ENV CELERY_RESULT_BACKEND redis://redis:6379/0

# # Expose the port for the Django server
# # EXPOSE 8000

# # Start the Django server
# # CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt