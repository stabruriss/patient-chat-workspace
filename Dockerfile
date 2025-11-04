# Use Python 3.11 official image
FROM python:3.11-slim

# Install Node.js and npm (required for Claude Code CLI)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Claude Code CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Copy and set executable permission for start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Start command - use bash script for proper env var handling
CMD ["/app/start.sh"]
