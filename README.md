# 🚀 Gobuster Smart Scanner – All Options with Proxy Rotation

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gobuster 3.x](https://img.shields.io/badge/Gobuster-3.x-green)](https://github.com/OJ/gobuster)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux%20%7C%20Parrot%20%7C%20Ubuntu-lightgrey)](https://kali.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](http://makeapullrequest.com)

> **Automated Gobuster Scanner with 18 different test variants, intelligent proxy rotation, and rate‑limit handling**

---

## 📖 What is Gobuster Smart Scanner?

**Gobuster Smart Scanner** is a fully automated wrapper around the popular directory/file brute‑forcing tool **Gobuster**. It runs **18 pre‑configured test variants** (HTTPS/HTTP, with/without redirects, various thread counts, status‑code filtering, file extensions, verbose mode, etc.) to thoroughly enumerate a target web server. It intelligently handles:

- **Direct connectivity** – tests if the target is reachable without a proxy.
- **Proxy fallback** – if direct access fails or is rate‑limited, it automatically tests a large built‑in pool of proxies (or a user‑supplied list) and keeps only working ones.
- **Proxy rotation** – rotates proxies per test and immediately removes any proxy that triggers a **429 (Rate Limit)** or fails.
- **Wordlist management** – uses SecLists `common.txt` if available, otherwise downloads it automatically, and creates a fallback list if all else fails.
- **Colored terminal output** – differentiates status codes (200, 301, 302, 403, 429) with colours for quick analysis.
- **Detailed reporting** – generates per‑test output files and a comprehensive summary report with statistics, found entries, and status‑code breakdowns.

This tool is ideal for **penetration testers**, **bug bounty hunters**, and **system administrators** who need a comprehensive, hands‑off directory enumeration with minimal manual intervention.

---

## ✨ Features

- **18 Built‑in Test Variants** – covers HTTPS and HTTP with different flags:
  - Standard scan, redirect follow (`-r`), all status codes (no blacklist), verbose (`-v`), no file extensions, only `200` status, only `200/301/302`, slow (2 threads), fast (30 threads), and combined flags.
- **Smart Proxy Management**:
  - Built‑in list of ~300 proxies (HTTP, HTTPS, SOCKS4, SOCKS5) – shuffled and tested.
  - Parallel proxy testing with `ThreadPoolExecutor`.
  - Proxy rotation per test – round‑robin from the working pool.
  - Automatic removal of failed or rate‑limited proxies.
  - Supports custom proxy files (one per line).
- **Direct Connection Check** – first attempts a direct `curl` to the target before using proxies.
- **Automatic Wordlist Handling**:
  - Searches common paths: `/usr/share/seclists/Discovery/Web-Content/common.txt`, `/usr/share/wordlists/dirb/common.txt`, etc.
  - If not found, downloads SecLists via `git clone`.
  - Creates a small fallback wordlist if download fails.
- **Rate‑Limit Resilience** – detects `429` responses and immediately switches to a fresh proxy.
- **Colored Terminal Output** – status codes are colour‑coded:
  - `200` – Green (accessible)
  - `301/302` – Yellow (redirect)
  - `403` – Red (forbidden)
  - `429` – Red (rate limited)
- **Comprehensive Reporting**:
  - Each test saves its raw Gobuster output to a separate `.txt` file.
  - A summary report (`report.txt`) includes per‑test success/failure, time, entries found, status‑code distribution, and sample entries.
  - Total entries, success rate, proxy usage, and rate‑limit occurrences are displayed.
- **Thread‑Safe Proxy Pool** – uses `threading.Lock` to safely hand out proxies across concurrent tests.
- **Random Delays** – a small random delay (0.5–2 seconds) between tests to reduce detection.

---

## 🛠️ Installation

### Prerequisites

| Requirement | Description |
|-------------|-------------|
| **Python 3.6+** | The script uses Python’s standard library and the `requests` module. |
| **Gobuster** | The core tool – must be installed and in `PATH`. |
| **Proxychains4** | Required to route Gobuster through proxies. |
| **Curl** | Used for direct connection and proxy testing. |
| **Git** | Needed to clone SecLists if not present. |
| **requests (Python)** | Used for HTTP proxy verification. |

### Step 1: Install System Dependencies

For **Ubuntu / Debian / Kali Linux**:

```bash
sudo apt update
sudo apt install -y gobuster proxychains4 curl git python3 python3-pip
```

### Step 2: Install Python Dependencies

```bash
pip3 install requests --break-system-packages   # or just pip3 install requests
```

### Step 3: Clone the Repository

```bash
git clone https://github.com/your-username/gobuster-smart-scanner.git
cd gobuster-smart-scanner
```

### Step 4: Make the Script Executable (Optional)

```bash
chmod +x gobuster_smart_scanner.py
```

### Step 5: Verify Installation

```bash
python3 gobuster_smart_scanner.py --help
# or simply run it with a target
python3 gobuster_smart_scanner.py example.com
```

---

## 🚀 Usage

### Basic Usage (Automatic Proxy Discovery)

```bash
python3 gobuster_smart_scanner.py <target-domain>
```

Example:

```bash
python3 gobuster_smart_scanner.py example.com
```

If you don't provide a target as an argument, the script will prompt you:

```bash
python3 gobuster_smart_scanner.py
Enter target domain: example.com
Proxy file path (press Enter for default): 
```

### Using a Custom Proxy File

```bash
python3 gobuster_smart_scanner.py example.com my_proxies.txt
```

### Command‑Line Options

| Option | Description |
|--------|-------------|
| `target` | Target domain (e.g., example.com) – required as first argument. |
| `proxy_file` | (Optional) Path to a file containing proxies, one per line. If omitted, the built‑in list is used. |

### Proxy File Format

Each line must contain a full proxy URL in one of these formats:

```text
http://user:pass@host:port
https://host:port
socks4://host:port
socks5://host:port
```

Example `my_proxies.txt`:

```text
http://192.168.1.1:8080
socks5://10.0.0.1:1080
https://proxy.example.com:443
http://user:pass@47.89.184.18:3128
```

---

## 🖥️ Example Output

```text
╔═══════════════════════════════════════════════════════════════════╗
║     GOBUSTER SMART SCANNER - ALL OPTIONS                         ║
║     Fixed: -b "" to disable 404 blacklist                        ║
║     18 Complete Tests with Proxy Rotation                        ║
╚═══════════════════════════════════════════════════════════════════╝

🔍 Checking Gobuster installation...
✅ Gobuster is installed   Gobuster v3.1.0

📂 Finding wordlist...
✅ Wordlist found: /usr/share/seclists/Discovery/Web-Content/common.txt

🔍 Testing direct connection...
   ✅ Direct HTTPS: 200 - Working

🚀 SMART GOBUSTER SCAN - ALL OPTIONS
======================================================================
💡 Direct mode
💡 Fixed: -b "" (disabled 404 blacklist)
======================================================================

📝 Test 1/18: HTTPS - Standard Scan
   Common files and directories
▶️ HTTPS - Standard Scan
   🔓 Direct mode (no proxy)
   CMD: gobuster dir -u https://example.com -w /usr/share/seclists/... -t 15 ...
   ✅ Completed in 12.34s - Found 42 entries

📝 Test 2/18: HTTPS - With Redirect (-r)
   Follow redirects...

======================================================================
📊 SCAN SUMMARY
======================================================================
Total Tests: 18
✅ Successful: 16
❌ Failed: 2
📊 Total Entries Found: 342
🔄 Proxy Used: 0 tests
📋 Status Codes:
   • 200: 120 times (ACCESSIBLE)
   • 301: 45 times (REDIRECT)
   • 403: 12 times (FORBIDDEN)
   • 500: 2 times

📋 DETAILED RESULTS
======================================================================
[1] HTTPS - Standard Scan
   ✅ PASS | Mode: 🔓 Direct | Time: 12.34s | Found: 42 entries
   Sample entries:
   • admin
   • login
   • wp-admin
   • api
   • blog

[2] HTTPS - With Redirect (-r)
   ✅ PASS | Mode: 🔓 Direct | Time: 14.22s | Found: 38 entries
...

✅ Report saved: gobuster_scan_20260101_120000/report.txt
✅ Scan completed!
📁 Results saved in: gobuster_scan_20260101_120000
```

---

## ⚙️ How It Works (Flow Diagram)

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        START SCAN                                   │
│               User provides target domain                           │
│               and optional proxy file                               │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 1: ENVIRONMENT SETUP                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  1. Check if Gobuster is installed; if not, try `sudo apt  │    │
│  │     install gobuster -y`                                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  2. Find or download wordlist:                              │    │
│  │     - Check common paths (/usr/share/seclists/...)          │    │
│  │     - If not found, `git clone` SecLists                    │    │
│  │     - If that fails, create a fallback list                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  3. Load proxies (from file or built‑in list)               │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 2: CONNECTIVITY CHECK                            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Direct connection test (curl to target)                     │    │
│  │  - If success (200/301/302/403) → direct mode enabled       │    │
│  │  - If failure (429/timeout) → direct blocked → use proxies  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  If direct blocked: test all proxies in parallel:           │    │
│  │  - For each proxy, check if it can reach Google             │    │
│  │  - Then check if it can reach the target                    │    │
│  │  - Collect only working proxies into a pool                 │    │
│  │  - Remove dead/blocked proxies                               │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 3: RUN 18 GOBUSTER TESTS                         │
│                                                                     │
│  For each test (1..18):                                             │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  a) Choose mode: direct (if available) or proxy             │    │
│  │  b) If proxy: get next proxy from the pool (round‑robin)    │    │
│  │  c) Build the Gobuster command with specific flags:         │    │
│  │     - HTTPS/HTTP base                                       │    │
│  │     - Wordlist path                                         │    │
│  │     - Thread count (2, 15, or 30)                          │    │
│  │     - Status‑code filters (`-s` and `-b ""`)              │    │
│  │     - Extensions (`-x php,html,txt,...`)                   │    │
│  │     - Redirect (`-r`), verbose (`-v`)                      │    │
│  │     - Output file                                           │    │
│  │  d) Execute: if proxy, wrap with `proxychains4`            │    │
│  │  e) Capture and parse output (real‑time)                   │    │
│  │  f) Detect rate‑limiting (429) and mark proxy failed       │    │
│  │  g) Store results (entries, status codes, timing)         │    │
│  │  h) Random delay (0.5‑2s) before next test                │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PHASE 4: REPORTING                                     │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  - Display summary: total tests, successful/failed,         │    │
│  │    total entries, proxy usage, rate‑limit incidents,        │    │
│  │    status‑code breakdown                                     │    │
│  │  - Show detailed per‑test results (sample entries)          │    │
│  │  - Save comprehensive `report.txt`                          │    │
│  │  - Each Gobuster output saved as separate `.txt` file      │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SCAN COMPLETE                                 │
│            Results saved in timestamped directory                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Output Structure

