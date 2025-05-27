FROM python:3.9-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (default Flask)
EXPOSE 5000

# Jalankan Flask dengan gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api.index:app"]
