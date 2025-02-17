import os
import json
from safe_eth.eth import EthereumClient, EthereumNetwork
from safe_eth.safe.api.transaction_service_api import TransactionServiceApi
from safe_eth.safe import Safe
from hexbytes import HexBytes

class TransactionExecuter:


    def __init__(self):
        self.__rpc_url = None
        self.__service_safe_address = None
        self.__agent_pk = None

        try:
            print(f"[INFO] Retrieving RPC URL")
            self.__rpc_url = os.environ.get("CONNECTION_LEDGER_CONFIG_LEDGER_APIS_GNOSIS_ADDRESS")
        except Exception as e:
            print(f"[ERROR] {e}")

        try:
            print(f"[INFO] Retrieving service safe address")
            safe_addresses = json.loads(os.environ.get("CONNECTION_CONFIGS_CONFIG_SAFE_CONTRACT_ADDRESSES"))
            self.__service_safe_address = safe_addresses.get("gnosis")
        except Exception as e:
            print(f"[ERROR] {e}")


        path_to_agent_pk = "/agent_key/ethereum_private_key.txt"

        try:
            print(f"[INFO] Retrieving agent EOA private key")
            with open(path_to_agent_pk, "r") as file:
                self.__agent_pk = file.read()                
        except FileNotFoundError:
            print(f"[ERROR] File {path_to_agent_pk} not found.")
        except Exception as e:
            print(f"[ERROR] {e}")  

        print("[INFO] TransactionExecutor initialized.")          

    def can_transact(self):
        """Returns true if all the configuration were found during initialization"""
        if self.__rpc_url is not None and self.__service_safe_address is not None and self.__agent_pk is not None:
            return True
        
        return False

    def execute(self, to_address:str)->bool:
        """Public method to access the private balance."""

        try:
            ethereum_client = EthereumClient(self.__rpc_url)

            # Instantiate a Safe
            safe = Safe(self.__service_safe_address, ethereum_client)

            # Create a Safe transaction
            safe_tx = safe.build_multisig_tx(
                to_address,
                0,
                HexBytes("0x3635C9ADC5DEA00000"))

            # Sign the transaction with Owner A
            #OWNER_A_PRIVATE_KEY
            safe_tx.sign(self.__agent_pk)

            # Instantiate the Transaction Service API
            transaction_service_api = TransactionServiceApi(
                network=EthereumNetwork.GNOSIS,
                ethereum_client=ethereum_client)

            # Send the transaction to the Transaction Service with the signature from Owner A
            transaction_service_api.post_transaction(safe_tx)

            (safe_tx_from_tx_service, _) = transaction_service_api.get_safe_transaction(safe_tx.safe_tx_hash)

            result = safe_tx_from_tx_service.execute(self.__agent_pk)

            transactions = transaction_service_api.get_transactions(self.__service_safe_address)

            last_executed_tx = next(
                (x for x in transactions if x.get('isExecuted')),
                None)
            
            return True
        
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
