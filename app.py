from flask import Flask, jsonify

from blockchain.blockchain import Blockchain

# create teh Flask app
app = Flask(__name__)

# initialize blockchain
blockchain = Blockchain()

# mine a new block for the chain
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_block_data = previous_block.get_data()

    previous_proof = previous_block.proof
    
    proof = blockchain.proof_of_work(previous_proof)

    previous_hash = blockchain.hash(previous_block)

    block = blockchain.create_block(proof=proof, previous_hash=previous_hash)

    response = {
        'message': 'A blcok is MINED',
        'index': block.index,
        'timestamp': block.timestamp,
        'proof': block.proof,
        'previous_hash': block.previous_hash,    
    }

    return jsonify(response), 200

# display blockchain in json format
@app.route('/get_chain', methods=["GET"])
def get_chain():
    chain = blockchain.blocks

    blocks = []

    for block in chain:
        blocks.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'proof': block.proof,
            'previous_hash': block.previous_hash,            
        })

    response = {
        'chain': blocks,
        'length': len(blocks),
    }
    return jsonify(response), 200

# check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain)

    if valid:
        response = { 'message': "Blockchain passed validation." }
    else:
        response = { 'message': "Blockhain failed validation." }

    return jsonify(response), 200