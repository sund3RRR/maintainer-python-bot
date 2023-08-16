# Use the official Python image as the base image
FROM python:3.10

# Set working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV githubToken=<TOKEN>
ENV tgToken=<TOKEN>

# Specify the command to run Python application
CMD ["python", "src/run.py"]
