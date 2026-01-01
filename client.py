import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

# --- Network Setup ---
HOST = '127.0.0.1'
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# --- GUI Setup ---
root = tk.Tk()
root.title("Chat Client")
root.geometry("500x500")

messages_frame = tk.Frame(root)
scrollbar = tk.Scrollbar(messages_frame)
msg_list = scrolledtext.ScrolledText(messages_frame, height=20, width=60, state='disabled')
msg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
messages_frame.pack(pady=10)

online_label = tk.Label(root, text="Online Users: ", anchor='w')
online_label.pack(fill=tk.X, padx=10)

entry_msg = tk.Entry(root, width=40)
entry_msg.pack(side=tk.LEFT, padx=(10,0), pady=10)
send_btn = tk.Button(root, text="Send")
send_btn.pack(side=tk.LEFT, padx=10, pady=10)

nickname = simpledialog.askstring("Nickname", "Choose a nickname:")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICKNAME":
                client.send(nickname.encode('utf-8'))
            elif message.startswith("/online "):
                users = message.replace("/online ", "").split(",")
                online_label.config(text="Online Users: " + ", ".join(users))
            else:
                msg_list.config(state='normal')
                msg_list.insert(tk.END, message + "\n")
                msg_list.yview(tk.END)
                msg_list.config(state='disabled')
        except:
            messagebox.showerror("Error", "Connection lost.")
            client.close()
            break

def send():
    msg = entry_msg.get()
    if msg.startswith("/nick "):
        new_nick = msg.split(" ",1)[1]
        client.send(f"/nickname {new_nick}".encode('utf-8'))
        global nickname
        nickname = new_nick
    else:
        client.send(f"{nickname}: {msg}".encode('utf-8'))
    entry_msg.delete(0, tk.END)

send_btn.config(command=send)
entry_msg.bind("<Return>", lambda event: send())

# Start threads
receive_thread = threading.Thread(target=receive)
receive_thread.daemon = True
receive_thread.start()

root.mainloop()
