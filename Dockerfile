# Use a slim Python base image for efficiency
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Prevent Python from generating .pyc files and enables unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code to container
COPY . /code

# Expose the port your app will run on
EXPOSE 4000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:4000", "application:app"]
