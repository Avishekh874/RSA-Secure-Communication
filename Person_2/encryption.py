
from shared.public_key_exchange import load_contact_public_key


# STEP 1: Convert text into integer
def text_to_integer(message):

    message_bytes = message.encode("utf-8")

    message_integer = int.from_bytes(
        message_bytes,
        byteorder="big"
    )

    return message_bytes, message_integer


# STEP 2: RSA Encryption
def encrypt_message(message, receiver="Person_1"):

    if not isinstance(message, str) or not message:
        raise ValueError("Message must be a non-empty string")

    # Load Person 1's public key
    public_key = load_contact_public_key(
        owner="Person_2",
        contact=receiver
    )

    e = public_key["e"]
    n = public_key["n"]

    # Convert plaintext into integer
    message_bytes, M = text_to_integer(message)

    if M >= n:
        raise ValueError("Message is too large for this RSA key")

    # RSA encryption
    C = pow(M, e, n)

    print("\n========== RSA ENCRYPTION ==========")
    print("Sender: Person_2")
    print("Receiver: Person_1")
    print("Original message:", message)
    print("UTF-8 bytes:", message_bytes)
    print("Integer representation (M):", M)
    print("Public exponent (e):", e)
    print("Modulus (n):", n)
    print("\nRSA Operation:")
    print("C = M^e mod n")
    print("Ciphertext (C):", C)
    print("\n========== ENCRYPTION COMPLETE ==========")

    return {
        "ciphertext": str(C),
        "byte_length": len(message_bytes)
    }
