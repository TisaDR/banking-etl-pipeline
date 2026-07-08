# base image — Python 3.13
FROM python:3.13-slim

# set working directory inside container
WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy all your scripts
COPY . .

# command to run when container starts
CMD ["python", "etl_pipeline.py"]