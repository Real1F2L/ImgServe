FROM python:3

# set working dir
WORKDIR /app

# Dockerfile runs before docker-compose volumes are made, so we need to copy requirements.txt in here
COPY requirements.txt .

# install requirments
RUN pip install --no-cache-dir -r requirements.txt

# run script
CMD ["python", "-u", "main.py"]