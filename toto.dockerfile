FROM python:3.11-slim


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN chmod 755 ./entrypoint.sh

RUN chmod 755 ./entrypoint_test.sh

RUN chmod -R 777 /app ./data


EXPOSE 8000



ENTRYPOINT ["./entrypoint_test.sh"]
