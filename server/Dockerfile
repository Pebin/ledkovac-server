FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1

COPY . .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5600

ENTRYPOINT ["./gunicorn.sh"]
