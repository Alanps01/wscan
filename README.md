# 🔎 wscan - Advanced Web Vulnerability Scanner

wscan is a lightweight CLI Web Vulnerability Scanner built with Python for cybersecurity students and beginners.

It detects common security issues such as:

• SQL Injection
• Reflected XSS
• Missing Security Headers
• Clickjacking
• Technology Disclosure
• Vulnerable forms

---

## Installation

Clone the repository from GitHub:

git clone https://github.com/Alanps01/wscan.git

Move into the project directory:

cd wscan

Run the installer:

chmod +x install.sh
./install.sh

---

## Usage

Basic scan:

wscan -u http://example.com

Advanced scan:

wscan -u http://example.com --depth 3 --threads 10

Save JSON report:

wscan -u http://example.com -o report.json

---

## Example

wscan -u http://testphp.vulnweb.com

---

## Output

The scanner generates:

• Console vulnerability results
• HTML report
• Optional JSON report

---

## Author

Alan
Cybersecurity Student
