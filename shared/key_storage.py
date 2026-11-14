
import secrets
import json
from pathlib import Path


# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent
VALID_USERS = {"Person_1", "Person_2"}


# STEP 1: GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# STEP 2: Miller-Rabin primality test
def is_prime(number, rounds=40):

    if number < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    for prime in small_primes:
        if number == prime:
            return True
        if number % prime == 0:
            return False

    d = number - 1
    r = 0

    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(rounds):

        a = secrets.randbelow(number - 3) + 2
        x = pow(a, d, number)

        if x == 1 or x == number - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, number)

            if x == number - 1:
                break
        else:
            return False

    return True


# STEP 3: Generate prime number
def generate_prime(bits=1024):

    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1

        if is_prime(candidate):
            return candidate


# STEP 4: Extended Euclidean Algorithm
# Calculate modular inverse
def mod_inverse(e, phi):

    old_r, r = e, phi
    old_s, s = 1, 0

    while r != 0:
        quotient = old_r // r

        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s

    if old_r != 1:
        raise ValueError("Modular inverse does not exist")

    return old_s % phi


# STEP 5: Generate RSA key pair
def generate_key_pair():

    e = 65537

    while True:

        p = generate_prime(1024)
        q = generate_prime(1024)

        if p == q:
            continue

        n = p * q

        # Ensure exactly 2048-bit modulus
        if n.bit_length() != 2048:
            continue

        phi = (p - 1) * (q - 1)

        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    public_key = {
        "e": e,
        "n": n
    }

    private_key = {
        "d": d,
        "n": n,
        "p": p,
        "q": q
    }

    return public_key, private_key


# STEP 6: Save keys
def save_keys(person_name, public_key, private_key):

    if person_name not in VALID_USERS:
        raise ValueError("Invalid person name")

    key_directory = BASE_DIR / person_name / "keys"
    key_directory.mkdir(parents=True, exist_ok=True)

    public_path = key_directory / "public_key.json"
    private_path = key_directory / "private_key.json"

    with open(public_path, "w") as file:
        json.dump(public_key, file, indent=4)

    with open(private_path, "w") as file:
        json.dump(private_key, file, indent=4)

    print(f"\nKeys saved for {person_name}")
    print(f"Public key: {public_path}")
    print(f"Private key: {private_path}")


# STEP 7: Load public key
def load_public_key(person_name):

    if person_name not in VALID_USERS:
        raise ValueError("Invalid person name")

    key_path = (
        BASE_DIR / person_name / "keys" / "public_key.json"
    )

    if not key_path.exists():
        raise FileNotFoundError("Public key not found")

    with open(key_path, "r") as file:
        return json.load(file)


# STEP 8: Load private key
def load_private_key(person_name):

    if person_name not in VALID_USERS:
        raise ValueError("Invalid person name")

    key_path = (
        BASE_DIR / person_name / "keys" / "private_key.json"
    )

    if not key_path.exists():
        raise FileNotFoundError("Private key not found")

    with open(key_path, "r") as file:
        return json.load(file)
