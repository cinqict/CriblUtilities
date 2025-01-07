# Use an official Python image as the base
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files to reduce image size
COPY pyproject.toml poetry.lock ./

# Install Poetry to manage dependencies
RUN pip install poetry && poetry install --no-root

# Copy the rest of the project files
COPY . .

# Create directories where users can mount their config and env folders
RUN mkdir -p /app/env /app/config

# Set the default command to run the CLI
CMD ["cribl-utilities-cli"]
