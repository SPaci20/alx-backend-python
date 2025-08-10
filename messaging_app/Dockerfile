# Use official Python 3.10 base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port Django runs on (default 8000)
EXPOSE 8000

# Set environment variables to avoid Python buffering and run Django server
ENV PYTHONUNBUFFERED=1

# Run Django development server (adjust if using gunicorn or other)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
