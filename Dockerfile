FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Pixi
RUN curl -fsSL https://pixi.sh/install.sh | bash && \
    mv /root/.pixi/bin/pixi /usr/local/bin/pixi && \
    pixi --version

# Copy Pixi configuration
COPY pixi.toml /app/pixi.toml

# Install dependencies for both environments
RUN pixi install && pixi install -e frontend

# Add frontend environment binaries to PATH
ENV PATH="/app/.pixi/envs/frontend/bin:$PATH"

# Copy application code
COPY . /app

# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Start supervisord to manage both services
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
