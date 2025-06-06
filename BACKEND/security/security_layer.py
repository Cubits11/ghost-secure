# BACKEND/security/security_layer.py
# 🔐 Ghost Secure — Enterprise-Grade Encryption Module v3

import os
import base64
import logging
import hmac
import hashlib
from cryptography.fernet import Fernet, InvalidToken

# 📍 Constants
FERNET_KEY_ENV_VAR = "GHOST_FERNET_KEY"
FERNET_KEY_PATH = os.path.join(os.path.dirname(__file__), "fernet.key")
HMAC_SECRET_ENV_VAR = "GHOST_HMAC_SECRET"
HMAC_SECRET_PATH = os.path.join(os.path.dirname(__file__), "hmac.secret")

logger = logging.getLogger("GhostSecurity")

# ===========================================================
# 🔑 KEY + SECRET MANAGEMENT
# ===========================================================

def load_or_generate_key(path: str, env_var: str, length: int = 32, base64_format: bool = True) -> bytes:
    """
    Load from env or file; if missing, generate and persist.
    """
    env_value = os.getenv(env_var)
    if env_value:
        try:
            decoded = base64.urlsafe_b64decode(env_value.encode()) if base64_format else env_value.encode()
            if len(decoded) == length:
                logger.info(f"[SECURE LOAD] Loaded {env_var} from environment.")
                return env_value.encode() if base64_format else decoded
            else:
                logger.warning(f"[SECURE LOAD] Invalid {env_var} length.")
        except Exception as e:
            logger.warning(f"[SECURE LOAD] Failed decoding {env_var}: {e}")

    if os.path.exists(path):
        with open(path, "rb") as f:
            logger.info(f"[SECURE LOAD] Loaded {os.path.basename(path)} from file.")
            return f.read().strip()

    # Generate
    value = Fernet.generate_key() if base64_format else os.urandom(length)
    with open(path, "wb") as f:
        f.write(value)
    logger.info(f"[SECURE LOAD] Generated and saved new {os.path.basename(path)}.")
    return value

FERNET_KEY = load_or_generate_key(FERNET_KEY_PATH, FERNET_KEY_ENV_VAR)
HMAC_SECRET = load_or_generate_key(HMAC_SECRET_PATH, HMAC_SECRET_ENV_VAR, base64_format=False)
cipher = Fernet(FERNET_KEY)

# ===========================================================
# 🔒 ENCRYPTION + HMAC INTEGRITY LAYER
# ===========================================================

def encrypt_entry(entry: str) -> str:
    if not isinstance(entry, str):
        raise TypeError("Entry must be a string.")
    encrypted = cipher.encrypt(entry.encode())
    hmac_sig = hmac.new(HMAC_SECRET, encrypted, hashlib.sha256).hexdigest()
    return f"{encrypted.decode()}::{hmac_sig}"

def decrypt_entry(token: str) -> str:
    try:
        encrypted_b64, received_sig = token.split("::")
        encrypted_bytes = encrypted_b64.encode()
        expected_sig = hmac.new(HMAC_SECRET, encrypted_bytes, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_sig, received_sig):
            logger.warning("[HMAC] Signature mismatch. Possible tampering.")
            return "[Error: Signature mismatch. Entry tampered.]"

        return cipher.decrypt(encrypted_bytes).decode()
    except InvalidToken:
        logger.error("[FERNET] Invalid decryption token.")
        return "[Error: Corrupted or tampered data]"
    except Exception as e:
        logger.exception(f"[DECRYPT ERROR] Unexpected failure: {e}")
        return "[Error: Decryption failed]"

# ===========================================================
# 🧪 LOCAL TEST MODE
# ===========================================================

if __name__ == "__main__":
    print("\n🔐 Ghost Secure Encryption Test")
    test_entry = "This is a classified ghost memory."
    encrypted = encrypt_entry(test_entry)
    print("Encrypted:", encrypted)

    decrypted = decrypt_entry(encrypted)
    print("Decrypted:", decrypted)

    # 🔧 Tamper Test
    print("\n🔍 Tamper Simulation")
    tampered = encrypted[:-1] + "x"
    print("Decryption Result:", decrypt_entry(tampered))

    # 🔐 Signature Mismatch Test
    print("\n🔐 Signature Mismatch Simulation")
    wrong_sig = encrypted.split("::")[0] + "::abcdef123456"
    print("Mismatch Result:", decrypt_entry(wrong_sig))