FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    tcpdump \
    net-tools \
    iputils-ping \
    iproute2 \
    lftp \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir scapy

# Set working directory
WORKDIR /app

# Copy the inquisitor script
COPY inquisitor /app/inquisitor
RUN chmod +x /app/inquisitor

# Keep container running
CMD ["/bin/bash"]
