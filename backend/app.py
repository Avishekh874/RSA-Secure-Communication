
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO

from backend.socket_handler import (
    register_socket_events,
    terminal_send_message
)


# ======================================
# 1. INITIALIZE FLASK APPLICATION
# ======================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "development-secret-key"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

register_socket_events(socketio)


# ======================================
# 2. FRONTEND DIRECTORY
# ======================================

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


# ======================================
# 3. HEALTH CHECK ROUTE
# ======================================

@app.route("/")
def home():

    return jsonify({
        "status": "running",
        "application": "RSA Secure Communication",
        "message": "Backend server is working!"
    })


# ======================================
# 4. FRONTEND ROUTES
# ======================================

@app.route("/person1")
def person1_dashboard():

    return send_from_directory(
        FRONTEND_DIR,
        "person1.html"
    )


@app.route("/person2")
def person2_dashboard():

    return send_from_directory(
        FRONTEND_DIR,
        "person2.html"
    )


@app.route("/style.css")
def frontend_css():

    return send_from_directory(
        FRONTEND_DIR,
        "style.css"
    )


@app.route("/script.js")
def frontend_js():

    return send_from_directory(
        FRONTEND_DIR,
        "script.js"
    )


# ======================================
# 5. BACKEND TERMINAL CONSOLE
# ======================================




def terminal_console():

    print("\n" + "=" * 50)
    print("       RSA BACKEND LIVE CONSOLE")
    print("=" * 50)

    print("\nFrontend messages will appear here automatically.")

    while True:

        print("\n----------- SELECT BACKEND SENDER -----------")
        print("1. Person_1")
        print("2. Person_2")
        print("Type 'exit' to stop.")

        choice = input("\nChoose option: ").strip()

        if choice.lower() == "exit":
            print("Terminal console stopped.")
            break

        if choice == "1":
            sender = "Person_1"
            receiver = "Person_2"

        elif choice == "2":
            sender = "Person_2"
            receiver = "Person_1"

        else:
            print("Invalid option. Please enter 1 or 2.")
            continue

        print("\n" + "=" * 45)
        print(f"[BACKEND SENDER] {sender}")
        print(f"[BACKEND RECEIVER] {receiver}")
        print("=" * 45)

        print("Type 'switch' to change sender.")
        print("Type 'exit' to stop.")

        while True:

            plaintext = input(f"\n{sender}: ").strip()

            if plaintext.lower() == "switch":
                print("\nSwitching sender...")
                break

            if plaintext.lower() == "exit":
                print("Terminal console stopped.")
                return

            if not plaintext:
                print("Message cannot be empty.")
                continue

            terminal_send_message(
                socketio,
                sender,
                receiver,
                plaintext
            )





# ======================================
# 6. APPLICATION ENTRY POINT
# ======================================

if __name__ == "__main__":

    print("=" * 50)
    print("RSA SECURE COMMUNICATION SERVER")
    print("=" * 50)

    # Start terminal console in background
    socketio.start_background_task(terminal_console)

    # Start Flask + Socket.IO server
    socketio.run(
        app,
        host="127.0.0.1",
        port=5000,
        debug=False,
        allow_unsafe_werkzeug=True
    )
