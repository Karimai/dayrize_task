# Use an official Python runtime as the base image
FROM python:3.10.0-alpine

# Set the working directory
WORKDIR /app

# Set the environment variables
ENV PYTHONUNBUFFERED=1

# Update pip and install poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy your poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the project files to the container
COPY . /app/

# Run the makemigrations and migrate commands to create the necessary database tables
RUN python manage.py makemigrations dayrizer_task && \
    python manage.py migrate

# Expose the port that your Django application will be running on
EXPOSE 8000

# Define the command to run the Django application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

