FROM python:3.12.2-slim-bookworm

WORKDIR /app
COPY requirement.txt requirement,txt

RUN python3  -m pip install -r requirement.txt

COPY . .


CMD ["python3","manage.py","runserver","0.0.0.0:8000"]