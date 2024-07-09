FROM python:3.12.4-slim-bullseye
ENV DockerDir=/app/web-server
RUN mkdir -p $DockerDir
WORKDIR $DockerDir
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY . $DockerDir
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]