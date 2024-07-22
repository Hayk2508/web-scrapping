ENV DockerDir=/app/web-server
WORKDIR $DockerDir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["gunicorn", "web-server.core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]

