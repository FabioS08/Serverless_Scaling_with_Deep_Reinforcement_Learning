# Use a lightweight base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your application code to the container
COPY . /app

# Install any needed dependencies (make sure you have a requirements.txt if using Python)
RUN pip install --no-cache-dir -r requirements.txt

# Create results directory
RUN mkdir -p results

# Define the command to run your matrix multiplication program
CMD ["python", "matrixMultiplication.py"]