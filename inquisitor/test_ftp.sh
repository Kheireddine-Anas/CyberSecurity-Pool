#!/bin/bash

echo "============================================"
echo "FTP Test Script - Inquisitor Project"
echo "============================================"
echo ""

FTP_HOST="172.20.0.10"
FTP_USER="ftpuser"
FTP_PASS="ftppass"

echo "[1] Creating test files..."
echo "This is a test file for upload" > /tmp/upload_test.txt
echo "Another test file" > /tmp/document.pdf
echo "Secret data" > /tmp/backup.zip

echo "[2] Connecting to FTP server..."
echo ""

# Use lftp for automated FTP operations
lftp -u $FTP_USER,$FTP_PASS $FTP_HOST <<EOF
echo "Connected to FTP server"
pwd
ls

echo ""
echo "[3] Uploading files (watch for STOR commands)..."
put /tmp/upload_test.txt
put /tmp/document.pdf
put /tmp/backup.zip

echo ""
echo "[4] Listing files on server..."
ls

echo ""
echo "[5] Downloading files (watch for RETR commands)..."
get upload_test.txt -o /tmp/downloaded_test.txt
get document.pdf -o /tmp/downloaded_doc.pdf

echo ""
echo "[6] Test completed!"
quit
EOF

echo ""
echo "============================================"
echo "FTP operations completed!"
echo "============================================"
echo ""
echo "Check the inquisitor output for intercepted filenames:"
echo "  - STOR upload_test.txt"
echo "  - STOR document.pdf"
echo "  - STOR backup.zip"
echo "  - RETR upload_test.txt"
echo "  - RETR document.pdf"
echo ""
