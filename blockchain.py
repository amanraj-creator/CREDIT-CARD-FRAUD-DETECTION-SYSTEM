
import hashlib
import json
import time
from datetime import datetime  # Added for readable timestamp

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(data='Genesis Block')

    def create_block(self, data):
        timestamp = time.time()
        readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # New line

        block = {
            'index': len(self.chain) + 1,
            'timestamp': timestamp,                         # Original timestamp
            'readable_timestamp': readable_time,            # Human-readable timestamp
            'data': data,
            'previous_hash': self.chain[-1]['hash'] if self.chain else '0'
        }
        block['hash'] = self.hash_block(block)
        self.chain.append(block)
        return block

    def add_block(self, data):
        return self.create_block(data)

    def hash_block(self, block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
