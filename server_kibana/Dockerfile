FROM python:3.9-alpine

COPY . .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5050

CMD ["python", "main.py"]
