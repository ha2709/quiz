# Use an official Python base image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements file to the working directory
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . ./


# Hardcoded DATABASE_URL_SYNC
ENV DATABASE_URL_SYNC=postgresql+psycopg2://postgres:1234@192.168.1.7:5432/quiz

# Expose the application port
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
