
import json

from shared.key_storage import (
    BASE_DIR,
    VALID_USERS,
    load_public_key
)


# STEP 1: Exchange public keys
def exchange_public_keys():

    # Create contact directories
    person1_contacts = (
        BASE_DIR / "Person_1" / "keys" / "contacts"
    )

    person2_contacts = (
        BASE_DIR / "Person_2" / "keys" / "contacts"
    )

    person1_contacts.mkdir(parents=True, exist_ok=True)
    person2_contacts.mkdir(parents=True, exist_ok=True)

    # Load original public keys
    person1_public = load_public_key("Person_1")
    person2_public = load_public_key("Person_2")

    # Destination paths
    person1_received_key = (
        person1_contacts / "Person_2_public_key.json"
    )

    person2_received_key = (
        person2_contacts / "Person_1_public_key.json"
    )

    # Person 1 receives Person 2's public key
    with open(person1_received_key, "w") as file:
        json.dump(person2_public, file, indent=4)

    # Person 2 receives Person 1's public key
    with open(person2_received_key, "w") as file:
        json.dump(person1_public, file, indent=4)

    print("Public keys exchanged successfully!")

    return person1_received_key, person2_received_key


# STEP 2: Load exchanged public key
def load_contact_public_key(owner, contact):

    if owner not in VALID_USERS or contact not in VALID_USERS:
        raise ValueError("Invalid user")

    if owner == contact:
        raise ValueError("A user cannot be their own contact")

    key_path = (
        BASE_DIR
        / owner
        / "keys"
        / "contacts"
        / f"{contact}_public_key.json"
    )

    if not key_path.exists():
        raise FileNotFoundError(
            f"{contact}'s public key not found for {owner}"
        )

    with open(key_path, "r") as file:
        return json.load(file)
