
from flask import request
from flask_socketio import emit, join_room

from backend.message_manager import create_message_envelope

from Person_1.encryption import encrypt_message as person1_encrypt
from Person_2.encryption import encrypt_message as person2_encrypt

from Person_1.decryption import decrypt_message as person1_decrypt
from Person_2.decryption import decrypt_message as person2_decrypt


connected_users = {}

VALID_USERS = {"Person_1", "Person_2"}


# =====================================================
# RSA MESSAGE PROCESSING
# =====================================================

def process_rsa_message(socketio, sender, receiver, plaintext, source='frontend'):

    if sender not in VALID_USERS or receiver not in VALID_USERS:
        raise ValueError("Invalid sender or receiver")

    if sender == receiver:
        raise ValueError("Sender and receiver cannot be the same")

    if not isinstance(plaintext, str) or not plaintext.strip():
        raise ValueError("Message cannot be empty")

    print("\n========== RSA ENCRYPTION STARTED ==========")

    # Encrypt using receiver's public key
    if sender == "Person_1" and receiver == "Person_2":

        encrypted_data = person1_encrypt(
            plaintext,
            receiver="Person_2"
        )

    elif sender == "Person_2" and receiver == "Person_1":

        encrypted_data = person2_encrypt(
            plaintext,
            receiver="Person_1"
        )

    else:
        raise ValueError("Invalid communication direction")

    # Create message envelope
    message = create_message_envelope(
        sender=sender,
        receiver=receiver,
        encrypted_data=encrypted_data
    )

    # Decrypt using receiver's private key
    print("\n========== RSA DECRYPTION STARTED ==========")

    if receiver == "Person_1":

        decrypted_message = person1_decrypt(
            encrypted_data,
            sender="Person_2"
        )

    else:

        decrypted_message = person2_decrypt(
            encrypted_data,
            sender="Person_1"
        )

    # Deliver to receiver's dashboard
    payload = {
        **message,
        "message": decrypted_message
    }

        # Always deliver to the receiver
    socketio.emit(
        "receive_message",
        payload,
        to=receiver
    )

    # For backend-originated messages, also update the sender's dashboard
    if source == "backend":
        socketio.emit(
            "receive_message",
            payload,
            to=sender
        )

    print("\n============================================")
    print(f"[DELIVERED] {sender} -> {receiver}")
    print(f"[MESSAGE] {decrypted_message}")
    print("============================================")

    return message


# =====================================================
# BACKEND TERMINAL MESSAGING
# =====================================================

def terminal_send_message(socketio, sender, receiver, plaintext):

    try:

        message = process_rsa_message(
            socketio,
            sender,
            receiver,
            plaintext,source='backend'
        )

        print(f"\n[BACKEND MESSAGE] {sender} -> {receiver}")
        print(f"[MESSAGE ID] {message['message_id']}")

    except (ValueError, TypeError, FileNotFoundError) as error:

        print("\n[TERMINAL MESSAGE ERROR]", error)

    except Exception as error:

        print("\n[UNEXPECTED ERROR]", error)


# =====================================================
# SOCKET.IO EVENT REGISTRATION
# =====================================================

def register_socket_events(socketio):

    @socketio.on("connect")
    def handle_connect(auth):

        if not isinstance(auth, dict):
            return False

        username = auth.get("username")

        if username not in VALID_USERS:
            return False

        connected_users[request.sid] = username

        join_room(username)

        print(f"\n[CONNECTED] {username}")

        emit(
            "connection_status",
            {"message": f"Welcome, {username}!"}
        )

    # ---------------------------------------------
    # FRONTEND -> BACKEND -> RECEIVER
    # ---------------------------------------------

    @socketio.on("send_message")
    def handle_send_message(data):

        sender = connected_users.get(request.sid)

        if not sender:

            emit(
                "message_error",
                {"error": "Not authenticated"}
            )
            return

        if not isinstance(data, dict):

            emit(
                "message_error",
                {"error": "Invalid message data"}
            )
            return

        receiver = data.get("receiver")
        plaintext = data.get("message")

        try:

            print("\n" + "=" * 55)
            print(f"[FRONTEND] {sender} -> {receiver}")
            print(f"[MESSAGE] {plaintext}")
            print("=" * 55)

            message = process_rsa_message(
                socketio,
                sender,
                receiver,
                plaintext
            )

            emit(
                "message_sent",
                {
                    "message_id": message["message_id"],
                    "status": "success"
                }
            )

        except (ValueError, TypeError, FileNotFoundError) as error:

            emit(
                "message_error",
                {"error": str(error)}
            )

        except Exception as error:

            print("\n[UNEXPECTED ERROR]", error)

            emit(
                "message_error",
                {"error": "Message processing failed"}
            )

    # ---------------------------------------------
    # USER DISCONNECTION
    # ---------------------------------------------

    @socketio.on("disconnect")
    def handle_disconnect(reason=None):

        username = connected_users.pop(request.sid, None)

        if username:

            print(f"\n[DISCONNECTED] {username}")
