import os
import json
from safe_eth.eth import EthereumClient
from safe_eth.safe import Safe
from hexbytes import HexBytes
from web3 import Web3

class TransactionExecutor:
    """
    Generates single transaction using Safe SDK library
    """
   
    def __init__(self):
        """
        Retrive values and setup Safe SDK clients
        """
        self.__rpc_url = None
        self.__service_safe_address = None
        self.__agent_pk = None

        try:
            print(f"[INFO] Retrieving RPC URL")
            self.__rpc_url = os.environ.get("CONNECTION_LEDGER_CONFIG_LEDGER_APIS_GNOSIS_ADDRESS")
            print(f"[INFO] {self.__rpc_url}")
        except Exception as e:
            print(f"[ERROR] {e}")

        try:
            print(f"[INFO] Retrieving service safe address")
            safe_addresses = json.loads(os.environ.get("CONNECTION_CONFIGS_CONFIG_SAFE_CONTRACT_ADDRESSES"))
            self.__service_safe_address = safe_addresses.get("gnosis")
            print(f"[INFO] { self.__service_safe_address}")
        except Exception as e:
            print(f"[ERROR] {e}")

        
        # Define paths for both Docker volume and local folder
        docker_path = "/agent_key/ethereum_private_key.txt"  # Path inside Docker container
        local_path = "./agent_key/ethereum_private_key.txt"  # Path for local development

        # Determine which path to use
        file_path = docker_path if os.path.exists(docker_path) else local_path

        try:
            print(f"[INFO] Retrieving agent EOA private key")
            with open(file_path, "r") as file:
                self.__agent_pk = file.read() 
            print(f"[INFO] { self.__agent_pk}")               
        except FileNotFoundError:
            print(f"[ERROR] File {file_path} not found.")
        except Exception as e:
            print(f"[ERROR] {e}")

        #Configuring Safe SDK clients
        ethereum_client = EthereumClient(self.__rpc_url)

        # Instantiate the factory contract
        self.__w3 = Web3(Web3.HTTPProvider(self.__rpc_url))

        # Instantiate a Safe
        self.__safe = Safe(self.__service_safe_address, ethereum_client)

        print("[INFO] TransactionExecutor initialized.")          

    def execute(self, to_address:str)->bool:
        """
        Return strue if the transaction is executed with success.
        returns false otherwise.
        """

        if self.__rpc_url is None or self.__service_safe_address is None or self.__agent_pk is None:
            return False
        
        try:
            # Create a Safe transaction
            safe_tx = self.__safe.build_multisig_tx(
                to_address,
                0,
                HexBytes("0x3635C9ADC5DEA00000"))

            # Sign the transaction with Owner A          
            safe_tx.sign(self.__agent_pk)

            # Execute transaction
            tx_hash, _ = safe_tx.execute(self.__agent_pk)

             # Wait
            tx_receipt = self.__w3.eth.wait_for_transaction_receipt(tx_hash)
            if tx_receipt.status == 1:
                print("[INFO] The transaction has been successfully validated")
                return True
            else:
                print(f"ERROR] The transaction has failed with status {tx_receipt.status }")
                return False
        
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
