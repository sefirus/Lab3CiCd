FROM ubuntu:latest
LABEL authors="Sashs"

FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the Django app runs on
EXPOSE 8000

# Start the Django app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT