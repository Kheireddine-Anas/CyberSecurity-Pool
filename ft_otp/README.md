# ft_otp - Time-based One-Time Password Generator

## Project Overview
This project is a complete implementation of a TOTP (Time-based One-Time Password) generator, following the requirements of the 1337 School Cybersecurity Pool. It allows you to securely store a secret key and generate 6-digit one-time passwords compatible with standard tools like oathtool and mobile authenticator apps.

## Features

### Mandatory
- ✅ Store hexadecimal keys (64+ characters) in encrypted format
- ✅ Generate 6-digit TOTP codes based on HOTP algorithm (RFC 4226)
- ✅ Compatible with oathtool and standard TOTP systems
- ✅ Executable named `ft_otp` with command-line interface

### Bonus
- 🎁 **QR Code Generation**: Create QR codes for mobile authenticator apps (Google Authenticator, Microsoft Authenticator, Authy)
- 🎁 **Graphical Interface**: Full-featured GUI with real-time OTP display and countdown timer

## Installation

### Setup
```bash
chmod +x ft_otp
chmod +x ft_otp.py
```

### Dependencies
For bonus features (QR code generation):
```bash
pip3 install qrcode pillow
```

For GUI (if tkinter is not installed):
```bash
# On Debian/Ubuntu
sudo apt-get install python3-tk

# On Fedora/RHEL
sudo dnf install python3-tkinter

# On Arch
sudo pacman -S tk
```

## Usage

### Command Line Interface

#### 1. Store a Key
```bash
./ft_otp -g key.hex
```
or after installation:
```bash
ft_otp -g key.hex
```
- Reads the hex key from `key.hex`
- Validates it (must be 64+ hex characters)
- Encrypts and saves it to `ft_otp.key`

#### 2. Generate an OTP
```bash
./ft_otp -k ft_otp.key
```
or:
```bash
ft_otp -k ft_otp.key
```
- Decrypts the key from `ft_otp.key`
- Uses the current time to generate a 6-digit OTP
- Prints the OTP to the screen

#### 3. Generate QR Code (Bonus)
```bash
./ft_otp -qr key.hex
```
or:
```bash
ft_otp -qr key.hex
```
- Generates a QR code image (`ft_otp_qr.png`)
- Scan with Google Authenticator, Microsoft Authenticator, or Authy
- QR code contains TOTP URI with the secret key

### Graphical Interface (Bonus)

Launch the GUI:
```bash
python3 ft_otp_gui.py
```

Features:
- **Store Key Tab**: Browse and store hexadecimal keys
- **Generate OTP Tab**: Real-time OTP display with countdown timer
- **QR Code Tab**: Generate QR codes for mobile apps

### 4. Verify with oathtool
### 4. Verify with oathtool
```bash
oathtool --totp $(cat key.hex)
```
- This should give the same 6-digit code as your script (if run at the same time)

## Example Usage

```bash
# Create a test key
echo "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef" > key.hex

# Store the key
./ft_otp -g key.hex
# Output: Key was successfully saved in ft_otp.key.

# Generate OTP
./ft_otp -k ft_otp.key
# Output: 836492

# Wait 30 seconds and generate again
sleep 30
./ft_otp -k ft_otp.key
# Output: 123518 (different code)

# Generate QR code for mobile app
./ft_otp -qr key.hex
# Output: [+] QR code generated successfully: ft_otp_qr.png

# Launch GUI
python3 ft_otp_gui.py
```

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
├── ft_otp.py           # Main CLI implementation
├── ft_otp_gui.py       # GUI implementation (Bonus)
├── README.md           # This file
├── key.hex             # Your original hex key (not committed)
├── ft_otp.key          # Encrypted key file (generated)
└── ft_otp_qr.png       # QR code image (generated)
```

### Command Line Interface
```
$ ./ft_otp -g key.hex
Key was successfully saved in ft_otp.key.

$ ./ft_otp -k ft_otp.key
836492
```

### GUI Features
- Modern, user-friendly interface
- Three tabs: Store Key, Generate OTP, QR Code
- Real-time OTP updates with countdown timer
- File browser for easy key selection
- Visual feedback for all operations

### QR Code
- Compatible with all major authenticator apps
- Includes issuer and account information
- Standard TOTP URI format

## Notes
- Only use the original `key.hex` with oathtool, not the encrypted file.
- The script is compatible with standard TOTP tools.

## References
- [RFC 4226 - HOTP](https://datatracker.ietf.org/doc/html/rfc4226)
- [RFC 6238 - TOTP](https://datatracker.ietf.org/doc/html/rfc6238)
- [oathtool documentation](https://www.nongnu.org/oath-toolkit/)
