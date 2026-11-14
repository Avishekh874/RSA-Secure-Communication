
from shared.key_storage import load_private_key


# STEP 1: RSA Decryption
def decrypt_message(encrypted_data, sender="Person_2"):

    if sender != "Person_2":
        raise ValueError("Invalid sender")

    if not isinstance(encrypted_data, dict):
        raise ValueError("Invalid encrypted message")

    ciphertext = encrypted_data.get("ciphertext")
    byte_length = encrypted_data.get("byte_length")

    if not isinstance(ciphertext, str) or not ciphertext.isdigit():
        raise ValueError("Invalid ciphertext")

    if type(byte_length) is not int or byte_length <= 0:
        raise ValueError("Invalid byte length")

    # Load Person 1's private key
    private_key = load_private_key("Person_1")

    d = private_key["d"]
    n = private_key["n"]

    C = int(ciphertext)

    if C >= n:
        raise ValueError("Ciphertext must be smaller than n")

    # RSA decryption: M = C^d mod n
    M = pow(C, d, n)

    if M >= 1 << (8 * byte_length):
        raise ValueError("Invalid decrypted message length")

    # Integer to bytes
    decrypted_bytes = M.to_bytes(
        byte_length,
        byteorder="big"
    )

    # Bytes to original text
    original_message = decrypted_bytes.decode("utf-8")

    # Display decryption process
    print("\n========== RSA DECRYPTION ==========")

    print("Sender: Person_2")
    print("Receiver: Person_1")
    print("Received ciphertext (C):", C)
    print("Private exponent (d):", d)
    print("Modulus (n):", n)

    print("\nRSA Operation:")
    print("M = C^d mod n")

    print("Recovered integer (M):", M)
    print("Recovered UTF-8 bytes:", decrypted_bytes)
    print("Original message:", original_message)

    print("\n========== DECRYPTION COMPLETE ==========")

    return original_message
