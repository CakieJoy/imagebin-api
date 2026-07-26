FROM python:3.11-slim


# install gosu
RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" imagebin


WORKDIR /app

# * copy module list and install modules
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# * Copy all files 
COPY . .

# * Change permissions
RUN chmod +x ./entrypoint.sh ./Tests/entrypoint_test.sh


# * API Port
EXPOSE 8000


# * Entrypoint file
ENTRYPOINT ["./Tests/entrypoint_test.sh"]
