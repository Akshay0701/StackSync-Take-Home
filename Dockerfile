FROM python:3.10-slim

# Install Python dependencies
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./

EXPOSE 8080
CMD ["python", "app.py"]