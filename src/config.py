import secrets as secretslib
from pathlib import Path

import yaml

SECRETS_PATH = Path("secrets.yml")
with SECRETS_PATH.open() as f:
    secrets = yaml.safe_load(f)

SECRET_KEY_PATH = Path("secret_key.txt")
if not SECRET_KEY_PATH.exists():
    # Generate random 32 characters hex string
    secret_key = secretslib.token_hex(32)
    SECRET_KEY_PATH.write_text(secret_key)
else:
    secret_key = SECRET_KEY_PATH.read_text()
