# S-AES with CTR Mode (Assignment Project)

This repository contains a full implementation of the Simplified Advanced Encryption Standard (S-AES) using the Counter (CTR) mode of operation, written entirely from scratch in standard Python without external predefined cryptographic libraries.

## 1. Project Structure
The project is mathematically divided into two domains:
1.  **`saes_core.py`**: Contains the core cryptography engine. It handles all matrix operations, S-Box lookups, Bitwise logic, and Galois Field $GF(2^4)$ math to securely encrypt a single 16-bit block.
2.  **`ctr_mode.py`**: Contains the completed CTR wrapper that allows the cipher to encrypt/decrypt entire binary files, images, and text streams using a dynamic counter stream. Padding-safe file reading and writing are fully implemented.

## 2. Methodology & Operations Used
Because predefined AES libraries were strictly forbidden, the algorithm relies strictly on low-level Python manipulations:
*   **Bitwise Shifts (`<<`, `>>`)**: Used to perfectly isolate 4-bit nibbles and execute polynomial multiplication.
*   **Bitwise AND (`&`)**: Used as a mask to prevent binary overlaps.
*   **Bitwise XOR (`^`)**: Used for the AddRoundKey step and for $GF(2^4)$ polynomial reduction.

## 3. The Mathematics of `saes_core.py`
The block cipher expands a 16-bit key into three round keys ($K_0, K_1, K_2$). It encrypts the 16-bit plaintext block using two Rounds. The complex `MixColumns` step utilizes a matrix multiplication optimized via a custom $GF(2^4)$ Shift-and-XOR mathematical reduction function (`gf_multiply_2`).

To execute this, the required sequence is:
`AddRoundKey` $\rightarrow$ `SubNibbles` $\rightarrow$ `ShiftRows` $\rightarrow$ `MixColumns` $\rightarrow$ `AddRoundKey` $\rightarrow$ `SubNibbles` $\rightarrow$ `ShiftRows` $\rightarrow$ `AddRoundKey`. 

## 4. How to Use & Test the Project
Because Counter Mode (CTR) transforms a block cipher into a stream cipher via symmetrical XOR operations, the script for encryption is completely mathematically identical to the script for decryption. 

### Executing the script
Run the CTR wrapper file from your terminal:
```bash
python ctr_mode.py
```
It will prompt you for four interactive variables:
1. **Input File**: Path to the file you wish to process (e.g., `message.txt`, `image.png`).
2. **Output File**: Path to save the processed binary output (e.g., `encrypted.txt`, `decrypted_image.png`).
3. **Key**: A 16-bit integer (e.g., `55000`) serving as your highly-secret encryption key. **You must use this exact same integer to decrypt the file later.**
4. **Starting Counter**: Your starting Initialization Vector (usually `0`).

### Example Test Workflow
1. Create a file `secret.txt` containing a hidden message.
2. Run `python ctr_mode.py`. Use inputs: `secret.txt`, `cipher.bin`, `12345`, `0`.
3. Open `cipher.bin` to verify the bytes are perfectly scrambled and unreadable.
4. Run `python ctr_mode.py` again. Use inputs: `cipher.bin`, `restored.txt`, `12345`, `0`.
5. Open `restored.txt`. It will perfectly match your original `secret.txt` message!
