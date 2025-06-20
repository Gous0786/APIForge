# Use the official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

ENV PORT=8080
ENV PYTHONUNBUFFERED=TRUE

# Run the Flask app
CMD exec gunicorn --bind :$PORT app:app
