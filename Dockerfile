# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Expose the port your app will run on (e.g., 8000)
EXPOSE 8000

# Define the command to run your application
CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]