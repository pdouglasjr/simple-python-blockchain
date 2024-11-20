# for timestamps
import datetime

# for fingerprinting blocks
import hashlib

# for storing data in blockchain
import json

class Block:
    """
    Description: Object representing a single block in a blockchain
     
    Attributes:
        index:          location of block in the blockchain
        id:             unique identifier of the block
        timestamp:      time the block was generated
        proof:          value representing proof-of-work 
        previous_hash:  hash of the previous block in the blockchain

    """

    def __init__(self, index, proof, previous_hash):
        self.index = index
        self.id = index
        self.timestamp = str(datetime.datetime.now())
        self.proof = proof
        self.previous_hash = previous_hash

    def get_data(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.create_block(proof=1, previous_hash='0')
 
    def create_block(self, proof, previous_hash):
        block = Block(
            index=len(self.blocks) + 1,
            proof=proof,
            previous_hash=previous_hash            
        )

        self.blocks.append(block)
        return block

    def get_previous_block(self):
        return self.blocks[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            data = (new_proof ** 2) - (previous_proof ** 2)
            encoded_data = str(data).encode()
            hash_operation = hashlib.sha256(encoded_data).hexdigest()

            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block.get_data(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def chain_valid(self, chain):
        previous_block = chain.blocks[0]
        block_index = 1

        while block_index < len(chain.blocks):
            block = chain.blocks[block_index]

            print(block)

            if block['previous_hash'] != self.hash(previous_block.get_data()):
                return False

            previous_proof = previous_block['proof']
            
            proof = block.proof

            encoded_data = str(proof ** 2 - previous_proof ** 2).encode()

            hash_operation = hashlib.sha256(encoded_data).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            
            previous_block = block
            block_index += 1

        return True
            
if __name__ == "__main__":
    pass