import sys
from solana.rpc.api import Client
from solana.publickey import PublicKey
import pandas as pd

# RPC endpoint (mainnet-beta)
RPC_URL = "https://api.mainnet-beta.solana.com"

def fetch_transactions(signature):
    client = Client(RPC_URL)
    tx = client.get_transaction(signature, encoding="jsonParsed", max_supported_transaction_version=0)
    if tx.value:
        return tx.value.transaction
    return None

def analyze_tx(tx):
    if not tx:
        return "No data"
    meta = tx.meta
    message = tx.transaction.message
    df = pd.DataFrame({
        'fee': [meta.fee],
        'pre_balances': [meta.pre_balances],
        'post_balances': [meta.post_balances],
        'instructions': [len(message.instructions)]
    })
    print(df)
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <tx_signature>")
    else:
        sig = sys.argv[1]
        tx = fetch_transactions(sig)
        analyze_tx(tx)
