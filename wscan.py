#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import threading
from queue import Queue
import json
import time

# ===================== BANNER =====================

def show_banner():
    banner = r"""
██╗    ██╗███████╗ ██████╗ █████╗ ███╗   ██╗
██║    ██║██╔════╝██╔════╝██╔══██╗████╗  ██║
██║ █╗ ██║███████╗██║     ███████║██╔██╗ ██║
██║███╗██║╚════██║██║     ██╔══██║██║╚██╗██║
╚███╔███╔╝███████║╚██████╗██║  ██║██║ ╚████║
 ╚══╝╚══╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝

              wscan
      Advanced Web Vulnerability Scanner
            Author: Alan
"""
    print(banner)

# ===================== ARGUMENTS =====================

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=True, help="Target URL")
parser.add_argument("--depth", type=int, default=2)
parser.add_argument("--threads", type=int, default=5)
parser.add_argument("-o", "--output", help="Save JSON report")
args = parser.parse_args()

target = args.url
domain = urlparse(target).netloc

visited = set()
queue = Queue()
vulnerabilities = []
lock = threading.Lock()

# ===================== HEADER CHECK =====================

def check_headers(url):
    try:
        r = requests.get(url, timeout=5)
        headers = r.headers

        required = [
            "X-Frame-Options",
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Content-Type-Options"
        ]

        for h in required:
            if h not in headers:
                vulnerabilities.append({
                    "type": "Missing Security Header",
                    "url": url,
                    "detail": h
                })

        # Clickjacking
        if "X-Frame-Options" not in headers:
            vulnerabilities.append({
                "type": "Possible Clickjacking",
                "url": url
            })

        # Technology fingerprint
        if "Server" in headers:
            vulnerabilities.append({
                "type": "Technology Disclosure",
                "url": url,
                "detail": headers["Server"]
            })

    except:
        pass

# ===================== SQLi CHECK =====================

def test_sqli(url):
    payload = "'"
    try:
        normal = requests.get(url, timeout=5)
        injected = requests.get(url + payload, timeout=5)

        if abs(len(normal.text) - len(injected.text)) > 50:
            vulnerabilities.append({
                "type": "Possible SQL Injection",
                "url": url,
                "payload": payload
            })
    except:
        pass

# ===================== XSS CHECK =====================

def test_xss(url):
    payload = "<script>alert(1)</script>"
    try:
        r = requests.get(url + payload, timeout=5)
        if payload in r.text:
            vulnerabilities.append({
                "type": "Reflected XSS",
                "url": url,
                "payload": payload
            })
    except:
        pass

# ===================== FORM TEST =====================

def scan_forms(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        forms = soup.find_all("form")

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            form_url = urljoin(url, action)

            inputs = form.find_all("input")
            data = {}

            for inp in inputs:
                name = inp.get("name")
                if name:
                    data[name] = "' OR '1'='1"

            if method == "post":
                res = requests.post(form_url, data=data)
            else:
                res = requests.get(form_url, params=data)

            if "sql" in res.text.lower():
                vulnerabilities.append({
                    "type": "SQL Injection (Form)",
                    "url": form_url
                })

    except:
        pass

# ===================== CRAWLER =====================

def worker():
    while not queue.empty():
        url, depth = queue.get()

        if url in visited or depth == 0:
            queue.task_done()
            continue

        with lock:
            visited.add(url)

        print(f"[+] Crawling: {url}")

        check_headers(url)
        test_sqli(url)
        test_xss(url)
        scan_forms(url)

        try:
            r = requests.get(url, timeout=5)
            soup = BeautifulSoup(r.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if domain in urlparse(full_url).netloc:
                    queue.put((full_url, depth - 1))

        except:
            pass

        queue.task_done()

# ===================== HTML REPORT =====================

def generate_html():
    html = "<html><head><title>wscan Report</title></head><body>"
    html += "<h1>wscan Vulnerability Report</h1><ul>"

    for v in vulnerabilities:
        html += f"<li><b>{v['type']}</b> - {v['url']}</li>"

    html += "</ul></body></html>"

    with open("report.html", "w") as f:
        f.write(html)

# ===================== MAIN =====================

show_banner()
start = time.time()

queue.put((target, args.depth))

for _ in range(args.threads):
    t = threading.Thread(target=worker)
    t.start()

queue.join()

print("\nScan Completed.\n")

if vulnerabilities:
    for v in vulnerabilities:
        print(f"[!] {v['type']} -> {v['url']}")
else:
    print("No obvious vulnerabilities found.")

generate_html()
print("\nHTML report saved as report.html")

if args.output:
    with open(args.output, "w") as f:
        json.dump(vulnerabilities, f, indent=4)
    print(f"JSON report saved as {args.output}")

print(f"\nTime Taken: {round(time.time() - start, 2)} seconds")
