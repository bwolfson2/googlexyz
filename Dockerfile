# syntax=docker/dockerfile:1
FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /requirements.txt
COPY ./app /app
WORKDIR /app
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    /py/bin/python -m spacy download en_core_web_sm 
ENV PATH="/py/bin:$PATH"
ENV PORT=8080
#CMD python manage.py runserver 0.0.0.0:8000
CMD exec gunicorn --bind :$PORT --workers 1 --threads 2 --chdir app/ app.wsgi:application --timeout 6000 --preload
