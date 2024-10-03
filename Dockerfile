FROM python:3.11-slim

WORKDIR /pet-project
COPY requirements.txt ./
RUN pip install --upgrade -r requirements.txt
COPY pet-project ./
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && gunicorn main:main_app"]