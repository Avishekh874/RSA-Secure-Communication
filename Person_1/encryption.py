
from shared.public_key_exchange import load_contact_public_key


# ---------------------------------------
# STEP 1: Convert plaintext into integer
# ---------------------------------------

def text_to_integer(message):

    message_bytes = message.encode("utf-8")

    message_integer = int.from_bytes(
        message_bytes,
        byteorder="big"
    )

    return message_bytes, message_integer


# ---------------------------------------
# STEP 2: RSA Encryption
# ---------------------------------------

def encrypt_message(message, receiver="Person_2"):

    if not isinstance(message, str) or not message:
        raise ValueError("Message must be a non-empty string")

    # Load receiver's public key
    public_key = load_contact_public_key(
        owner="Person_1",
        contact=receiver
    )

    e = public_key["e"]
    n = public_key["n"]

    # Convert text into integer
    message_bytes, M = text_to_integer(message)

    # Check RSA message-size requirement
    if M >= n:
        raise ValueError(
            "Message is too large for this RSA key. "
            "Maximum supported message size is 255 UTF-8 bytes."
        )

    # RSA encryption: C = M^e mod n
    C = pow(M, e, n)

    # Display educational conversion process
    print("\n========== RSA ENCRYPTION ==========")

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
