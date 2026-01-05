# ft_onion - VM Configuration & Setup Guide

This guide explains how to configure a Debian 13 VM for the ft_onion project, with detailed explanations for every command and the bonus (SSH fortification).

---

## 1. Create and Configure Your VM
- Download Debian 13 ISO from the official site.
- Create a new VM in VirtualBox, VMware, or your preferred hypervisor.
- Assign at least 1GB RAM, 1 CPU, and 10GB disk.
- Attach the Debian ISO and install Debian (CLI mode is sufficient).
- Set up a user account and password.
- After installation, log in as your user.

---

## 2. Update Your System
```bash
sudo apt-get update && sudo apt-get upgrade -y
```
**Explanation:**
- `sudo apt-get update` refreshes the list of available packages and their versions.
- `sudo apt-get upgrade -y` upgrades all installed packages to the latest versions. The `-y` flag auto-confirms prompts.

---

## 3. Install Required Packages
```bash
sudo apt-get install -y tor nginx openssh-server
```
**Explanation:**
- `tor`: Installs the Tor service for anonymous networking and hidden services.
- `nginx`: Installs the Nginx web server to serve your static web page.
- `openssh-server`: Installs the SSH server for remote access.
- The `-y` flag auto-confirms installation prompts.

---

## 4. Create Your Static Web Page
```bash
sudo mkdir -p /var/www/html
```
**Explanation:**
- Creates the directory for your website if it doesn't exist.

```bash
sudo nano /var/www/html/index.html
```
**Explanation:**
- Opens a text editor to create your static web page. Add your HTML content, then save and exit (Ctrl+O, Enter, Ctrl+X in nano).

---

## 5. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/default
```
**Explanation:**
- Opens the Nginx default site config. Set `root` to `/var/www/html` and `index` to `index.html`.

Example server block:
```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html;
    server_name _;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

```bash
sudo systemctl restart nginx
```
**Explanation:**
- Restarts the Nginx service to apply your changes.

---

## 6. Configure SSH
```bash
sudo nano /etc/ssh/sshd_config
```
**Explanation:**
- Opens the SSH server config file. Change the following:
  - `Port 22` → `Port 4242` (required)

**Important: Add your SSH key before enabling SSH hardening!**
1. On your local machine, generate a key if you don't have one:
   ```bash
   ssh-keygen -t ed25519
   ```
2. Copy your public key to the VM (while password login is still enabled):
   ```bash
   ssh-copy-id -p 4242 youruser@your_vm_ip
   ```
   Or manually append your public key to `~/.ssh/authorized_keys` for your user on the VM.

**After your key is added and tested, you can proceed to the bonus (SSH fortification) step.**

```bash
sudo systemctl restart ssh
```
**Explanation:**
- Restarts the SSH service to apply your changes.

---

## 7. Configure Tor Hidden Service
```bash
sudo nano /etc/tor/torrc
```
**Explanation:**
- Opens the Tor configuration file. Add:
```
HiddenServiceDir /var/lib/tor/hidden_service/
HiddenServicePort 80 127.0.0.1:80
HiddenServicePort 4242 127.0.0.1:4242
```
- This sets up a hidden service that maps your .onion address to your Nginx (80) and SSH (4242) ports.

```bash
sudo systemctl restart tor
```
**Explanation:**
- Restarts the Tor service to apply your changes.

```bash
sudo cat /var/lib/tor/hidden_service/hostname
```
**Explanation:**
- Displays your generated .onion address. Use this in Tor Browser to access your site.

---

## 8. Test Your Setup
- Open Tor Browser on your host machine.
- Enter your .onion address to view your web page.
- SSH to your VM on port 4242:
  ```bash
  ssh -p 4242 youruser@your_vm_ip
  # (Or via Tor if required)
  ```
**Explanation:**
- This verifies your web and SSH services are accessible as required.

---

## 9. (Bonus) SSH Fortification (Hardening)
**What does "SSH fortification" mean?**

SSH fortification means making your SSH server as secure as possible. This is what the subject wants for the bonus. It includes:
- Disabling root login (`PermitRootLogin no`)
- Enforcing key-based authentication only (`PasswordAuthentication no`)
- Restricting which users can log in (`AllowUsers youruser`)
- (Optionally) Disabling unused authentication methods, rate limiting, and more

**How to do it:**
Edit `/etc/ssh/sshd_config` and set:
```
PermitRootLogin no
PasswordAuthentication no
AllowUsers youruser
```
Restart SSH:
```bash
sudo systemctl restart ssh
```
**Explanation:**
- These settings prevent brute-force attacks, unauthorized access, and enforce best practices for SSH security.

---

## 10. Submission Checklist
- [✅] `index.html`
- [✅] `nginx.conf` (or copy `/etc/nginx/sites-available/default` and rename it to `nginx.conf`)
- [✅] `sshd_config`
- [✅] `torrc`
- [✅] `README.md` (setup guide)

---

## Notes
- Do not open extra ports or set firewall rules.
- Only submit the required files in your repository.
- Bonus is only evaluated if the mandatory part is perfect.
