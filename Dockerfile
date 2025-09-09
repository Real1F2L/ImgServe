FROM python:3

# set working dir
WORKDIR /app

# install requirments
RUN pip install --no-cache-dir -r requirements.txt

# run script
CMD ["python", "-u", "main.py"]