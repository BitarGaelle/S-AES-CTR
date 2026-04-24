import time
from saes_core import saes_encrypt

def recover_keystream(plaintext_block, ciphertext_block):
    #keystream = pt XOR ct
    return plaintext_block ^ ciphertext_block

def brute_force(plaintext_block, ciphertext_block, counter=0):
    keystream = recover_keystream(plaintext_block, ciphertext_block)
    for candidate_key in range(65536):
        if saes_encrypt(counter, candidate_key) == keystream:
            return candidate_key
    return None

if __name__ == "__main__":
    plaintext_block  = int(input("Enter known plaintext block (integer): "))
    ciphertext_block = int(input("Enter known ciphertext block (integer): "))
    counter          = int(input("Enter counter value used for that block: "))

    print("Brute forcing...")
    start = time.time()
    found_key = brute_force(plaintext_block, ciphertext_block, counter)
    elapsed = time.time() - start

    if found_key is not None:
        print(f"Key found: {found_key} (0x{found_key:04X})")
    else:
        print("No key found.")
    print(f"Time: {elapsed:.4f}s")
