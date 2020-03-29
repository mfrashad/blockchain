import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/pow', methods=['POST'])
def proof_of_work():
    """
    Simple Proof of Work Algorithm:
     - Find a number p' such that hash(pp') contains leading 4 zeroes
     - Where p is the previous proof, and p' is the new proof
     
    :param last_proof: integer, last_hash: string
    :return: <int>
    """

    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['last_proof', 'last_hash']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    proof = 0
    while valid_proof(values['last_proof'], proof, values['last_hash']) is False:
        proof += 1
    
    response = {'proof': proof}
    return jsonify(response), 201

def valid_proof(last_proof, proof, last_hash):
    """
    Validates the Proof
    :param last_proof: <int> Previous Proof
    :param proof: <int> Current Proof
    :param last_hash: <str> The hash of the Previous Block
    :return: <bool> True if correct, False if not.
    """

    guess = f'{last_proof}{proof}{last_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)