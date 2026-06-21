FROM python:3.11-slim

# * create project user
RUN adduser --disabled-password --gecos "" imagebinapi-user

WORKDIR /app

# * copy module list and install modules
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# * Copy all files 
COPY . .

# * Change permissions
RUN chmod 755 ./entrypoint.sh

RUN chmod 755 ./entrypoint_test.sh

RUN chmod -R 777 /app ./data

# * API Port
EXPOSE 8000

# * Switch to project user
USER imagebinapi-user

# * Entrypoint file
ENTRYPOINT ["./entrypoint.sh"]
