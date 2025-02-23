# yet to be implemented ig 
# dinesh use the meowfi mint token for reference okay must not be hard

from aptos_sdk.aptos_token_client import RestClient
from config import REWARDS_COLLECTION_ID
from database import create_document

APTOS_NODE_URL = "https://fullnode.testnet.aptoslabs.com"
aptos_client = RestClient(APTOS_NODE_URL)

def mint_tokens(reps: int, user: dict):
    if reps >= 10:
        tx = "mock_tx_hash"  # Mock for hackathon
        try:
            tx = aptos_client.submit_transaction(user["wallet_address"], "FormFitRewards::mint_reward", [100])
        except Exception as e:
            print(f"Aptos error: {e}")
        reward = create_document(
            REWARDS_COLLECTION_ID,
            {
                "user_id": user["$id"],
                "reps_achieved": reps,
                "tokens": 100,
                "tx_hash": tx
            }
        )
        return {"status": "success", "tokens": 100, "tx": tx}
    return {"status": "no_reward"}