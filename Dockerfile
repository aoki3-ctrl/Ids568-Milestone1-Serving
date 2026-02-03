##Use lightweight Python image
FROM python:3.9-slim

##Set working directory inside container
WORKDIR /app

##Copy dependency file first (Docker cache optimization)
COPY requirements.txt .

##Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

##Copy application code
COPY app ./app
COPY model.pkl .

##Expose port (Cloud Run uses 8080)
EXPOSE 8080

##Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
