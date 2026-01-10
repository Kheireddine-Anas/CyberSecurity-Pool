# Stockholm

Stockholm is an educational ransomware-like program developed for the Cybersecurity Piscine.
It demonstrates how ransomware encrypts and decrypts files, for defensive learning purposes only.

## Description

The program encrypts files inside a directory called `infection` located in the user's HOME directory.
It targets file extensions commonly affected by WannaCry ransomware and appends the `.ft` extension
to encrypted files.

The encryption uses **AES-256 in CBC mode**, a secure encryption algorithm.

⚠️ This project is strictly for educational purposes.

## Installation

Run the Makefile to install dependencies:

```bash
make
```

This will install the required Python library (`cryptography`) and make the script executable.

## Usage

```bash
./stockholm [-r] [-s] <key>
```

### Options

- `-h`, `--help`  
  Display help message.

- `-v`, `--version`  
  Display program version.

- `-r`, `--reverse`  
  Reverse the encryption (decrypt files).

- `-s`, `--silent`  
  Silent mode (no output).

### Key Requirements

- The key must be **at least 16 characters long**.
- The same key must be used to decrypt the files.

## Examples

Encrypt files:
```bash
./stockholm myverysecurekey123
```

Decrypt files:
```bash
./stockholm -r myverysecurekey123
```

Silent mode:
```bash
./stockholm -s myverysecurekey123
```

## Notes

- The program only works inside `~/infection`.
- Files already encrypted (`.ft`) are skipped.
- Errors are handled gracefully to avoid crashes.
- Ensure you have the necessary permissions to read/write files in the target directory.
- **Encryption**: Uses AES-256 CBC with random IV (prepended to ciphertext).
- The key is padded/truncated to 32 bytes for AES-256 compatibility.
