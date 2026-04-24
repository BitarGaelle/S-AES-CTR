import unittest
from saes_core import (
    key_expansion, add_round_key, sub_nibbles,
    shift_rows, gf_multiply_2, gf_multiply, mix_columns, saes_encrypt
)
from ctr_mode import increment_counter, ctr_process_block


class TestGFMultiply(unittest.TestCase):
    """GF(2^4) arithmetic with irreducible polynomial x^4+x+1 (0x13)."""

    def test_multiply2_zero(self):
        self.assertEqual(gf_multiply_2(0), 0)

    def test_multiply2_one(self):
        self.assertEqual(gf_multiply_2(1), 2)

    def test_multiply2_no_overflow(self):
        # 6 << 1 = 12, no reduction needed
        self.assertEqual(gf_multiply_2(6), 12)

    def test_multiply2_with_reduction(self):
        # 8 << 1 = 16 > 15 → 16 ^ 0x13 = 3
        self.assertEqual(gf_multiply_2(8), 3)

    def test_multiply2_with_reduction_9(self):
        # 9 << 1 = 18 > 15 → 18 ^ 0x13 = 1
        self.assertEqual(gf_multiply_2(9), 1)

    def test_multiply4_is_double_double(self):
        # gf_multiply(a) = gf_multiply_2(gf_multiply_2(a))
        for a in range(16):
            self.assertEqual(gf_multiply(a), gf_multiply_2(gf_multiply_2(a)))

    def test_multiply4_stays_in_field(self):
        # All results must be 4-bit values
        for a in range(16):
            result = gf_multiply(a)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 15)

    def test_multiply2_stays_in_field(self):
        for a in range(16):
            result = gf_multiply_2(a)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 15)


class TestKeyExpansion(unittest.TestCase):
    """Known test vector from Stallings 'Cryptography and Network Security'."""

    def test_stallings_vector(self):
        # Key = 0xA73B → K0=0xA73B, K1=0x1C27, K2=0x7651
        k0, k1, k2 = key_expansion(0xA73B)
        self.assertEqual(k0, 0xA73B)
        self.assertEqual(k1, 0x1C27)
        self.assertEqual(k2, 0x7651)

    def test_k0_is_original_key(self):
        for key in [0x0000, 0xFFFF, 0x1234, 0xA73B]:
            k0, _, _ = key_expansion(key)
            self.assertEqual(k0, key)

    def test_keys_are_16bit(self):
        k0, k1, k2 = key_expansion(0xA73B)
        for k in (k0, k1, k2):
            self.assertGreaterEqual(k, 0)
            self.assertLessEqual(k, 0xFFFF)


class TestAddRoundKey(unittest.TestCase):
    def test_xor_correctness(self):
        self.assertEqual(add_round_key(0x6F6B, 0xA73B), 0xC850)

    def test_identity_with_zero_key(self):
        self.assertEqual(add_round_key(0x1234, 0x0000), 0x1234)

    def test_self_inverse(self):
        # XOR is its own inverse
        state = 0xABCD
        key = 0x1234
        self.assertEqual(add_round_key(add_round_key(state, key), key), state)


class TestSubNibbles(unittest.TestCase):
    def test_stallings_intermediate(self):
        # After AddRoundKey: 0xC850 → SubNibbles → 0xC619
        self.assertEqual(sub_nibbles(0xC850), 0xC619)

    def test_output_is_16bit(self):
        for val in [0x0000, 0xFFFF, 0x1234, 0xABCD]:
            result = sub_nibbles(val)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 0xFFFF)


class TestShiftRows(unittest.TestCase):
    def test_stallings_intermediate(self):
        # ShiftRows(0xC619) → swaps nibbles n1 and n3 → 0xC916
        self.assertEqual(shift_rows(0xC619), 0xC916)

    def test_double_shift_is_identity(self):
        # Two ShiftRows = identity (swapping twice restores original)
        for val in [0x0000, 0xFFFF, 0x1234, 0xABCD]:
            self.assertEqual(shift_rows(shift_rows(val)), val)


