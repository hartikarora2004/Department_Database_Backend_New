FROM node:alpine
COPY . /app
WORKDIR /app
CMD python -m venv env && source env/bin/activate && pip install -r requirements.txt && 