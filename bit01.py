import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data, nonce):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data) + str(nonce)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def proof_of_work(block, difficulty):
    nonce = 0
    while True:
        hash = calculate_hash(block.index, block.previous_hash, block.timestamp, block.data, nonce)
        if hash[:difficulty] == '0'*difficulty:
            return nonce, hash
        nonce += 1

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block", 0))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    nonce, hash = proof_of_work(previous_block, 4)  # 4 is the difficulty level
    return Block(index, previous_block.hash, timestamp, data, hash)

# Create blockchain and add genesis block
blockchain = [create_genesis_block()]
previous_block = blockchain[0]

# Add blocks to the blockchain
num_blocks_to_add = 10
for i in range(0, num_blocks_to_add):
    block_to_add = create_new_block(previous_block, f"Block #{i} has been added to the blockchain!")
    blockchain.append(block_to_add)
    previous_block = block_to_add
    print(f"Block #{block_to_add.index} has been added to the blockchain!")
    print(f"Hash: {block_to_add.hash}\n")