from web3 import Web3
from flask import Flask
import os
from config import mycollection
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

ganache_url = 'HTTP://127.0.0.1:7545'
web3_connection = Web3(Web3.HTTPProvider(ganache_url))
print('Connection established' + ' = ', web3_connection.isConnected())
print('blockNumber' + ' = ', web3_connection.eth.blockNumber)


def transaction():
    account1 = web3_connection.toChecksumAddress('0x52b60b6cfCd1fdb26F009EaFb1649455b2690A3C')
    account2 = web3_connection.toChecksumAddress('0xC367C9c52452023FCC13d6B3eCae1801d238d041')
    # private key of account 1 from ganache
    private_key = os.getenv('PRIVATE_KEY')
    # get the nance
    # build a transaction
    nonce = web3_connection.eth.getTransactionCount(account1)
    amount_transfer = web3_connection.toWei(0.005, 'ether')
    tx = {
        'nonce': nonce,
        'to': account2,
        'value': amount_transfer,
        'gas': 100000,
        'gasPrice': web3_connection.toWei('5', 'gwei')
    }
    # sign transaction
    signed_tx = web3_connection.eth.account.signTransaction(tx, private_key)
    txhash = web3_connection.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(txhash)
    print(web3_connection.toHex(txhash))
    dicts = {}
    dicts['hash'] = web3_connection.toHex(txhash)
    dicts['amount_to_transfer'] = amount_transfer
    # add into db
    mycollection.insert_one(dicts)
    return 'success'


@app.route('/webtransaction')
def main():
    return transaction()


if __name__ == '__main__':
    app.run(debug=True)
