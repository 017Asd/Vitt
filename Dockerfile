FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends gcc libffi-dev libssl-dev libjpeg-dev zlib1g-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --retries=10 --no-cache-dir --trusted-host pypi.org --trusted-host pypi.pythonhosted.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app/app.py"]
