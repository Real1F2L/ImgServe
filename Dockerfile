FROM python:3

WORKDIR /app

# Copy requirements file in and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into /app
COPY . .

# run script
CMD ["python", "-u", "main.py"]