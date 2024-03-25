# Chose the python version you need
FROM python:3.12-alpine

WORKDIR /app

# Copy txt file with dependencies
COPY requirements.txt ./

# Creating virtual environment
RUN python3 -m venv venv
# Activate virtual environment
RUN source venv/bin/activate
# Install dependencies
RUN pip3 install -r requirements.txt

# Copying all app dirs/files
COPY . .

CMD ["python3", "src/main.py"]