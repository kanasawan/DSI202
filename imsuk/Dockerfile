FROM python:3.9-slim

# Install system dependencies (รวมของ Pillow ด้วย)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Make sure entrypoint is executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# Run app
CMD ["/bin/bash", "entrypoint.sh"]
