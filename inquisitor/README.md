# Inquisitor - ARP Poisoning & FTP Sniffer

Man-in-the-Middle attack tool that performs ARP poisoning and intercepts FTP traffic.

**⚠️ Educational purposes only. Use only in isolated lab environments.**

---

## Overview

This project demonstrates:
- **ARP Poisoning** (bidirectional/full duplex)
- **Traffic interception** using libpcap/scapy
- **FTP protocol analysis** and credential sniffing
- **Graceful cleanup** (ARP table restoration)

---

## Requirements

- **Docker** and **Docker Compose** installed
- **Make** utility
- Root/sudo privileges (for raw socket operations)

---

## Quick Start

### 1. Install Docker on Debian 13

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Install Docker Compose (standalone)
sudo apt install -y docker-compose

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Reboot or re-login for group changes to take effect
```

### 2. Build and Start the Environment

```bash
cd inquisitor

# Build Docker images and start containers
make build
make up
```

This will start 3 containers:
- **ftp_server** (172.20.0.10) - FTP server with user `ftpuser:ftppass`
- **client** (172.20.0.5) - FTP client
- **attacker** - Your inquisitor tool

---

## Usage

### Basic Attack (Show Filenames Only)

In one terminal, start the attack:

```bash
make attack
```

**Output:**
```
============================================================
INQUISITOR - ARP Poisoning & FTP Sniffer
============================================================
Source:     172.20.0.5 (02:42:ac:14:00:05)
Target:     172.20.0.10 (02:42:ac:14:00:0a)
Verbose:    False
============================================================
[+] IP forwarding enabled
[+] Starting packet sniffer...
[+] Starting ARP poisoning (Press CTRL+C to stop)...

[*] FTP: Uploading upload_test.txt
[*] FTP: Uploading document.pdf
[*] FTP: Downloading backup.zip
```

In another terminal, run the FTP test:

```bash
make test
```

**Press CTRL+C** to stop the attack. The program will automatically restore ARP tables.

---

### Verbose Mode (Show All FTP Traffic + Credentials)

```bash
make attack-verbose
```

**Output:**
```
[*] FTP: USER ftpuser
[!] FTP Username: ftpuser
[*] FTP: PASS ftppass
[!] FTP Password: ftppass
[*] FTP: PWD
[*] FTP: 257 "/home/vsftpd/ftpuser"
[*] FTP: TYPE I
[*] FTP: PASV
[*] FTP: STOR upload_test.txt
[*] FTP: Uploading upload_test.txt
```

---

## Manual Testing

### Option 1: Use Test Script

```bash
# Automated FTP test
make test
```

### Option 2: Manual FTP Commands

```bash
# Open shell in client container
make shell-client

# Install FTP client (if needed)
apk add lftp

# Connect to FTP server
lftp ftpuser:ftppass@172.20.0.10

# Upload a file
lftp> put /etc/hostname
# Your inquisitor will show: [*] FTP: Uploading hostname

# Download a file
lftp> get hostname
# Your inquisitor will show: [*] FTP: Downloading hostname

# Exit
lftp> quit
```

---

## Project Structure

```
inquisitor/
├── inquisitor              # Main Python script (ARP poisoning + sniffer)
├── Dockerfile              # Container image for attacker
├── docker-compose.yaml     # Multi-container setup
├── Makefile                # Automation commands
├── test_ftp.sh             # FTP test script
└── README.md               # This file
```

---

## How It Works

### 1. ARP Poisoning

The program sends fake ARP replies to both the client and server:

```
Client (172.20.0.5)          Server (172.20.0.10)
       ↓                              ↓
   "Server is at                "Client is at
    MY MAC address"              MY MAC address"
       ↓                              ↓
   All traffic flows through attacker (MITM)
```

### 2. Packet Forwarding

IP forwarding is enabled so traffic still reaches its destination:
```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

### 3. FTP Sniffing

Using scapy, the program captures TCP packets on port 21 (FTP control):
- **STOR filename** → File upload
- **RETR filename** → File download
- **USER/PASS** → Login credentials (verbose mode)

### 4. Cleanup

On CTRL+C:
1. Stop ARP poisoning loop
2. Send correct ARP replies (5 times each)
3. Disable IP forwarding
4. Exit gracefully

