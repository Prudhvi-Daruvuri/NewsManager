FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make pywsgi.py executable
RUN chmod +x pywsgi.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using our pywsgi.py
CMD ["python", "pywsgi.py"]