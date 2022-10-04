FROM python:3
WORKDIR /usr/src/app
RUN pip install --upgrade pip
EXPOSE 8565

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY

CMD [ "python", "bash", "deploy.sh" ]