After a scan, a directory named `gobuster_scan_YYYYMMDD_HHMMSS` is created. Its contents:

```text
gobuster_scan_20260101_120000/
├── report.txt                                    # Full summary report
├── fallback_wordlist.txt                         # (if created)
├── gobuster_https_standard.txt
├── gobuster_https_redirect.txt
├── gobuster_https_allstatus.txt
├── gobuster_https_verbose.txt
├── gobuster_https_noext.txt
├── gobuster_https_only200.txt
├── gobuster_https_200301302.txt
├── gobuster_https_slow.txt
├── gobuster_https_fast.txt
├── gobuster_https_redirect_verbose.txt
├── gobuster_http_standard.txt
├── gobuster_http_redirect.txt
├── gobuster_http_allstatus.txt
├── gobuster_http_verbose.txt
├── gobuster_http_noext.txt
├── gobuster_http_only200.txt
├── gobuster_http_slow.txt
└── gobuster_http_redirect_verbose.txt
```

### Description of Output Files

| File | Description |
|------|-------------|
| `report.txt` | Human‑readable summary: scan date, target, wordlist used, total tests, success/failure counts, total entries, status‑code distribution, and per‑test details (time, entries, sample URLs). |
| `fallback_wordlist.txt` | Created only if no system wordlist was found; contains a small set of common words. |
| `gobuster_*.txt` | Each file contains the raw output of the corresponding Gobuster test. Useful for manual inspection and parsing. |

