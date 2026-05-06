SBOX = [
    0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5, 
    0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7
] #S-box (1-D list with hex notations)


def key_expansion(key):
    #key 0
    w0 = (key >> 8) & 0xFF
    w1 = key & 0xFF
    
    #constants
    rcon1 = 0x80
    rcon2 = 0x30
    
    #Sub(Rot(w)) ^ Rcon
    def g_func(w, rcon):
        n0 = (w >> 4) & 0xF
        n1 = w & 0xF
        
        sub = (SBOX[n1] << 4) | SBOX[n0]
        
        return sub ^ rcon

    #key1
    w2 = w0 ^ g_func(w1, rcon1)
    w3 = w1 ^ w2
    
    #key2
    w4 = w2 ^ g_func(w3, rcon2)
    w5 = w3 ^ w4
    
    key1 = (w2 << 8) | w3
    key2 = (w4 << 8) | w5
    
    return key, key1, key2

def add_round_key(plaintext, key):
    return plaintext ^ key
    
def sub_nibbles(state):
    n0 = (state >> 12) & 0xF
    n1 = (state >> 8) & 0xF
    n2 = (state >> 4) & 0xF
    n3 = state & 0xF
    return (SBOX[n0] << 12) | (SBOX[n1] << 8) | (SBOX[n2] << 4) | SBOX[n3]

def shift_rows(state):
    n0 = (state >> 12) & 0xF
    n1 = (state >> 8) & 0xF
    n2 = (state >> 4) & 0xF
    n3 = state & 0xF
    return (n0 << 12) | (n3 << 8) | (n2 << 4) | n1

# multiplying by 4 is multiplying by 2 twice => shift left by 1 twice
def gf_multiply_2(a):
    new_a = a << 1

    if new_a > 15:
        new_a = new_a ^ 0x13 # 19 in decimal or x^4 + x + 1

    return new_a & 15 # making sure to return 4 bits

def gf_multiply(a):
    return gf_multiply_2(gf_multiply_2(a))
    
def mix_columns(nibbles):
    n0 = (nibbles >> 12) & 0xF
    n1 = (nibbles >> 8) & 0xF
    n2 = (nibbles >> 4) & 0xF
    n3 = nibbles & 0xF
    
    s0 = n0 ^ gf_multiply(n1)
    s1 = gf_multiply(n0) ^ n1

    s2 = n2 ^ gf_multiply(n3)
    s3 = gf_multiply(n2) ^ n3
    
    return (s0 << 12) | (s1 << 8) | (s2 << 4) | s3

def saes_encrypt(block, key):
    key0, key1, key2 = key_expansion(key)
    
    # Initial Round
    state = add_round_key(block, key0)
    
    # Round 1
    state = sub_nibbles(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, key1)
    
    # Round 2
    state = sub_nibbles(state)
    state = shift_rows(state)
    state = add_round_key(state, key2)
    
    return state

# plaintext = 0x6F6B
# key = 0xA73B

# print(f'keys: {key_expansion(key)} ')

# print(f'Cypher text: {saes_encrypt(plaintext, key)}')

