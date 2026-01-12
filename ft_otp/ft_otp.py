#!/usr/bin/env python3

import sys
import base64
import time
import hmac
import hashlib
import os

def ft_otp(file_name):
	try:
		with open(file_name, "r") as f:
			content = f.read()
	except FileNotFoundError:
		print(f"[-] Error: file {file_name} not found")
		sys.exit(1)

	# Decrypt: decode base64 then XOR with password
	password = b"Abc0015"
	decoded = base64.b64decode(content)
	hex_key = bytes([decoded[i] ^ password[i % len(password)] for i in range(len(decoded))])
	
	# Convert hex string to bytes for HMAC
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

	print(f"{otp:06d}")


def save_keys(file_name):
	try:
		with open(file_name, 'r') as file:
			content = file.read()
	except FileNotFoundError:
		print(f"[-] Error: file {file_name} not found")
		sys.exit(1)

	# Remove spaces and newlines
	content = "".join(content.split())

	# Validate length
	if len(content) < 64:
		print(f"./ft_otp: error: key must be 64 hexadecimal characters.")
		sys.exit(1)

	# Validate hexadecimal
	for c in content:
		if c.lower() not in '0123456789abcdef':
			print(f"./ft_otp: error: key must be 64 hexadecimal characters.")
			sys.exit(1)

	# Encrypt: XOR with password then encode base64
	password = b"Abc0015"
	content_bytes = content.encode()
	encrypted = bytes([content_bytes[i] ^ password[i % len(password)] for i in range(len(content_bytes))])
	encoded = base64.b64encode(encrypted).decode('utf-8')

	# Save to file
	with open("ft_otp.key", "w") as k:
		k.write(encoded)

	print("Key was successfully saved in ft_otp.key.")


def generate_qr(file_name):
	"""Generate QR code for TOTP"""
	try:
		import qrcode
	except ImportError:
		print("[-] Error: qrcode library not installed")
		print("[-] Install with: pip3 install qrcode[pil]")
		sys.exit(1)
	
	try:
		with open(file_name, 'r') as file:
			content = file.read()
	except FileNotFoundError:
		print(f"[-] Error: file {file_name} not found")
		sys.exit(1)

	# Remove spaces and newlines
	content = "".join(content.split())

	# Validate length
	if len(content) < 64:
		print(f"./ft_otp: error: key must be 64 hexadecimal characters.")
		sys.exit(1)

	# Validate hexadecimal
	for c in content:
		if c.lower() not in '0123456789abcdef':
			print(f"./ft_otp: error: key must be 64 hexadecimal characters.")
			sys.exit(1)

	# Convert hex to base32 for TOTP URI
	hex_bytes = bytes.fromhex(content)
	base32_key = base64.b32encode(hex_bytes).decode('utf-8')
	
	# Create TOTP URI
	# Format: otpauth://totp/LABEL?secret=SECRET&issuer=ISSUER
	issuer = "ft_otp"
	account = os.getenv('USER', 'user')
	totp_uri = f"otpauth://totp/{issuer}:{account}?secret={base32_key}&issuer={issuer}&algorithm=SHA1&digits=6&period=30"
	
	# Generate QR code
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(totp_uri)
	qr.make(fit=True)
	
	# Save QR code as image
	img = qr.make_image(fill_color="black", back_color="white")
	img.save("ft_otp_qr.png")
	
	print("[+] QR code generated successfully: ft_otp_qr.png")
	print("[+] Scan this QR code with Google Authenticator or similar app")
	print(f"[+] Account: {account}")
	print(f"[+] Issuer: {issuer}")


if len(sys.argv) < 2:
	print("Usage:")
	print("  ft_otp -g <hexkey_file>  : Store a key")
	print("  ft_otp -k <key_file>     : Generate OTP")
	print("  ft_otp -qr <hexkey_file> : Generate QR code")
	sys.exit(1)

if sys.argv[1] == "-g":
	if len(sys.argv) != 3:
		print("Usage: ft_otp -g <hexkey_file>")
		sys.exit(1)
	file_name = sys.argv[2]
	save_keys(file_name)

elif sys.argv[1] == "-k":
	if len(sys.argv) != 3:
		print("Usage: ft_otp -k <key_file>")
		sys.exit(1)
	file_name = sys.argv[2]
	ft_otp(file_name)

elif sys.argv[1] == "-qr":
	if len(sys.argv) != 3:
		print("Usage: ft_otp -qr <hexkey_file>")
		sys.exit(1)
	file_name = sys.argv[2]
	generate_qr(file_name)

else:
	print(f"[-] Error: Unknown flag '{sys.argv[1]}'")
	print("Use -g, -k, or -qr")
	sys.exit(1)
