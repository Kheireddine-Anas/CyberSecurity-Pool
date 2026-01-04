# ft_otp - Time-based One-Time Password Generator

## Project Overview
This project is a simple implementation of a TOTP (Time-based One-Time Password) generator, following the requirements of the 1337 School Cybersecurity Pool. It allows you to securely store a secret key and generate 6-digit one-time passwords compatible with standard tools like oathtool.

## How It Works
- You provide a secret key in hexadecimal format (at least 64 characters).
- The script can **store** this key in an encrypted file (`ft_otp.key`) using a simple XOR with a password and base64 encoding.
- The script can **generate** a 6-digit OTP code using the stored key and the current time.
- The OTP code matches what you get from `oathtool` using the same key.

## Usage

### 1. Store a Key
```bash
python3 ft_otp.py -g key.hex
```
- Reads the hex key from `key.hex`.
- Validates it (must be 64+ hex characters).
- Encrypts and saves it to `ft_otp.key`.

### 2. Generate an OTP
```bash
python3 ft_otp.py -k ft_otp.key
```
- Decrypts the key from `ft_otp.key`.
- Uses the current time to generate a 6-digit OTP.
- Prints the OTP to the screen.

### 3. Verify with oathtool
```bash
oathtool --totp $(cat key.hex)
```
- This should give the same 6-digit code as your script (if run at the same time).

## How the Technologies Work

### HOTP (HMAC-based One-Time Password)
- **HOTP** is an algorithm that generates a one-time password using a secret key and a counter.
- It uses HMAC-SHA1 to mix the key and counter securely.
- Steps:
	1. Convert the counter to an 8-byte value.
	2. Compute HMAC-SHA1 of the key and counter.
	3. Use dynamic truncation to extract a 4-byte part of the hash.
	4. Convert to an integer, mask the highest bit, and take the last 6 digits.
- The result is a 6-digit code that changes every time the counter increases.

### TOTP (Time-based One-Time Password)
- **TOTP** is an extension of HOTP where the counter is based on time.
- Instead of a manual counter, it uses the number of 30-second intervals since 1970 (Unix time).
- This means the code changes every 30 seconds.
- Steps:
	1. Get the current Unix time (seconds since 1970).
	2. Divide by 30 to get the time-step counter.
	3. Use HOTP with this counter to generate the code.
- TOTP is used in Google Authenticator, Microsoft Authenticator, and many 2FA systems.

## Encryption Method
- The script uses a simple XOR with a password and base64 encoding to "encrypt" the key.
- This is not strong encryption, but it is enough for educational purposes and matches the project requirements.
- Only the script (with the password) can decrypt and use the key.

## File Structure
```
ft_otp/
├── ft_otp.py      # The main script
├── key.hex        # Your original hex key (not committed)
├── ft_otp.key     # Encrypted key file (not committed)
└── README.md      # This file
```

## Notes
- Only use the original `key.hex` with oathtool, not the encrypted file.
- The script is compatible with standard TOTP tools.

## References
- [RFC 4226 - HOTP](https://datatracker.ietf.org/doc/html/rfc4226)
- [RFC 6238 - TOTP](https://datatracker.ietf.org/doc/html/rfc6238)
- [oathtool documentation](https://www.nongnu.org/oath-toolkit/)
