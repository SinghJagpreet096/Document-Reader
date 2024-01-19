FROM python:3.10

WORKDIR /app


COPY /src /app/src
COPY requirements.txt /app/.
COPY app.py /app/.
COPY chainlit.md /app/.



# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Try and run pip command after setting the user with `USER user` to avoid permission issues with Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app

# Download a checkpoint
RUN mkdir content
#ADD --chown=user https://<SOME_ASSET_URL> content/<SOME_ASSET_NAME>

EXPOSE 7860

CMD ["chainlit", "run", "app.py"]

