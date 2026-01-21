FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY api/requirements.txt /app/api/requirements.txt
RUN pip install --no-cache-dir -r /app/api/requirements.txt

# Copy API
COPY api/ /app/api/

# Copy Frontend
COPY frontend/ /app/frontend/

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app/api && uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
cd /app/frontend && python -m http.server 3000 --bind 0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

# Update frontend to use correct API URL (same host, port 8000)
RUN sed -i "s|http://localhost:8000|http://localhost:8000|g" /app/frontend/js/app.js

# Expose ports
EXPOSE 8000 3000

# Start both services
CMD ["/bin/bash", "/app/start.sh"]
