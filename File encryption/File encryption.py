import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from cryptography.fernet import Fernet

# Function to load or generate a key
def load_key():
    try:
        return open("secret.key", "rb").read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_name, key):
    f = Fernet(key)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_name, "wb") as file:
        file.write(decrypted_data)

def perform_action(action, filename, key):
    try:
        if action == 'Encrypt':
            encrypt_file(filename, key)
            messagebox.showinfo("Success", "File encrypted successfully.")
        elif action == 'Decrypt':
            decrypt_file(filename, key)
            messagebox.showinfo("Success", "File decrypted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_app():
    key = load_key()
    app = tk.Tk()
    app.title("File Encryptor/Decryptor")
    app.geometry("400x150")
    app.configure(bg="#333")

    def file_dialog():
        filename = filedialog.askopenfilename()
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filename)

    def on_submit():
        action = action_var.get()
        filename = file_path_entry.get()
        if not filename:
            messagebox.showwarning("Warning", "Please select a file.")
            return
        perform_action(action, filename, key)

    action_var = tk.StringVar(value="Encrypt")

    tk.Radiobutton(app, text="Encrypt", variable=action_var, value="Encrypt", bg="#333", fg="white").pack()
    tk.Radiobutton(app, text="Decrypt", variable=action_var, value="Decrypt", bg="#333", fg="white").pack()

    tk.Button(app, text="Select File", command=file_dialog, bg="#555", fg="white").pack()

    file_path_entry = tk.Entry(app, bg="#555", fg="white")
    file_path_entry.pack(fill=tk.X, padx=20, pady=5)

    submit_btn = tk.Button(app, text="Submit", command=on_submit, bg="#555", fg="white")
    submit_btn.pack()

    app.mainloop()

if __name__ == "__main__":
    create_app()
