import time
from saes_core import saes_encrypt
from ctr_mode import ctr_process_block, increment_counter, process_file_ctr
from brute_force import brute_force


def parse_int(s):
    return int(s.strip(), 0)


def text_to_blocks(text):
    raw = text.encode("utf-8")
    padded = len(raw) % 2 == 1
    if padded:
        raw += b"\x00"
    blocks = [int.from_bytes(raw[i:i+2], "big") for i in range(0, len(raw), 2)]
    return blocks, padded


def blocks_to_text(blocks, padded):
    raw = b"".join(b.to_bytes(2, "big") for b in blocks)
    if padded:
        raw = raw[:-1]
    return raw.decode("utf-8", errors="replace")


def ctr_blocks(blocks, key, counter):
    result = []
    cur = counter
    for block in blocks:
        result.append(ctr_process_block(block, cur, key))
        cur = increment_counter(cur)
    return result


def menu_encrypt():
    text = input("Plaintext: ")
    key = parse_int(input("Key (decimal or 0x hex): "))
    counter_str = input("Starting counter [0]: ").strip()
    counter = parse_int(counter_str) if counter_str else 0

    blocks, padded = text_to_blocks(text)
    cipher = ctr_blocks(blocks, key, counter)

    print(f"\nCiphertext: {' '.join(f'{b:04X}' for b in cipher)}")
    if padded:
        print("[last block was padded]")


def menu_decrypt():
    raw = input("Ciphertext (space-separated hex, e.g. 1A2B 3C4D): ")
    cipher = [int(x, 16) for x in raw.split()]
    key = parse_int(input("Key (decimal or 0x hex): "))
    counter_str = input("Starting counter [0]: ").strip()
    counter = parse_int(counter_str) if counter_str else 0
    padded = input("Was last block padded? (y/n) [n]: ").strip().lower() == "y"

    plain = ctr_blocks(cipher, key, counter)
    print(f"\nDecrypted: {blocks_to_text(plain, padded)!r}")


def menu_file():
    src = input("Input file path: ").strip()
    dst = input("Output file path: ").strip()
    key = parse_int(input("Key (decimal or 0x hex): "))
    counter_str = input("Starting counter [0]: ").strip()
    counter = parse_int(counter_str) if counter_str else 0

    process_file_ctr(src, dst, key, counter)
    print(f"Done → {dst}")


def menu_brute_force():
    print("\nTries all 65 536 possible keys.")
    pt = parse_int(input("Known plaintext block (decimal or 0x hex): "))
    ct = parse_int(input("Corresponding ciphertext block (decimal or 0x hex): "))
    counter_str = input("Counter value used for that block [0]: ").strip()
    counter = parse_int(counter_str) if counter_str else 0

    print("Searching...")
    start = time.time()
    found = brute_force(pt, ct, counter)
    elapsed = time.time() - start

    if found is not None:
        print(f"Key found: {found} (0x{found:04X})")
    else:
        print("No key found.")
    print(f"Time: {elapsed:.4f}s")


def menu_demo():
    text = "Hello!"
    key = 0xA73B
    counter = 0

    print(f"\nPlaintext : {text!r}")
    print(f"Key       : 0x{key:04X}")
    print(f"Counter   : {counter}")

    blocks, padded = text_to_blocks(text)
    cipher = ctr_blocks(blocks, key, counter)
    print(f"Ciphertext: {' '.join(f'{b:04X}' for b in cipher)}")

    plain = ctr_blocks(cipher, key, counter)
    print(f"Decrypted : {blocks_to_text(plain, padded)!r}")

    pt_block = blocks[0]
    ct_block = cipher[0]
    print(f"\nBrute forcing from block 0 (PT=0x{pt_block:04X}, CT=0x{ct_block:04X}, ctr=0)...")
    start = time.time()
    found = brute_force(pt_block, ct_block, 0)
    elapsed = time.time() - start
    print(f"Found key : 0x{found:04X} in {elapsed:.4f}s")


def main():
    print("=" * 44)
    print("   S-AES + CTR MODE  —  Interactive Demo")
    print("=" * 44)

    while True:
        print("\n1. Encrypt text")
        print("2. Decrypt text")
        print("3. Encrypt / Decrypt file")
        print("4. Brute force key recovery")
        print("5. Run built-in demo")
        print("0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            menu_encrypt()
        elif choice == "2":
            menu_decrypt()
        elif choice == "3":
            menu_file()
        elif choice == "4":
            menu_brute_force()
        elif choice == "5":
            menu_demo()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
