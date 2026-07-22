import json
import os
import sys
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64

# Load plain accounts from accounts_import.json
json_path = r"C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault\accounts_import.json"
with open(json_path, "r", encoding="utf-8") as f:
    accounts = json.load(f)

master_pass = "12345678"
salt = os.urandom(32)
iv = os.urandom(12)

# Derive key using PBKDF2 HMAC SHA-256 with 600,000 iterations
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=600000,
)
key = kdf.derive(master_pass.encode("utf-8"))

# AES-256-GCM encrypt
aesgcm = AESGCM(key)
data_json_bytes = json.dumps(accounts, ensure_ascii=False).encode("utf-8")
ciphertext = aesgcm.encrypt(iv, data_json_bytes, None)

encrypted_payload = {
    "salt": base64.b64encode(salt).decode("utf-8"),
    "iv": base64.b64encode(iv).decode("utf-8"),
    "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    "appName": "Zero-Knowledge Vault",
    "version": "1.0",
    "note": f"Encrypted 42 accounts. Master Password: {master_pass}"
}

out_path = r"C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault\zk_vault_encrypted_42_accounts.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(encrypted_payload, f, ensure_ascii=False, indent=2)

print(f"Created pre-encrypted ZK Backup file with 42 accounts at: {out_path}")
