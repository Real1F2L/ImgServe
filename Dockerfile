FROM python:3

# set working dir
WORKDIR /app/
# copy files into container
COPY . .

# install requirments
RUN pip install --no-cache-dir -r requirements.txt

# run script
CMD ["python", "-u", "Scripts/__init__.py"]