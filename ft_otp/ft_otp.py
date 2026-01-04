#!/usr/bin/env python3

import sys
import base64
import time
import hmac
import hashlib

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


if len(sys.argv) != 3:
	print("Usage:")
	print("  ft_otp -g <hexkey_file>  : Store a key")
	print("  ft_otp -k <key_file>     : Generate OTP")
	sys.exit(1)

if sys.argv[1] == "-g":
	file_name = sys.argv[2]
	save_keys(file_name)

elif sys.argv[1] == "-k":
	file_name = sys.argv[2]
	ft_otp(file_name)

else:
	print(f"[-] Error: Unknown flag '{sys.argv[1]}'")
	print("Use -g or -k")
	sys.exit(1)