---

## ⚙️ Configuration

### Proxy Management
The tool uses the `ProxyManager` class to handle proxies. It supports:
- **Built‑in proxy list** – ~300 proxies (HTTP/HTTPS/SOCKS) that are shuffled and tested.
- **Custom proxy file** – provide your own list via the second argument.
- **Parallel testing** – proxies are tested concurrently (default 20 workers) to find working ones quickly.
- **Proxy pool** – only working proxies (those that respond to the target) are kept in the pool.
- **Rotation** – proxies are used in a round‑robin fashion, with thread‑safe locking.

### Wordlist Configuration
The script searches for wordlists in the following order:
1. `/usr/share/seclists/Discovery/Web-Content/common.txt`
2. `/usr/share/wordlists/dirb/common.txt`
3. `/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`
4. `/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt`

If none exist, it attempts to clone the SecLists repository to `/usr/share/seclists`. If cloning fails, it creates a fallback list with 40 common words (`admin`, `login`, etc.).

### Adjustable Parameters
You can tweak the following inside the script:
- **Number of threads for proxy testing** – in `test_all_proxies(max_workers=20)`, change `max_workers`.
- **Delay between tests** – in `run_smart_scan()`, the `random.uniform(0.5, 2)` can be increased to reduce detection.
- **Gobuster thread counts** – the tests use `-t 15` (default), `-t 2`, and `-t 30`. You can modify the test definitions.
- **Extensions** – the tests use `-x php,html,txt,js,css,json`; you can change this list.

---

