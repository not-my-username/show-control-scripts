import mido
import socket
import time

MAC_IP = "192.168.1.150"
PORT = 5005

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

def send_command(direction):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((MAC_IP, PORT))
            s.sendall(direction.encode())
    except ConnectionRefusedError:
        print("⚠️ Could not connect to client")

def main():
    device = choose_midi_device()
    print(f"✅ Listening on '{device}'...")
    with mido.open_input(device) as inport:
        while True:
            for msg in inport.iter_pending():
                if msg.type == "control_change" and msg.value:
                    if msg.control == 116:
                        print("← LEFT triggered")
                        send_command("left")
                    elif msg.control == 117:
                        print("→ RIGHT triggered")
                        send_command("right")
            time.sleep(0.01)

if __name__ == "__main__":
    main()


