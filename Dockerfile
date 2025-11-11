# Use Python 3.11 slim
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the entire repository into the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Set working directory to where server.py and util.py live
WORKDIR /app

# Run the Flask server
CMD ["python", "server.py"]