## 🧪 Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `gobuster: command not found` | Gobuster not installed. | Install with `sudo apt install gobuster -y`. |
| `proxychains4: command not found` | Proxychains not installed. | Install with `sudo apt install proxychains4 -y`. |
| `ModuleNotFoundError: No module named 'requests'` | Python requests missing. | Install with `pip3 install requests`. |
| Direct connection fails but proxies exist | Target may block direct IPs or is behind a CDN. | The tool will automatically switch to proxy mode. |
| No working proxies found | All proxies are dead or blocked. | Supply your own fresh proxies using a custom file. Free proxies often expire quickly. |
| Scan stuck on a test | Gobuster may hang due to network issues. | Kill the script (Ctrl+C) and restart. The script handles timeouts (120s per test). |
| Rate‑limited (429) persists | All proxies are being rate‑limited. | Increase the delay between tests, use premium proxies, or reduce thread count. |
| No results found | Wordlist may be too small or target has no exposed directories. | Use a larger wordlist (e.g., `directory-list-2.3-medium.txt`). Consider manual testing. |
| Permission denied when cloning SecLists | Insufficient permissions. | Run with `sudo` or clone to a user‑writable location and modify the `seclist_paths` list. |

### Debugging Tips
- **Check `report.txt`** – contains detailed per‑test information.
- **Examine individual `gobuster_*.txt` files** – see raw output for errors.
- **Run with a single test** – by commenting out unwanted tests in the `tests` list inside `run_smart_scan()`.
- **Increase verbosity** – set `verbose=True` in the script to print more debug info.

---

## 📦 Dependencies

### System Packages
- `gobuster` (>= 3.0)
- `proxychains4`
- `curl`
- `git`
- `python3`
- `python3-pip`

### Python Modules
- `requests` (for proxy testing)
- All other modules are from the standard library (`subprocess`, `threading`, `re`, `random`, `socket`, `time`, `datetime`, `concurrent.futures`)

### Installation Commands (Summary)

```bash
sudo apt update && sudo apt install -y gobuster proxychains4 curl git python3 python3-pip
pip3 install requests --break-system-packages
```

---

## 📜 License

This project is licensed under the MIT License – see the LICENSE file for details.

---

## ⚠️ Disclaimer

This tool is intended for educational and authorized testing purposes only.
Use it only on systems you own or have explicit written permission to test. Unauthorised scanning may violate laws and terms of service. The authors are not responsible for any misuse, damage, or legal consequences arising from the use of this software. Always comply with applicable laws and regulations.

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

### Contribution Ideas
- Add more test variants (e.g., with cookies, user‑agent spoofing).
- Improve proxy testing (use more robust checks).
- Support additional output formats (JSON, CSV).
- Implement CMS detection and tailored wordlists.
- Add multi‑target scanning.

Please ensure your code follows the existing style and includes appropriate comments. For major changes, open an issue first to discuss.

---

## 📚 Resources

### Gobuster Documentation
- [Official Gobuster GitHub](https://github.com/OJ/gobuster)
- Gobuster Usage Examples

### Proxy Sources
- Free Proxy List
- SSL Proxies
- SOCKS Proxy List
- ProxyScrape

### Wordlist Sources
- SecLists
- DirBuster Lists

---

## 👨‍💻 Author

Your Name  
GitHub: [@yourusername](https://github.com/)  
Twitter: [@yourtwitter](https://twitter.com/)  

---

## 🙏 Acknowledgments

- **Gobuster Developers** – for the excellent directory brute‑force tool.
- **SecLists Project** – for the comprehensive wordlists.
- **Security Community** – for testing and feedback.

---

## 📌 Final Notes

### Quick Start Summary

```bash
# 1. Install dependencies
sudo apt update && sudo apt install -y gobuster proxychains4 curl git python3 python3-pip
pip3 install requests

# 2. Clone repo
git clone https://github.com/your-username/gobuster-smart-scanner.git
cd gobuster-smart-scanner

# 3. Run (auto proxies)
python3 gobuster_smart_scanner.py example.com

# 4. Or with your own proxies
python3 gobuster_smart_scanner.py example.com my_proxies.txt

# 5. Check results
cat gobuster_scan_*/report.txt
```

### Pro Tips
- **Use reliable proxies** – free proxies are often slow and get blocked quickly; consider using premium services.
- **Adjust delays** – if you keep hitting rate limits, increase the delay between tests (edit `random.uniform(0.5, 2)`).
- **Monitor progress** – watch the coloured output for early signs of blocking.
- **Combine with other tools** – use the discovered directories as input for further testing (e.g., with ffuf, nikto, or manual inspection).
- **Keep wordlists updated** – regularly update SecLists for the latest common paths.

Made with ❤️ for the Security Community
