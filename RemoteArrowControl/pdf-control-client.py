import socket
import subprocess

HOST = '0.0.0.0'
PORT = 5005

def press_arrow(direction):
    key_code = 123 if direction == "left" else 124  # 123 = left, 124 = right
    subprocess.run([
        "osascript", "-e",
        f'tell application "System Events" to key code {key_code}'
    ])

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Listening on {HOST}:{PORT}...")
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                print(f"Received: {data}")
                if data == "left":
                    press_arrow("left")
                elif data == "right":
                    press_arrow("right")

if __name__ == "__main__":
    main()

