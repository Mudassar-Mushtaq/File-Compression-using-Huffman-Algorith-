import heapq
import os
from collections import defaultdict, Counter

# Node class for Huffman Tree
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return heapq.heappop(priority_queue)

# Generate Huffman Codes
def generate_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

# Encode the text using Huffman codes
def huffman_encode(text, codebook):
    return ''.join(codebook[char] for char in text)

# Compress the file
def compress_file(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    if not text:
        raise ValueError("The input file is empty.")

    huffman_tree = build_huffman_tree(text)
    codebook = generate_codes(huffman_tree)
    encoded_text = huffman_encode(text, codebook)

    # Pad the encoded text to make it divisible by 8
    padding = 8 - len(encoded_text) % 8
    encoded_text += '0' * padding

    # Convert binary string to bytes
    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        byte_array.append(int(byte, 2))

    # Write to output file
    with open(output_file, 'wb') as file:
        file.write(bytes([padding]))  # Write padding info
        file.write(bytes(byte_array))  # Write encoded data

    print(f"File compressed successfully: {output_file}")

# Decompress the file
def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        padding = int.from_bytes(file.read(1), byteorder='big')
        encoded_data = file.read()

    # Convert bytes to binary string
    encoded_text = ''.join(f'{byte:08b}' for byte in encoded_data)
    encoded_text = encoded_text[:-padding]  # Remove padding

    # Rebuild Huffman Tree (for simplicity, we assume the tree is known)
    # In a real implementation, you would need to store the tree or codebook in the compressed file.
    # For now, we'll assume the codebook is the same as during compression.

    # Decode the text
    decoded_text = ""
    current_code = ""
    reverse_codebook = {v: k for k, v in codebook.items()}

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_text += reverse_codebook[current_code]
            current_code = ""

    # Write decoded text to output file
    with open(output_file, 'w') as file:
        file.write(decoded_text)

    print(f"File decompressed successfully: {output_file}")

# Main function
if __name__ == "__main__":
    input_file = "input.txt"
    compressed_file = "compressed.bin"
    decompressed_file = "decompressed.txt"

    try:
        # Compress the file
        compress_file(input_file, compressed_file)

        # Decompress the file
        decompress_file(compressed_file, decompressed_file)
    except Exception as e:
        print(f"Error: {e}")