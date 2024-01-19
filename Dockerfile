FROM python:3.10

WORKDIR /app


COPY /src /app/src
COPY requirements.txt /app/.
COPY app.py /app/.
COPY chainlit.md /app/.

EXPOSE 7860

RUN pip install -r requirements.txt

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

CMD ["chainlit", "run", "app.py"]

