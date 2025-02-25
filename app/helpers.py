import logging
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
logging.basicConfig(level=logging.INFO)

def hash_password(password):
    if not password:
        logging.error("Password cannot be empty or None")
        raise ValueError("Password cannot be empty or None")

    try:
        return bcrypt.generate_password_hash(password).decode('utf-8')
    except Exception as e:
        logging.error(f"Error hashing password: {e}")
        raise

def check_password(hash, password):
    if not hash or not password:
        logging.error("Hash and password cannot be empty or None")
        raise ValueError("Hash and password cannot be empty or None")

    try:
        return bcrypt.check_password_hash(hash, password)
    except Exception as e:
        logging.error(f"Error checking password: {e}")
        raise
