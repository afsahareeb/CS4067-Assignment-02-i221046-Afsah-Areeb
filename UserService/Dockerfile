# Use a minimal Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy dependency file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the service port
EXPOSE 8001

# Define the startup command
CMD ["uvicorn", "user_main:app", "--host", "0.0.0.0", "--port", "8001"]
