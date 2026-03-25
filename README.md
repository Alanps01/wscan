# 🔎 wscan – Advanced Web Vulnerability Scanner

**wscan** is a lightweight **CLI-based Web Vulnerability Scanner** built with Python.
It is designed for cybersecurity students, penetration testers, and bug bounty hunters who want to quickly identify common web vulnerabilities.

The scanner automatically crawls a target website, analyzes responses, and detects potential security issues such as **SQL Injection, XSS, and missing security headers**.

---

## 🚀 Features

✅ **Automated Website Crawling** – Discovers internal links within the target domain.

✅ **SQL Injection Detection** – Identifies potential SQL injection vulnerabilities.

✅ **Reflected XSS Detection** – Tests pages for reflected cross-site scripting.

✅ **Form Vulnerability Scanning** – Automatically analyzes input forms.

✅ **Security Header Analysis** – Detects missing security headers.

✅ **Clickjacking Detection** – Checks for missing `X-Frame-Options`.

✅ **Technology Fingerprinting** – Identifies server technologies.

✅ **Multithreaded Scanning** – Faster scans using concurrent threads.

✅ **HTML Report Generation** – Generates a readable vulnerability report.

✅ **JSON Export** – Optional structured vulnerability output.

---

## 🛠️ Dependencies

The following dependencies are required to run **wscan**:

* Python 3
* requests
* beautifulsoup4

These dependencies can be installed automatically using the **requirements.txt** file.

---

## 💻 Installation

Clone the repository:

```
git clone https://github.com/Alanps01/wscan.git
```

Move into the project directory:

```
cd wscan
```

Install required dependencies:

```
pip3 install -r requirements.txt
```

Make the scanner executable:

```
chmod +x wscan.py
```

Run the scanner:

```
python3 wscan.py -u http://example.com
```

---

## ⚡ Quick Installation (Recommended)

Use the installation script:

```
chmod +x install.sh
./install.sh
```

After installation you can run the tool globally:

```
wscan -u http://example.com
```

---

## 📝 Usage

Basic scan:

```
wscan -u http://example.com
```

Advanced scan with custom depth and threads:

```
wscan -u http://example.com --depth 3 --threads 10
```

Export JSON report:

```
wscan -u http://example.com -o report.json
```

---

## 📊 Example Scan

```
wscan -u http://testphp.vulnweb.com
```

Example output:

```
[+] Crawling: http://testphp.vulnweb.com
[!] Missing Security Header -> http://testphp.vulnweb.com
[!] Possible SQL Injection -> http://testphp.vulnweb.com/product?id=1
[!] Reflected XSS -> http://testphp.vulnweb.com/search?q=
```

---

## 📁 Output Files

After scanning, the following files may be generated:

```
report.html
report.json
```

Open the HTML report:

```
firefox report.html
```

---

## 📌 Project Structure

```
wscan/
│
├── wscan.py
├── install.sh
├── requirements.txt
├── README.md
└── report.html
```

---

## 🛡️ Disclaimer

This tool is created for **educational purposes and authorized security testing only**.

Do **not** scan systems without permission.
The author is **not responsible for misuse of this tool**.

---
