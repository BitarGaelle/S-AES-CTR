# S-AES with CTR Mode (Assignment Project)

This repository contains a full implementation of the Simplified Advanced Encryption Standard (S-AES) using the Counter (CTR) mode of operation, written entirely from scratch in standard Python without external predefined cryptographic libraries.

## 1. Project Structure
The project is mathematically divided into two domains:
1.  **`saes_core.py`**: Contains the core cryptography engine. It handles all matrix operations, S-Box lookups, Bitwise logic, and Galois Field $GF(2^4)$ math to securely encrypt a single 16-bit block.
2.  **`ctr_mode.py`** *(To be completed)*: Contains the CTR wrapper that allows the cipher to encrypt/decrypt entire files, images, and texts using a dynamic counter stream.

## 2. Methodology & Operations Used
Because predefined AES libraries were strictly forbidden, the algorithm relies strictly on low-level Python manipulations:
*   **Bitwise Shifts (`<<`, `>>`)**: Used to perfectly isolate 4-bit nibbles and execute polynomial multiplication.
*   **Bitwise AND (`&`)**: Used as a mask to prevent binary overlaps.
*   **Bitwise XOR (`^`)**: Used for the AddRoundKey step and for $GF(2^4)$ polynomial reduction.

## 3. The Mathematics of `saes_core.py`
The block cipher expands a 16-bit key into three round keys ($K_0, K_1, K_2$). It encrypts the 16-bit plaintext block using two Rounds. The complex `MixColumns` step utilizes a matrix multiplication optimized via a custom $GF(2^4)$ Shift-and-XOR mathematical reduction function (`gf_multiply_2`).

To execute this, the required sequence is:
`AddRoundKey` $\rightarrow$ `SubNibbles` $\rightarrow$ `ShiftRows` $\rightarrow$ `MixColumns` $\rightarrow$ `AddRoundKey` $\rightarrow$ `SubNibbles` $\rightarrow$ `ShiftRows` $\rightarrow$ `AddRoundKey`. 
