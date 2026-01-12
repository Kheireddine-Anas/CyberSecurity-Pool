#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import base64
import time
import hmac
import hashlib
import os
from threading import Thread

class FTOTP_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ft_otp - TOTP Generator")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Set theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.otp_value = tk.StringVar(value="------")
        self.time_remaining = tk.StringVar(value="30")
        self.key_file_path = tk.StringVar(value="")
        self.update_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="ft_otp",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Store Key
        store_frame = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(store_frame, text="Store Key")
        self.setup_store_tab(store_frame)
        
        # Tab 2: Generate OTP
        generate_frame = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(generate_frame, text="Generate OTP")
        self.setup_generate_tab(generate_frame)
        
        # Tab 3: QR Code
        qr_frame = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(qr_frame, text="QR Code")
        self.setup_qr_tab(qr_frame)
        
    def setup_store_tab(self, parent):
        # Instructions
        info_label = tk.Label(
            parent,
            text="Store a hexadecimal key (minimum 64 characters)",
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        info_label.pack(pady=20)
        
        # File selection
        file_frame = tk.Frame(parent, bg="#ecf0f1")
        file_frame.pack(pady=10)
        
        tk.Label(
            file_frame,
            text="Key File:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        self.store_file_entry = tk.Entry(file_frame, width=30, font=("Arial", 10))
        self.store_file_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(
            file_frame,
            text="Browse",
            command=self.browse_key_file
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Store button
        store_btn = ttk.Button(
            parent,
            text="Store Key",
            command=self.store_key,
            width=20
        )
        store_btn.pack(pady=20)
        
        # Status
        self.store_status = tk.Label(
            parent,
            text="",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#27ae60"
        )
        self.store_status.pack(pady=10)
        
    def setup_generate_tab(self, parent):
        # Instructions
        info_label = tk.Label(
            parent,
            text="Generate TOTP from stored key",
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        info_label.pack(pady=20)
        
        # OTP Display
        otp_frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=2)
        otp_frame.pack(pady=20, padx=50)
        
        otp_label = tk.Label(
            otp_frame,
            textvariable=self.otp_value,
            font=("Courier New", 48, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        otp_label.pack(padx=40, pady=20)
        
        # Timer
        time_label = tk.Label(
            parent,
            textvariable=self.time_remaining,
            font=("Arial", 16),
            bg="#ecf0f1",
            fg="#e74c3c"
        )
        time_label.pack(pady=5)
        
        tk.Label(
            parent,
            text="seconds remaining",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack()
        
        # Buttons
        btn_frame = tk.Frame(parent, bg="#ecf0f1")
        btn_frame.pack(pady=20)
        
        generate_btn = ttk.Button(
            btn_frame,
            text="Generate OTP",
            command=self.start_otp_generation,
            width=15
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ttk.Button(
            btn_frame,
            text="Stop",
            command=self.stop_otp_generation,
            width=15
        )
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.gen_status = tk.Label(
            parent,
            text="",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#e74c3c"
        )
        self.gen_status.pack(pady=10)
        
    def setup_qr_tab(self, parent):
        # Instructions
        info_label = tk.Label(
            parent,
            text="Generate QR code for mobile authenticator apps",
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        info_label.pack(pady=20)
        
        # File selection
        file_frame = tk.Frame(parent, bg="#ecf0f1")
        file_frame.pack(pady=10)
        
        tk.Label(
            file_frame,
            text="Key File:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT, padx=5)
        
        self.qr_file_entry = tk.Entry(file_frame, width=30, font=("Arial", 10))
        self.qr_file_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = ttk.Button(
            file_frame,
            text="Browse",
            command=self.browse_qr_file
        )
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Generate QR button
        qr_btn = ttk.Button(
            parent,
            text="Generate QR Code",
            command=self.generate_qr,
            width=20
        )
        qr_btn.pack(pady=20)
        
        # Status
        self.qr_status = tk.Label(
            parent,
            text="",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#27ae60"
        )
        self.qr_status.pack(pady=10)
        
        # Info
        info_text = "Scan the generated QR code with:\n• Google Authenticator\n• Microsoft Authenticator\n• Authy"
        tk.Label(
            parent,
            text=info_text,
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d",
            justify=tk.LEFT
        ).pack(pady=20)
        
    def browse_key_file(self):
        filename = filedialog.askopenfilename(
            title="Select Key File",
            filetypes=[("Hex files", "*.hex"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.store_file_entry.delete(0, tk.END)
            self.store_file_entry.insert(0, filename)
            
    def browse_qr_file(self):
        filename = filedialog.askopenfilename(
            title="Select Key File",
            filetypes=[("Hex files", "*.hex"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.qr_file_entry.delete(0, tk.END)
            self.qr_file_entry.insert(0, filename)
            
    def store_key(self):
        file_name = self.store_file_entry.get()
        if not file_name:
            self.store_status.config(text="Please select a file", fg="#e74c3c")
            return
            
        try:
            with open(file_name, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            self.store_status.config(text=f"File not found: {file_name}", fg="#e74c3c")
            return
            
        # Remove spaces and newlines
        content = "".join(content.split())
        
        # Validate
        if len(content) < 64:
            self.store_status.config(text="Key must be 64 hexadecimal characters", fg="#e74c3c")
            return
            
        for c in content:
            if c.lower() not in '0123456789abcdef':
                self.store_status.config(text="Key must be hexadecimal characters", fg="#e74c3c")
                return
                
        # Encrypt and save
        password = b"Abc0015"
        content_bytes = content.encode()
        encrypted = bytes([content_bytes[i] ^ password[i % len(password)] for i in range(len(content_bytes))])
        encoded = base64.b64encode(encrypted).decode('utf-8')
        
        with open("ft_otp.key", "w") as k:
            k.write(encoded)
            
        self.store_status.config(text="✓ Key saved successfully in ft_otp.key", fg="#27ae60")
        
    def start_otp_generation(self):
        if not os.path.exists("ft_otp.key"):
            self.gen_status.config(text="No key file found. Store a key first.", fg="#e74c3c")
            return
            
        self.update_running = True
        self.gen_status.config(text="", fg="#27ae60")
        Thread(target=self.update_otp, daemon=True).start()
        
    def stop_otp_generation(self):
        self.update_running = False
        self.otp_value.set("------")
        self.time_remaining.set("30")
        
    def update_otp(self):
        while self.update_running:
            try:
                # Read and decrypt key
                with open("ft_otp.key", "r") as f:
                    content = f.read()
                    
                password = b"Abc0015"
                decoded = base64.b64decode(content)
                hex_key = bytes([decoded[i] ^ password[i % len(password)] for i in range(len(decoded))])
                key_bytes = bytes.fromhex(hex_key.decode())
                
                # Generate TOTP
                counter = int(time.time()) // 30
                counter_bytes = counter.to_bytes(8, "big")
                
                h = hmac.new(key_bytes, counter_bytes, hashlib.sha1)
                digest = h.digest()
                
                offset = digest[-1] & 0x0f
                part = digest[offset : offset + 4]
                code = int.from_bytes(part, "big")
                code = code & 0x7fffffff
                otp = code % 1000000
                
                # Update display
                self.otp_value.set(f"{otp:06d}")
                
                # Update timer
                remaining = 30 - (int(time.time()) % 30)
                self.time_remaining.set(str(remaining))
                
                time.sleep(1)
                
            except Exception as e:
                self.gen_status.config(text=f"Error: {str(e)}", fg="#e74c3c")
                self.update_running = False
                break
                
    def generate_qr(self):
        file_name = self.qr_file_entry.get()
        if not file_name:
            self.qr_status.config(text="Please select a file", fg="#e74c3c")
            return
            
        try:
            import qrcode
        except ImportError:
            self.qr_status.config(text="qrcode library not installed", fg="#e74c3c")
            messagebox.showerror("Error", "Install qrcode library:\npip3 install qrcode[pil]")
            return
            
        try:
            with open(file_name, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            self.qr_status.config(text=f"File not found: {file_name}", fg="#e74c3c")
            return
            
        # Remove spaces and newlines
        content = "".join(content.split())
        
        # Validate
        if len(content) < 64:
            self.qr_status.config(text="Key must be 64 hexadecimal characters", fg="#e74c3c")
            return
            
        for c in content:
            if c.lower() not in '0123456789abcdef':
                self.qr_status.config(text="Key must be hexadecimal characters", fg="#e74c3c")
                return
                
        # Generate QR code
        hex_bytes = bytes.fromhex(content)
        base32_key = base64.b32encode(hex_bytes).decode('utf-8')
        
        issuer = "ft_otp"
        account = os.getenv('USER', 'user')
        totp_uri = f"otpauth://totp/{issuer}:{account}?secret={base32_key}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("ft_otp_qr.png")
        
        self.qr_status.config(text="✓ QR code saved as ft_otp_qr.png", fg="#27ae60")
        messagebox.showinfo("Success", "QR code generated successfully!\nSaved as: ft_otp_qr.png")


if __name__ == "__main__":
    root = tk.Tk()
    app = FTOTP_GUI(root)
    root.mainloop()
