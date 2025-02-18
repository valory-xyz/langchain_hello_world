# Langchain Hello World Agent for Olas

## Overview

This repository contains a basic Langchain agent that interacts with the Tavily and OpenAI APIs while also enabling on-chain transactions via the Safe ETH SDK. The agent is designed to run in a containerized environment through Olas' quickstart.

### Langchain Framework

[Langchain](https://www.langchain.com/) is a powerful framework for developing applications with Large Language Models (LLMs). It simplifies the integration of different AI tools, memory, and external APIs, making it easier to build intelligent agents that interact with diverse data sources.

### Olas Ecosystem

[Olas](https://olas.network/) is a decentralized compute marketplace that enables developers to deploy and monetize AI services in a trustless environment. By leveraging Olas' infrastructure, this agent can operate within a permissionless, decentralized environment while handling API interactions and on-chain transactions.

## Features

- **LLM-powered agent** using OpenAI API for natural language processing.
- **Web search capability** powered by Tavily API for retrieving real-time information.
- **Blockchain transactions** enabled via [Safe ETH SDK](https://docs.safe.global/core-api/transaction-service-overview) to perform secure on-chain operations.
- **Wallet abstraction and containerized execution** using [Olas Quickstart](https://github.com/valory-xyz/quickstart).

## Setup and Local Testing

### Prerequisites

Before setting up the environment, ensure you have the following installed:

- **[Python 3.10+](https://www.python.org/)**
- **[Poetry 1.8.4](https://github.com/python-poetry/poetry)**

### Running the Agent locally without on-chain transactions

1. Create a virtual environment and install the dependencies:

    ```sh
    poetry shell

    poetry install
    
    ```

3. Setup the .env file by duplicating the `.env.example` file and renaming it to `.env`.

    ```bash
    cp .env.example .env
    ```

    Then fill in the required environment variables.

    - `CONNECTION_CONFIGS_CONFIG_TAVILY_API_KEY` - Get a [Tavily](https://python.langchain.com/docs/integrations/tools/tavily_search/) API Key
    - `CONNECTION_CONFIGS_CONFIG_OPENAI_API_KEY` - Get an [OpenAI](https://platform.openai.com/settings/organization/api-keys) API Key.

4. Start agent execution:

   ```sh
   python src/main.py
   ```


### Testing on-chain transactions

When executing this agent through Olas Quickstart the safe wallet and agent private key will be automatically setup, however you can follow these steps if you want to test transactions execution locally:

1. Prepare some wallet private key that will act as the signer of your local transactions. Save this private key on a file called `ethereum_private_key.txt` on a folder called `agent_key`

    ```sh
    echo "<Your private key here>" > /agent_key/ethereum_private_key.txt
    ```

2. Deploy a [Safes on Gnosis](https://app.safe.global/welcome) (it's free) and set your wallet address the signer. Set the signature threshold to 1 out of 4.

3. Create a [Tenderly](https://tenderly.co/) account and from your dashboard create a fork of Gnosis chain (virtual testnet).

4. From Tenderly, fund your wallet and Safe with some xDAI.

5. Then add the following environment variables:
   
    - `CONNECTION_LEDGER_CONFIG_LEDGER_APIS_GNOSIS_ADDRESS` - Set it to your Tenderly fork Admin RPC
    - `CONNECTION_CONFIGS_CONFIG_SAFE_CONTRACT_ADDRESSES` - The safe contract address created on step 2.
 
6. Start agent execution and you should see some transactions being executed on Tenderly explorer:

   ```sh
   python src/main.py
   ```

## Docker

To deploy this agent to Olas you will need to have a docker image configured, ensure you have Docker installed and follow the steps below to test and publish your image. The tag of your image will need to match your agent hash. #TODO: Add link to SDK Starter guide

### Testing image 
```bash
#Build the image, to be executed where Dockerfile is
docker build -t langchain-hello-world .

#Run the container
docker run --rm -it langchain-hello-world

```

### Pushing image to docker hub

```bash
#Login to docker
docker login

#Tag the image built previously with correct tag
docker tag langchain-hello-world <docker_repo_name>/langchain-hello-world:<tag_name>

#Push it to a public docker hub repository
docker push <docker_repo_name>/langchain-hello-world:<tag_name>

```

## Contributing

Feel free to submit issues or pull requests if you want to improve this repository. Contributions are welcome!

## License

This project is licensed under the MIT License.

