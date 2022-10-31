FROM python:3.9

# Metadata
LABEL name="altertabot"
LABEL maintainer="avivace4@gmail.com"
LABEL version="0.1".0

ARG YOUR_ENV="virtualenv"

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.6 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# System deps:
RUN DEBIAN_FRONTEND=noninteractive apt update && apt install -y libpq-dev gcc

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app

#Copy all the project files
COPY . .
# Install libraries 
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" = production) --no-dev --no-interaction --no-ansi

# Set the launching script exec
# RUN chmod +x launch.sh

# Launch the script for cron
# CMD ["bash", "launch.sh"]

# Launch main python script
CMD ["uvicorn", "src.main:app", "--reload", "--env-file", "secrets.txt", "--port", "8000", "--host", "0.0.0.0"]
