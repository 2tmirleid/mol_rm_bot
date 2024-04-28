# Chose the python version you need
FROM python:3.12-alpine

WORKDIR /app

# Copy txt file with dependencies
COPY requirements.txt ./

# Install dependencies
RUN pip3 install -r requirements.txt

# Copying all app dirs/files
COPY . .

CMD ["python3", "main.py"]