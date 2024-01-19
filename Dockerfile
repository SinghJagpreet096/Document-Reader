FROM python:3.10

WORKDIR /app


COPY /src /app/src
COPY requirements.txt /app/.
COPY app.py /app/.
COPY chainlit.md /app/.

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt update && apt install -y ffmpeg

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

EXPOSE 7860

CMD ["chainlit", "run", "app.py"]

