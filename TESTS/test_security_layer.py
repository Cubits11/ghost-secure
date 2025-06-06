
import unittest
from BACKEND.security.security_layer import (
    encrypt_entry,
    decrypt_entry,
    load_or_generate_key,
    FERNET_KEY_PATH
)
import os

class TestSecurityLayer(unittest.TestCase):

    def setUp(self):
        self.sample_text = "Confidential journal entry from Ghost."
        self.corrupted_token = "invalid-token"

    def test_key_generation_and_loading(self):
        key = load_or_generate_key()
        self.assertTrue(isinstance(key, bytes))
        self.assertTrue(os.path.exists(FERNET_KEY_PATH))

    def test_encrypt_decrypt_roundtrip(self):
        encrypted = encrypt_entry(self.sample_text)
        decrypted = decrypt_entry(encrypted)
        self.assertEqual(decrypted, self.sample_text)

    def test_tampered_token_detection(self):
        result = decrypt_entry(self.corrupted_token)
        self.assertEqual(result, "[Error: Corrupted or tampered data]")

    def tearDown(self):
        pass  # Optional: Cleanup logic if needed

if __name__ == "__main__":
    unittest.main()
