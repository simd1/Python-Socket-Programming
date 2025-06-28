import socket
import threading
import tkinter as tk

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client")

        self.text_area = tk.Text(root, state='disabled', width=50, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.pack(padx=10, pady=5, side=tk.LEFT)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.LEFT)

        self.client_socket = None
        self.connect()

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 65430))  # Change IP if needed
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.sendall(message.encode())
            self.log_message(f"You: {message}")
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                self.log_message(data.decode())
            except ConnectionResetError:
                break
        self.client_socket.close()

    def log_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
