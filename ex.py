import socket
import threading
import tkinter as tk

class Server:
    def __init__(self, root):
        self.root = root
        self.root.title("server")

        self.text_area = tk.Text(root, state = 'disabled', width = 50, height = 20)
        self.text_area.pack(padx = 10, pady = 10)

        self.start_button = tk.Button(root, text = ("Start server"), command = self.start_server)
        self.start_button.pack(pady = 5)

        self.sever_socket = None

    def start_server(self):
        if self.server_socket is None:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0, 0, 0, 0', 65430))
            self.server_socket.listen(5)
            self.log_message("Server started, waiting for clients")
            threading.Thread(target = self.handle_clients(), daemon = True)
        
    def handle_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.log_message(f"Connected to {client_address}")
            threading.Thread(target = self.accept_connections(), args=(client_socket), daemon=True)

    def accept_connections(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                self.log_message(f"Client: {message}")
                client_socket.sendall(f"Echo: {message}".encode())

            except ConnectionResetError:
                break
        
        client_socket.close()

    def log_message(self, message):
        self.text_area.config(status = 'normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.config(status = 'disabled')
        self.text_area.yview(tk.END)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Server(root)
    root.mainloop()



    