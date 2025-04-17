import mido
import socket
import time

MAC_IP = "192.168.1.150"
PORT = 3820

def choose_midi_device():
    inputs = mido.get_input_names()
    if not inputs:
        print("❌ No MIDI input devices found.")
        exit(1)

    print("🎹 Available MIDI Input Devices:")
    for i, name in enumerate(inputs):
        print(f"[{i}] {name}")

    while True:
        try:
            selection = int(input("Select MIDI input device number: "))
            if 0 <= selection < len(inputs):
                return inputs[selection]
        except ValueError:
            pass
        print("Invalid selection, try again.")

def connect_to_client():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((MAC_IP, PORT))
            print("🔗 Connected to client!")
            return s
        except (ConnectionRefusedError, OSError):
            print("⏳ Waiting for client...")
            time.sleep(2)

def main():
    device = choose_midi_device()
    print(f"✅ Listening on '{device}'...")
    sock = connect_to_client()

    with mido.open_input(device) as inport:
        while True:
            try:
                for msg in inport.iter_pending():
                    if msg.type == "control_change" and msg.value:
                        if msg.control == 116:
                            print("← LEFT triggered")
                            sock.sendall(b"left")
                        elif msg.control == 117:
                            print("→ RIGHT triggered")
                            sock.sendall(b"right")
                time.sleep(0.01)

            except (BrokenPipeError, ConnectionResetError):
                print("⚠️ Lost connection to client. Reconnecting...")
                sock.close()
                sock = connect_to_client()

if __name__ == "__main__":
    main()

