
import uuid
from datetime import datetime, timezone

from shared.key_storage import (
    VALID_USERS,
    load_public_key
)


def create_message_envelope(sender, receiver, encrypted_data):
    """
    Validate and prepare a textbook RSA encrypted
    message for transmission.
    """

    # STEP 1: Validate sender
    if sender not in VALID_USERS:
        raise ValueError("Invalid sender")

    # STEP 2: Validate receiver
    if receiver not in VALID_USERS:
        raise ValueError("Invalid receiver")

    if sender == receiver:
        raise ValueError(
            "Sender and receiver cannot be the same"
        )

    # STEP 3: Validate encrypted data
    if not isinstance(encrypted_data, dict):
        raise ValueError("Invalid encrypted message")

    ciphertext = encrypted_data.get("ciphertext")
    byte_length = encrypted_data.get("byte_length")

    if (
        not isinstance(ciphertext, str)
        or not ciphertext.isdigit()
    ):
        raise ValueError("Invalid RSA ciphertext")

    if type(byte_length) is not int or not 1 <= byte_length <= 255:
        raise ValueError("Invalid message byte length")

    # STEP 4: Convert ciphertext into integer
    C = int(ciphertext)

    # STEP 5: Load receiver's public key for validation
    receiver_public_key = load_public_key(receiver)

    n = receiver_public_key["n"]

    if not 0 < C < n:
        raise ValueError("Ciphertext is outside the valid RSA range")

    # STEP 6: Prepare message envelope
    message = {
        "message_id": str(uuid.uuid4()),
        "sender": sender,
        "receiver": receiver,
        "ciphertext": ciphertext,
        "byte_length": byte_length,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return message
