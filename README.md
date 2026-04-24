# S-AES with CTR Mode and Cryptanalysis

This repository represents the final, complete implementation of the Simplified Advanced Encryption Standard (S-AES) using the Counter (CTR) mode of operation, alongside an exhaustive cryptanalysis brute-force attack and a comprehensive unit-testing suite. 

The entire mathematical engine and logic were written from scratch in Python, strictly fulfilling the requirement to avoid external predefined cryptographic libraries.

## 1. Project Architecture

The project is structured into four main operational domains:

1. **`saes_core.py` (The Mathematical Core)**: Contains the low-level cryptography engine. It handles all matrix operations, S-Box lookups, bitwise logic, and finite-field $GF(2^4)$ math to securely encrypt a single 16-bit block.
2. **`ctr_mode.py` (The System Wrapper)**: Transforms the block cipher into a Continuous Stream Cipher. It implements padding-safe binary interactions allowing the cipher to encrypt/decrypt arbitrary raw files, including images, videos, texts, and PDFs natively. 
3. **`test_saes.py` (The Verification Suite)**: Contains 31 automated unit tests verifying the mathematical precision of the Galois Field arithmetic, the key expansion, and asserting accuracy against the official Stallings S-AES test vectors (Key: `0xA73B`, Plaintext: `0x6F6B` $\rightarrow$ Ciphertext: `0x0738`).
4. **`brute_force.py` (The Cryptanalysis Attack)**: Explores the vulnerability of the 16-bit key space structure. It implements a Known-Plaintext Attack (KPA) by recovering the CTR keystream via boolean XOR and exhaustively searching all 65,536 key combinations in under one second to derive the master key.

## 2. Cryptographic Implementation Details

Because predefined libraries were strictly forbidden, the algorithm relies strictly on low-level Python manipulations:
* **Bitwise Shifts (`<<`, `>>`)**: Used to isolate 4-bit nibbles securely and execute structural mathematical scaling (multiplying by $x$ in polynomials).
* **Bitwise AND (`&`)**: Used as a masking filter to perfectly prevent binary tracking overflows.
* **Bitwise XOR (`^`)**: Employed heavily for the AddRoundKey step, symmetric CTR mode overlay, and for $GF(2^4)$ polynomial long-division reduction.

The `MixColumns` step utilizes a matrix multiplication optimized via a custom $GF(2^4)$ "Shift-and-XOR" reduction function, seamlessly looping operations within the field over the irreducible polynomial `0x13`.

## 3. How to Use The System

### Encrypting and Decrypting Files (`ctr_mode.py`)
Because Counter Mode (CTR) transforms a block cipher into a stream cipher via symmetrical XOR operations, the script for encryption is completely mathematically identical to the script for decryption. 

Run the CTR wrapper file from your terminal:
```bash
python ctr_mode.py
```
It will prompt you for four interactive variables:
1. **Input File**: Path to the file you wish to process (e.g., `image.png`).
2. **Output File**: Path to save the processed binary output (e.g., `encrypted_image.png`).
3. **Key**: A 16-bit integer (e.g., `12345`) serving as your highly-secret encryption key.
4. **Starting Counter**: Your starting Initialization Vector (usually `0`).

### Running the Brute-Force KPA Attack (`brute_force.py`)
Run the script to witness how quickly a 16-bit key falls to modern computational hardware:
```bash
python brute_force.py
```
You will provide a chunk of known plaintext, the matching ciphertext chunk, and the counter integer used. The program will instantaneously recover the keystream, scan all $2^{16}$ possible keys, and reveal the secret key.

### Verifying Math Integrity (`test_saes.py`)
Run the automated test suite to mathematically verify every single step of the AES rounds:
```bash
python test_saes.py
```
