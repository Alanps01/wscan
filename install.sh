#!/bin/bash

echo "[+] Installing wscan dependencies..."

pip3 install -r requirements.txt

echo "[+] Making wscan executable..."

chmod +x wscan.py

sudo ln -s $(pwd)/wscan.py /usr/local/bin/wscan

echo "[✓] Installation completed"
echo "Run scanner using: wscan -u http://target.com"
