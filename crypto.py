import os
import binascii
from cryptography.fernet import Fernet
from tkinter import Tk, filedialog, messagebox, Button

def encrypt():

    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    with open(file_path, 'r') as file:
        txt = file.read()

    key = Fernet.generate_key()

    cipher = Fernet(key)
    encrypted_txt = cipher.encrypt(txt.encode())
    hexed = binascii.hexlify(encrypted_txt).decode()
    bined = bin(int(hexed, 16))[2:]

    directory, filename = os.path.split(file_path)
    encrypted_file_path = os.path.join(directory, f"{filename}.encrypted")

    with open(encrypted_file_path, 'w') as encrypted_file:
        encrypted_file.write(bined)

    key_file_path = os.path.join(directory, f"{filename}.encrypted.key")
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)

    messagebox.showinfo("Encryption Result", f"File encrypted and saved at:\n{encrypted_file_path}")

def decrypt():

    encrypted_file_path = filedialog.askopenfilename()
    if not encrypted_file_path:
        return

    with open(encrypted_file_path, 'r') as file:
        encrypted_txt = file.read()

    directory, filename = os.path.split(encrypted_file_path)

    key_file_path = os.path.join(directory, f"{filename}.key")

    if not os.path.exists(key_file_path):
        messagebox.showinfo("Error", "No key file found.")
        return

    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

    cipher = Fernet(key)
    hexed = hex(int(encrypted_txt, 2))[2:].zfill(len(encrypted_txt) // 4)
    encrypted_txt_bytes = binascii.unhexlify(hexed)
    decrypted_txt = cipher.decrypt(encrypted_txt_bytes)

    decrypted_file_path = os.path.join(directory, f"{filename}.decrypted")
    with open(decrypted_file_path, 'w') as decrypted_file:
        decrypted_file.write(decrypted_txt.decode())

    messagebox.showinfo("Decryption Result", f"File decrypted and saved at:\n{decrypted_file_path}")

root = Tk()
root.title("File Encryption/Decryption")

encrypt_button = Button(root, text="Encrypt", command=encrypt)
encrypt_button.grid(row=0, column=0, padx=10, pady=10)

decrypt_button = Button(root, text="Decrypt", command=decrypt)
decrypt_button.grid(row=0, column=1, padx=10, pady=10)

root.mainloop()
