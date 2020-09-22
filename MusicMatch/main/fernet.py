from cryptography.fernet import Fernet

from main.util.util import get_env_var

def get_fernet_key():
    """ Returns the Fernet key in byte format."""

    return get_env_var("FERNET_KEY").encode()

def encrypt_message(message):
    """
    Encrypts a message.
    Args: message, str
    Returns: str
    """
    f = Fernet(get_env_var("FERNET_KEY"))

    return f.encrypt(message.encode()).decode("utf-8")

def decrypt_message(message):
    """
    Decrypts a message.
    Args: message, str
    Returns: str
    """
    f = Fernet(get_env_var("FERNET_KEY"))

    return f.decrypt(message.encode()).decode("utf-8")