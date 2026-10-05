FROM python:3.11-slim

# Create a non-root user (Required by HuggingFace Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create cache dir for huggingface ML models
ENV HF_HOME=/app/.cache
RUN mkdir -p /app/.cache

# Copy project files
COPY --chown=user . .

# Move into the src directory
WORKDIR /app/src

# HuggingFace expects the app to run on port 7860
ENV PORT=7860
EXPOSE 7860

# Start the server
CMD ["python", "app_server.py"]