---

## Makefile Commands

| Command              | Description                          |
|----------------------|--------------------------------------|
| `make build`         | Build Docker images                  |
| `make up`            | Start all containers                 |
| `make down`          | Stop containers                      |
| `make clean`         | Remove containers and images         |
| `make attack`        | Run inquisitor (normal mode)         |
| `make attack-verbose`| Run inquisitor (verbose mode)        |
| `make test`          | Run automated FTP test               |
| `make logs`          | Show container logs                  |
| `make status`        | Show container/network status        |
| `make shell-attacker`| Open shell in attacker container     |
| `make shell-client`  | Open shell in client container       |
| `make shell-server`  | Open shell in FTP server             |

---

## Testing Checklist

### ✅ Mandatory Features

1. **ARP Poisoning (Bidirectional)**
   ```bash
   # Start attack
   make attack
   
   # In another terminal, check ARP tables
   docker exec client ip neigh
   docker exec ftp_server ip neigh
   
   # Both should show attacker's MAC for the other's IP
   ```

2. **FTP Filename Detection**
   ```bash
   # Start attack
   make attack
   
   # Run test (in another terminal)
   make test
   
   # Verify output shows:
   # [*] FTP: Uploading upload_test.txt
   # [*] FTP: Uploading document.pdf
   # [*] FTP: Downloading ...
   ```

3. **ARP Restoration**
   ```bash
   # Start attack
   make attack
   
   # Press CTRL+C
   
   # Verify output shows:
   # [!] CTRL+C detected, restoring ARP tables...
   # [+] ARP tables restored
   
   # Check ARP tables are correct
   docker exec client ip neigh
   ```

4. **Error Handling**
   ```bash
   # Test invalid IP
   ./inquisitor 999.999.999.999 aa:bb:cc:dd:ee:ff 1.1.1.1 11:22:33:44:55:66
   # Should show: Error: Invalid source IP address
   
   # Test invalid MAC
   ./inquisitor 1.1.1.1 INVALID 2.2.2.2 11:22:33:44:55:66
   # Should show: Error: Invalid source MAC address
   ```

### ✅ Bonus Feature

5. **Verbose Mode**
   ```bash
   # Start attack with -v flag
   make attack-verbose
   
   # Run test
   make test
   
   # Verify output shows ALL FTP commands:
   # [*] FTP: USER ftpuser
   # [!] FTP Username: ftpuser
   # [*] FTP: PASS ftppass
   # [!] FTP Password: ftppass
   # [*] FTP: PWD
   # [*] FTP: STOR filename
   ```

---

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"
```bash
# Start Docker service
sudo systemctl start docker

# Enable on boot
sudo systemctl enable docker
```

### Issue: "Permission denied" when running make
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Re-login or reboot
sudo reboot
```

### Issue: Containers not communicating
```bash
# Check network
docker network inspect inquisitor_test_network

# Restart containers
make down
make up
```

### Issue: ARP poisoning not working
```bash
# Check if running as privileged
docker inspect attacker | grep Privileged
# Should show: "Privileged": true

# Check IP forwarding
docker exec attacker cat /proc/sys/net/ipv4/ip_forward
# Should show: 1
```

---

## Security Notes

⚠️ **This tool is for educational purposes only.**

- **Use ONLY in isolated lab environments**
- **NEVER use on production networks**
- **NEVER use on networks you don't own/control**
- ARP poisoning is **illegal** on unauthorized networks
- This project is designed to teach defensive security concepts

---

## Technical Details

### Technologies Used
- **Python 3.11** - Main language
- **Scapy** - Packet manipulation and sniffing
- **Docker** - Isolated network environment
- **vsftpd** - FTP server for testing

### Protocol Details
- **ARP** - Layer 2 protocol (Ethernet)
- **FTP** - Port 21 (control), Port 20 (data)
- **TCP** - Transport layer

### Key Concepts Demonstrated
- Man-in-the-Middle (MITM) attacks
- ARP cache poisoning
- Packet sniffing with libpcap
- Protocol analysis
- Network reconnaissance

---

## Author

Made for the Cybersecurity Piscine at 1337 School

---

## License

Educational use only. Do not use for malicious purposes.
