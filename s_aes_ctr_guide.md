# A Guide to S-AES with CTR Mode

Hello! This guide breaks down the theory of **Simplified AES (S-AES)** and the **CTR (Counter)** mode of operation so you can understand it and implement it on your own. 

As requested, I won't give you the code yet. Let's start with the theory, and once you write your code, you can share it back with me for review!

---

## Part 1: What is S-AES (Simplified AES)?

S-AES is an educational algorithm designed to teach you how the real Advanced Encryption Standard (AES) works, but with smaller numbers and fewer steps.

*   **Block Size:** 16 bits (instead of 128 in AES).
*   **Key Size:** 16 bits.
*   **Number of Rounds:** 2 rounds (instead of 10+ in AES).

Everything in S-AES operates on **nibbles** (4 bits). A 16-bit block is treated as a 2x2 matrix of nibbles.

### The Algorithm Steps (High Level)

To encrypt a 16-bit block with a 16-bit key, S-AES follows this sequence:

1.  **Key Expansion:** Your one 16-bit Key is expanded into three 16-bit Round Keys ($K_0, K_1, K_2$).
    *   $K_0$ is your original key.
    *   $K_1$ and $K_2$ are generated using a specific algorithm involving Substitution and fixed constants (Rcon).
2.  **Initial Round:** 
    *   **AddRoundKey:** XOR the 16-bit plaintext with $K_0$.
3.  **Round 1:**
    *   **SubNibbles:** Replace each nibble using a predefined 4-bit S-Box.
    *   **ShiftRows:** Swap the 2nd and 4th nibbles.
    *   **MixColumns:** Multiply the matrix by a constant matrix using Galois Field GF($2^4$) arithmetic.
    *   **AddRoundKey:** XOR the result with $K_1$.
4.  **Round 2 (Final Round):**
    *   **SubNibbles:** Same as above.
    *   **ShiftRows:** Same as above.
    *   *(Note: MixColumns is skipped in the final round, just like in real AES!)*
    *   **AddRoundKey:** XOR the result with $K_2$.

The output of Round 2 is your final 16-bit ciphertext block.

---

## Part 2: What is CTR (Counter) Mode?

When encrypting a long message (e.g., an image or a text file), you divide it into blocks. S-AES has a block size of 16 bits (2 bytes). 

However, encrypting each block independently (ECB mode) is insecure. **CTR (Counter) mode** solves this by turning our block cipher (S-AES) into a **stream cipher**.

### How CTR works:

Instead of encrypting the plaintext directly, **we encrypt a Counter**. The encrypted counter gives us a "keystream". We then XOR this keystream with our plaintext.

1.  **The Nonce/Counter:** You start with an Initial Vector (IV) or Nonce (A number used only once). Let's say it's 16 bits. This is Counter 0 ($C_0$).
2.  **Generating the Keystream:**
    *   **Block 1:** Encrypt $C_0$ using S-AES and your 16-bit Key. The output is a 16-bit keystream value ($O_0$).
    *   **Block 2:** Increment the counter: $C_1 = C_0 + 1$. Encrypt $C_1$ using S-AES and your Key. The output is ($O_1$).
    *   **Block 3:** Increment the counter: $C_2 = C_1 + 1$. Encrypt $C_2$, output ($O_2$).
    *   *...Repeat for all blocks...*
3.  **Encrypting the Message:**
    *   Ciphertext Block 1 = Plaintext Block 1 $\oplus$ $O_0$
    *   Ciphertext Block 2 = Plaintext Block 2 $\oplus$ $O_1$
    *   Ciphertext Block 3 = Plaintext Block 3 $\oplus$ $O_2$

### Important Characteristics of CTR Mode:

*   **No Padding Required:** Because you are just XORing the message with a keystream, if your last message block is only 8 bits (1 byte) instead of 16 bits, you just XOR it with the first 8 bits of the keystream. No adding dummy bits (padding) needed!
*   **Decryption is Exactly the Same:** To decrypt, you generate the **exact same keystream** by encrypting the counters with the exact same Key and starting IV. Then, you XOR the keystream with the Ciphertext to get the Plaintext back. **You don't need to write an S-AES Decryption function; you only need the Encryption function!**

---

## Part 3: Your Implementation Plan

To tackle your assignment, here is how you should break down your work mathematically and programmatically:

### 1. Build the building blocks for S-AES
You will need helper functions for:
*   Galois Field multiplication (for `MixColumns`).
*   An `S_BOX` lookup array/dictionary.
*   Functions to convert strings/bytes into 16-bit binary arrays.

### 2. Implement S-AES Core
*   Write a function `key_expansion(16bit_key) -> (K_0, K_1, K_2)`
*   Write a function `s_aes_encrypt_block(16bit_block, 16bit_key) -> 16bit_ciphertext`

### 3. Implement CTR Wrapper
*   Write an `encrypt_ctr(data, key, nonce)` function.
*   Loop through the data 16 bits at a time.
*   For each 16 bits, call `s_aes_encrypt_block(counter, key)`.
*   XOR the resulting keystream with the 16 bits of data.
*   Add 1 to the counter.
*   Return the combined ciphertext.

*(Remember: For decryption, you just call `encrypt_ctr(ciphertext, key, nonce)`! It will reverse the XOR and output the original data.)*

---
Good luck! Whenever you start writing the Python code and want me to review algorithms or debug issues, just paste your progress or mention the file path, and we'll fix it together.
