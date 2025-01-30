# Basic Langchain agent

To execute this agent:

```bash
poetry shell

poetry install

python langchain_hello_world/__init__.py
```


To test docker image:

```bash
#Build the image, to be executed where Dockerfile is
docker build -t langchain-hello-world .

#Run the container
docker run --rm -it langchain-hello-world

```

To push changes to docker hub:

```bash
docker login

docker tag langchain-hello-world nrosavalory/langchain-hello-world:30012025

docker push nrosavalory/langchain-hello-world:30012025

```