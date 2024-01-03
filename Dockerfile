FROM python:3.10

WORKDIR /app


COPY /src /app/src
COPY requirements.txt /app/.
COPY app.py /app/.
COPY chainlit.md /app/.


RUN pip install -r requirements.txt

CMD ["chainlit", "run", "app.py"]

