FROM python:3.12

ENV POETRY_VERSION=2.0.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

WORKDIR /langchain_hello_world

#Copy pyproject.toml and README.md to build directory
COPY pyproject.toml .
COPY README.md . 

COPY start.sh start.sh

# Copy agent to build directoyy
COPY langchain_hello_world/ langchain_hello_world/

RUN curl -sSL 'https://install.python-poetry.org' | python3 - \
&& poetry --version && poetry install

#Force installation here because
#even though this is specified on pyproject.toml it wasn't being added to the image
RUN pip install safe-eth-py web3 hexbytes


RUN chmod +x start.sh

ENTRYPOINT ["/langchain_hello_world/start.sh"]

HEALTHCHECK --interval=3s --timeout=600s --retries=600 CMD echo "Add your healthcheck command here" > /dev/null; if [ 0 != $? ]; then exit 1; fi;