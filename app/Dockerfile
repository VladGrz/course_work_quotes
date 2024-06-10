FROM python:3.8-slim

WORKDIR /app

COPY . /app
RUN pip install flask pydantic requests

CMD ["python", "main.py"]