class TestMixColumns(unittest.TestCase):
    def test_stallings_intermediate(self):
        # MixColumns(0xC916) → 0xECA2
        self.assertEqual(mix_columns(0xC916), 0xECA2)

    def test_output_is_16bit(self):
        for val in [0x0000, 0xFFFF, 0x1234, 0xABCD]:
            result = mix_columns(val)
            self.assertGreaterEqual(result, 0)
            self.assertLessEqual(result, 0xFFFF)


class TestSAESEncrypt(unittest.TestCase):
    """Full encrypt test against Stallings known vector."""

    def test_stallings_full_vector(self):
        # Plaintext: 0x6F6B, Key: 0xA73B → Ciphertext: 0x0738
        self.assertEqual(saes_encrypt(0x6F6B, 0xA73B), 0x0738)

    def test_output_is_16bit(self):
        result = saes_encrypt(0x6F6B, 0xA73B)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 0xFFFF)

    def test_different_keys_produce_different_ciphertext(self):
        c1 = saes_encrypt(0x6F6B, 0xA73B)
        c2 = saes_encrypt(0x6F6B, 0x0000)
        self.assertNotEqual(c1, c2)

    def test_different_plaintexts_produce_different_ciphertext(self):
        c1 = saes_encrypt(0x6F6B, 0xA73B)
        c2 = saes_encrypt(0x0000, 0xA73B)
        self.assertNotEqual(c1, c2)


class TestCTRMode(unittest.TestCase):
    def test_increment_counter_normal(self):
        self.assertEqual(increment_counter(0), 1)
        self.assertEqual(increment_counter(100), 101)
        self.assertEqual(increment_counter(65534), 65535)

    def test_increment_counter_wraps_at_max(self):
        self.assertEqual(increment_counter(65535), 0)

    def test_ctr_process_block_encrypt_decrypt(self):
        # CTR is symmetric: encrypt then decrypt must return original
        block = 0x6F6B
        key = 0xA73B
        counter = 0
        encrypted = ctr_process_block(block, counter, key)
        decrypted = ctr_process_block(encrypted, counter, key)
        self.assertEqual(decrypted, block)

    def test_ctr_different_counters_produce_different_keystreams(self):
        block = 0xFFFF
        key = 0xA73B
        c1 = ctr_process_block(block, 0, key)
        c2 = ctr_process_block(block, 1, key)
        self.assertNotEqual(c1, c2)

    def test_ctr_roundtrip_multiple_blocks(self):
        import os, tempfile
        from ctr_mode import process_file_ctr

        original = b"Hello, S-AES CTR mode test!"
        key = 0xA73B
        counter = 0

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(original)
            src = f.name
        enc = src + ".enc"
        dec = src + ".dec"

        try:
            process_file_ctr(src, enc, key, counter)
            process_file_ctr(enc, dec, key, counter)

            with open(dec, "rb") as f:
                result = f.read()

            self.assertEqual(result, original)

            # Encrypted file must not equal original
            with open(enc, "rb") as f:
                encrypted_bytes = f.read()
            self.assertNotEqual(encrypted_bytes, original)

        finally:
            for path in (src, enc, dec):
                if os.path.exists(path):
                    os.remove(path)

    def test_ctr_roundtrip_odd_byte_count(self):
        """Files with an odd number of bytes must round-trip cleanly."""
        import os, tempfile
        from ctr_mode import process_file_ctr

        original = b"ABC"  # 3 bytes — deliberately odd
        key = 0x1234
        counter = 0

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(original)
            src = f.name
        enc = src + ".enc"
        dec = src + ".dec"

        try:
            process_file_ctr(src, enc, key, counter)
            process_file_ctr(enc, dec, key, counter)

            with open(dec, "rb") as f:
                result = f.read()

            self.assertEqual(result, original)
        finally:
            for path in (src, enc, dec):
                if os.path.exists(path):
                    os.remove(path)


class TestBruteForce(unittest.TestCase):
    def test_recovers_correct_key(self):
        from brute_force import brute_force
        from saes_core import saes_encrypt
        key = 0xA73B
        pt  = 0x6F6B
        counter = 0
        ct = pt ^ saes_encrypt(counter, key)
        self.assertEqual(brute_force(pt, ct, counter), key)


if __name__ == "__main__":
    unittest.main(verbosity=2)
