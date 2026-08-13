#!/usr/bin/env python3
"""
Gobuster Smart Scanner - Fixed Version with All Options
"""

import subprocess
import os
import sys
import time
import re
import random
import socket
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ProxyManager:
    """Manage proxy testing and rotation"""
    
    def __init__(self, proxy_file=None):
        self.all_proxies = []
        self.working_proxies = []
        self.failed_proxies = set()
        self.current_index = 0
        self.lock = threading.Lock()
        self.load_proxies(proxy_file)
        
    def load_proxies(self, proxy_file=None):
        """Load proxies from file or use default list"""
        default_proxies = [
            "http://47.85.161.37:3128",
            "http://103.209.36.58:8080",
            "http://192.232.48.28:8181",
            "http://15.235.21.254:8080",
            "http://8.209.255.13:3128",
            "http://152.42.167.241:3128",
            "socks4://109.123.251.109:1080",
            "http://103.3.59.208:8080",
            "http://172.110.220.36:3128",
            "http://43.99.100.108:3128",
            "http://95.211.64.139:8887",
            "http://95.211.64.139:8888",
            "http://95.211.64.139:8889",
            "https://176.111.37.5:39811",
            "http://176.111.37.216:39811",
            "https://204.76.203.9:3128",
            "http://1.231.81.166:3128",
            "socks4://178.130.47.21:1082",
            "http://180.191.234.166:8080",
            "socks4://199.116.114.11:4145",
            "http://103.112.69.87:3128",
            "http://163.181.207.170:9999",
            "socks4://68.71.251.134:4145",
            "http://138.122.140.194:3128",
            "socks4://192.111.139.162:4145",
            "https://165.154.7.156:8888",
            "socks4://107.152.98.5:4145",
            "socks4://192.252.211.193:4145",
            "socks4://192.252.216.81:4145",
            "http://42.96.18.62:1311",
            "https://86.62.2.25:3128",
            "http://34.43.46.91:80",
            "https://121.101.134.181:8080",
            "http://34.43.46.91:443",
            "socks4://68.71.249.158:4145",
            "https://47.81.56.193:8888",
            "socks4://199.102.106.94:4145",
            "socks4://192.252.209.155:14455",
            "socks4://68.71.247.130:4145",
            "socks5://194.163.174.78:1089",
            "socks4://192.252.208.70:14282",
            "socks4://142.54.236.97:4145",
            "socks4://142.54.237.34:4145",
            "socks5://43.164.3.124:1080",
            "socks4://192.252.208.67:14287",
            "socks5://45.144.54.40:1080",
            "socks4://198.8.94.174:39078",
            "socks4://199.58.184.97:4145",
            "socks4://67.201.59.70:4145",
            "socks4://192.111.130.2:4145",
            "socks4://184.178.172.28:15294",
            "socks4://184.170.251.30:11288",
            "socks4://107.181.161.81:4145",
            "socks4://142.54.228.193:4145",
            "socks4://98.182.147.97:4145",
            "socks4://68.71.242.118:4145",
            "http://45.144.53.63:5000",
            "socks4://142.54.235.9:4145",
            "socks4://192.252.209.158:4145",
            "socks4://68.71.252.38:4145",
            "https://103.237.102.191:11111",
            "socks4://98.191.0.47:4145",
            "socks5://31.76.80.215:1080",
            "socks4://72.195.34.58:4145",
            "socks4://72.195.34.41:4145",
            "socks4://192.111.129.145:16894",
            "socks4://24.249.199.4:4145",
            "socks4://72.195.34.60:27391",
            "socks4://72.207.33.64:4145",
            "socks4://184.181.217.210:4145",
            "socks4://72.195.101.99:4145",
            "https://113.160.132.26:8080",
            "socks4://98.175.31.195:4145",
            "http://95.3.69.222:8080",
            "socks4://98.188.47.150:4145",
            "socks4://72.207.109.5:4145",
            "https://34.101.184.164:3128",
            "socks4://184.178.172.5:15303",
            "socks4://174.75.211.222:4145",
            "socks4://98.188.47.132:4145",
            "socks4://184.181.178.33:4145",
            "socks4://98.175.31.195:4145",
            "socks4://98.191.0.37:4145",
            "socks4://72.214.108.67:4145",
            "socks4://184.178.172.23:4145",
            "socks4://70.166.167.38:57728",
            "socks4://72.195.34.59:4145",
            "socks4://184.178.172.18:15280",
            "socks4://98.175.31.222:4145",
            "socks4://68.1.210.163:4145",
            "socks4://24.249.199.12:4145",
            "http://175.136.239.173:8181",
            "socks4://68.71.240.210:4145",
            "socks4://184.182.240.211:4145",
            "socks4://184.181.217.206:4145",
            "socks4://68.71.254.6:4145",
            "socks4://72.206.74.126:4145",
            "socks5://103.6.235.13:5555",
            "http://103.132.52.20:8080",
            "socks4://184.178.172.25:15291",
            "socks5://38.175.197.50:5555",
            "socks4://192.252.215.2:4145",
            "https://103.227.210.164:3128",
            "socks5://93.123.118.15:1080",
            "socks4://68.71.249.153:48606",
            "http://45.144.53.63:5001",
            "https://144.31.75.120:11112",
            "https://140.238.32.108:3128",
            "socks5://161.35.90.93:1083",
            "socks5://123.58.219.171:10808",
            "https://147.45.166.120:3333",
            "https://38.19.36.86:999",
            "socks5://144.124.232.204:1080",
            "https://34.94.46.8:80",
            "http://45.155.226.177:3128",
            "https://157.230.178.216:8080",
            "https://64.112.184.210:3128",
            "https://212.58.132.5:8888",
            "socks5://185.209.29.226:1080",
            "socks4://72.49.49.11:31034",
            "http://103.169.53.145:8080",
            "socks5://144.91.111.48:1088",
            "socks4://216.68.128.121:4145",
            "socks4://199.58.185.9:4145",
            "socks5://101.36.104.46:10808",
            "https://38.76.9.0:999",
            "socks5://144.91.121.61:1088",
            "socks4://66.42.224.229:41679",
            "http://38.75.81.174:999",
            "socks5://69.55.49.177:38182",
            "socks4://103.88.234.239:40001",
            "socks5://213.199.47.140:1080",
            "http://185.200.188.234:10001",
            "socks4://67.201.58.190:4145",
            "http://2.78.60.10:3129",
            "http://186.5.94.206:999",
            "socks4://37.18.73.60:5566",
            "socks4://185.171.83.65:49153",
            "socks5://103.243.82.38:8008",
            "socks4://152.70.237.238:3128",
            "http://223.25.110.76:3125",
            "http://181.39.25.196:8118",
            "http://206.206.103.117:8888",
            "https://110.49.66.210:8080",
            "https://37.59.125.131:8888",
            "socks5://20.83.154.79:7070",
            "socks4://67.201.33.10:25283",
            "socks5://79.76.59.115:1080",
            "http://190.2.214.148:999",
            "socks4://192.252.220.89:4145",
            "http://103.171.240.150:8090",
            "http://177.234.217.238:999",
            "http://176.88.166.174:8080",
            "socks4://206.220.175.2:4145",
            "http://124.107.39.186:8082",
            "https://202.83.174.147:443",
            "socks5://27.124.43.203:1080",
            "http://103.179.252.225:3128",
            "socks4://142.54.232.6:4145",
            "socks5://194.163.174.78:1087",
            "socks5://152.89.104.11:1080",
            "socks4://174.77.111.197:4145",
            "socks4://184.181.217.213:4145",
            "socks4://45.137.43.0:1081",
            "socks4://199.102.105.242:4145",
            "https://43.153.82.179:8888",
            "http://41.220.138.121:8080",
            "socks5://45.133.16.88:1080",
            "socks4://184.182.240.12:4145",
            "https://134.122.199.224:10001",
            "https://45.232.0.2:8080",
            "http://187.251.224.167:80",
            "https://103.227.187.11:6090",
            "http://95.85.233.144:18443",
            "https://170.83.242.77:999",
            "socks5://195.133.65.238:10909",
            "https://148.244.254.67:999",
            "https://103.247.23.76:8081",
            "socks4://98.181.137.83:4145",
            "https://103.175.84.2:80",
            "https://45.43.60.220:8080",
            "http://154.18.239.181:8085",
            "socks4://192.9.171.168:1080",
            "https://170.245.132.81:999",
            "http://169.58.85.194:8080",
            "http://175.136.239.174:8181",
            "https://177.224.225.7:3128",
            "https://177.234.236.134:8080",
            "http://103.238.232.138:8080",
            "socks5://216.22.13.244:1083",
            "https://43.133.128.153:16012",
            "https://45.71.114.185:999",
            "socks5://109.172.55.210:1082",
            "socks5://5.255.113.177:1080",
            "https://213.6.249.37:19000",
            "https://185.138.114.111:8080",
            "https://110.76.145.118:1111",
            "socks5://43.134.58.45:1080",
            "https://163.223.150.82:8080",
            "http://159.195.49.27:8888",
            "https://103.161.69.252:2698",
            "socks5://66.163.127.204:10006",
            "http://89.43.135.9:8080",
            "socks4://104.37.135.145:4145",
            "http://119.93.153.10:8087",
            "https://45.71.186.214:999",
            "http://45.229.30.29:11211",
            "http://154.58.138.227:8080",
            "socks4://78.159.131.108:1082",
            "https://43.160.255.142:7890",
            "socks4://147.45.60.250:1082",
            "socks4://79.137.196.250:1080",
            "https://201.71.24.65:8082",
            "socks5://38.76.215.92:1080",
            "socks4://142.54.226.214:4145",
            "https://185.144.60.130:8095",
            "https://103.163.134.99:1111",
            "http://195.19.217.200:3128",
            "http://45.172.218.67:3028",
            "https://110.76.144.83:8080",
            "http://2.56.178.88:808",
            "socks5://129.151.9.55:10808",
            "https://103.156.96.238:8088",
            "socks5://223.25.110.37:8199",
            "http://103.144.246.2:8889",
            "socks5://159.195.49.27:1080",
            "socks4://184.185.2.12:4145",
            "socks4://98.181.137.80:4145",
            "http://193.43.159.167:8080",
            "https://103.173.163.193:8818",
            "https://118.100.26.71:8080",
            "socks5://195.19.48.214:1080",
            "https://103.169.132.70:8080",
            "http://38.188.101.89:999",
            "https://165.154.162.73:8888",
            "https://103.134.220.122:1080",
            "https://49.151.177.175:8082",
            "http://186.250.29.230:8080",
            "https://103.193.144.81:8080",
            "https://103.193.145.155:8080",
            "https://38.121.212.98:999",
            "http://103.189.97.38:1080",
            "socks5://195.19.50.226:1080",
            "http://45.180.140.241:8080",
            "http://103.106.112.166:1234",
            "http://36.50.56.146:8080",
            "http://85.234.100.149:8080",
            "https://181.66.251.76:999",
            "http://5.104.75.62:12000",
            "socks5://92.118.234.124:1080",
            "https://103.117.108.59:8080",
            "http://45.133.251.223:3128",
            "socks5://159.195.61.240:1080",
            "http://151.115.99.193:10006",
            "https://163.61.112.244:8080",
            "https://187.49.176.141:8080",
            "http://51.159.97.242:10006",
            "http://49.151.126.22:8082",
            "https://116.254.118.180:80",
            "http://103.163.80.56:8080",
            "https://160.19.18.209:8080",
            "https://49.149.116.93:8082",
            "http://85.158.145.47:8080",
            "socks4://49.51.178.87:9050",
            "https://38.194.246.34:999",
            "http://203.2.151.13:8080",
            "socks4://144.124.227.88:3129",
            "http://157.20.239.237:9090",
            "https://43.155.138.148:3128",
            "socks5://144.22.165.206:1088",
            "http://216.106.179.216:49497",
            "socks5://161.35.90.93:1082",
            "http://38.158.83.241:999",
            "socks4://70.166.167.55:57745",
            "https://5.161.50.82:8118",
            "socks5://152.69.167.87:1080",
            "http://103.85.183.30:4995",
            "https://37.187.109.70:10111",
            "https://141.136.13.51:8080",
            "socks5://5.35.85.97:1080",
            "https://212.252.71.20:8080",
            "https://187.251.224.167:8081",
            "https://201.20.42.46:3127",
            "https://45.230.47.150:8080",
            "http://160.250.222.1:8090",
            "https://173.212.245.136:8888",
            "https://188.132.221.105:8080",
            "socks5://144.24.47.42:1080",
            "socks5://178.128.82.131:10808",
            "https://8.219.97.248:80",
            "socks4://47.251.127.154:1080",
            "https://139.28.49.111:8080",
            "https://174.137.134.182:2999",
            "https://38.156.246.129:999",
            "https://103.173.162.227:8818",
            "https://88.210.11.216:8989",
            "https://103.114.52.130:8080",
            "http://149.40.26.240:8080",
            "socks5://193.122.105.251:65535",
            "http://102.204.14.2:8080",
            "http://178.18.207.85:8888",
            "http://181.192.2.23:8080",
            "https://186.31.135.201:999",
            "https://50.200.166.130:8080",
            "socks5://66.163.118.99:10006",
            "https://38.44.17.142:999",
            "http://103.165.155.196:8080",
            "https://103.185.43.242:8080",
            "https://38.51.243.121:999",
            "https://109.94.1.23:4050",
            "http://181.13.221.155:999",
            "https://103.153.62.245:8181",
            "https://187.190.114.40:999",
            "https://164.163.73.69:999",
            "http://131.222.253.124:8080",
            "socks4://135.225.91.78:9072",
            "https://49.151.233.115:8082",
            "https://181.78.75.84:8080",
            "https://45.149.93.219:8080",
            "https://190.60.37.145:999",
            "http://38.7.206.186:999",
            "https://5.165.225.172:3128",
            "https://190.111.218.142:999",
            "http://103.242.104.191:8080",
            "https://164.52.11.194:18080",
            "https://179.1.113.129:999",
            "socks5://66.163.119.55:10006",
            "http://159.194.228.40:8888",
            "https://92.63.225.173:3128",
            "https://162.214.159.94:3128",
            "http://148.251.86.76:16379",
            "socks4://43.162.90.69:1080",
            "https://213.176.113.24:50001",
            "socks5://89.106.89.70:10808",
            "socks5://47.85.9.228:10800",
            "https://123.0.19.210:10000"
        ]
        
        if proxy_file and os.path.exists(proxy_file):
            try:
                with open(proxy_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.all_proxies.append(line)
                print(f"{Colors.GREEN}✅ Loaded {len(self.all_proxies)} proxies from {proxy_file}{Colors.RESET}")
                return
            except:
                pass
        
        self.all_proxies = default_proxies
        random.shuffle(self.all_proxies)
        print(f"{Colors.CYAN}📋 Loaded {len(self.all_proxies)} default proxies{Colors.RESET}")

    def test_single_proxy(self, proxy):
        """Test a single proxy"""
        test_url = "http://httpbin.org/ip"
        try:
            if proxy.startswith('socks5://') or proxy.startswith('socks4://'):
                cmd = f"curl -s --socks5 {proxy.replace('socks5://', '').replace('socks4://', '')} --max-time 10 {test_url}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
                if result.returncode == 0 and result.stdout:
                    return proxy, True
            else:
                import requests
                proxies = {'http': proxy, 'https': proxy}
                response = requests.get(test_url, proxies=proxies, timeout=10, verify=False)
                if response.status_code == 200:
                    return proxy, True
        except:
            pass
        return proxy, False

    def test_all_proxies(self, max_workers=20):
        """Test all proxies in parallel"""
        print(f"\n{Colors.CYAN}🔍 Testing {len(self.all_proxies)} proxies...{Colors.RESET}")
        print(f"{Colors.YELLOW}{'─'*50}{Colors.RESET}")
        
        working = []
        tested = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.test_single_proxy, proxy): proxy for proxy in self.all_proxies}
            
            for future in as_completed(futures):
                proxy, is_working = future.result()
                tested += 1
                
                if is_working:
                    working.append(proxy)
                    print(f"{Colors.GREEN}   ✅ [{tested}/{len(self.all_proxies)}] Working: {proxy[:40]}...{Colors.RESET}")
                else:
                    if tested % 5 == 0:
                        print(f"{Colors.YELLOW}   ⏳ Tested {tested}/{len(self.all_proxies)} proxies...{Colors.RESET}")
        
        self.working_proxies = working
        random.shuffle(self.working_proxies)
        
        print(f"\n{Colors.MAGENTA}{'─'*50}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Working proxies: {len(self.working_proxies)}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed proxies: {len(self.all_proxies) - len(self.working_proxies)}{Colors.RESET}")
        
        if self.working_proxies:
            print(f"\n{Colors.GREEN}📋 Sample working proxies:{Colors.RESET}")
            for p in self.working_proxies[:5]:
                print(f"{Colors.BLUE}   • {p[:50]}...{Colors.RESET}")
        
        return self.working_proxies

    def get_proxy(self):
        """Get next working proxy"""
        with self.lock:
            if not self.working_proxies:
                return None
            
            proxy = self.working_proxies[self.current_index % len(self.working_proxies)]
            self.current_index += 1
            return proxy

    def mark_failed(self, proxy):
        """Mark a proxy as failed"""
        with self.lock:
            if proxy in self.working_proxies:
                self.working_proxies.remove(proxy)
                self.failed_proxies.add(proxy)
                print(f"{Colors.YELLOW}   ⚠️ Proxy failed, removed from pool: {proxy[:40]}...{Colors.RESET}")

class GobusterSmartScanner:
    def __init__(self, target, proxy_file=None):
        self.target = target
        self.clean_target = self.clean_url(target)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"gobuster_scan_{self.timestamp}"
        os.makedirs(self.results_dir, exist_ok=True)
        self.test_results = []
        self.wordlist_path = None
        self.proxy_manager = ProxyManager(proxy_file)
        self.use_proxy = False
        self.direct_blocked = False
        
    def clean_url(self, url):
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'^www\.', '', url)
        url = url.split('/')[0]
        return url

    def print_header(self, text):
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}{text}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{'='*70}{Colors.RESET}")

    def check_gobuster(self):
        """Check if Gobuster is installed"""
        print(f"\n{Colors.CYAN}🔍 Checking Gobuster installation...{Colors.RESET}")
        try:
            result = subprocess.run(['gobuster', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0] if result.stdout else 'Unknown'
                print(f"{Colors.GREEN}✅ Gobuster is installed{Colors.RESET}")
                print(f"{Colors.BLUE}   {version}{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}❌ Gobuster not found{Colors.RESET}")
                return False
        except FileNotFoundError:
            print(f"{Colors.RED}❌ Gobuster not found. Installing...{Colors.RESET}")
            subprocess.run("sudo apt update -y", shell=True)
            subprocess.run("sudo apt install gobuster -y", shell=True)
            return self.check_gobuster()

    def download_wordlist(self):
        """Download SecLists and find wordlist"""
        print(f"\n{Colors.CYAN}📂 Finding wordlist...{Colors.RESET}")
        
        seclist_paths = [
            "/usr/share/seclists/Discovery/Web-Content/common.txt",
            "/usr/share/wordlists/dirb/common.txt",
            "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
            "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt"
        ]
        
        for wl in seclist_paths:
            if os.path.exists(wl):
                print(f"{Colors.GREEN}✅ Wordlist found: {wl}{Colors.RESET}")
                self.wordlist_path = wl
                return wl
        
        print(f"{Colors.YELLOW}⚠️ SecLists not found. Downloading...{Colors.RESET}")
        
        try:
            seclist_dir = "/usr/share/seclists"
            if os.path.exists(seclist_dir):
                subprocess.run(f"sudo rm -rf {seclist_dir}", shell=True)
            
            print(f"{Colors.BLUE}   Downloading SecLists...{Colors.RESET}")
            cmd = f"sudo git clone --depth 1 https://github.com/danielmiessler/SecLists.git {seclist_dir}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✅ SecLists downloaded{Colors.RESET}")
                wordlist = "/usr/share/seclists/Discovery/Web-Content/common.txt"
                if os.path.exists(wordlist):
                    self.wordlist_path = wordlist
                    return wordlist
        except:
            pass
        
        return self.create_fallback_wordlist()

    def create_fallback_wordlist(self):
        """Create fallback wordlist"""
        print(f"{Colors.CYAN}📝 Creating fallback wordlist...{Colors.RESET}")
        
        wordlist_file = f"{self.results_dir}/fallback_wordlist.txt"
        
        words = [
            "admin", "login", "test", "dev", "api", "blog", "shop",
            "wp-admin", "wp-login", "wp-content", "wp-includes",
            "images", "css", "js", "assets", "static",
            "uploads", "downloads", "files", "media",
            "backup", "old", "new", "tmp", "temp", "cache",
            "cgi-bin", "phpmyadmin", "mysql", "database",
            "config", "configuration", "settings", "conf",
            "xmlrpc", "feed", "sitemap", "robots"
        ]
        
        with open(wordlist_file, 'w') as f:
            for word in words:
                f.write(f"{word}\n")
        
        print(f"{Colors.GREEN}✅ Created fallback wordlist: {wordlist_file}{Colors.RESET}")
        self.wordlist_path = wordlist_file
        return wordlist_file

    def check_direct_connection(self):
        """Check if direct connection works"""
        print(f"\n{Colors.CYAN}🔍 Testing direct connection...{Colors.RESET}")
        
        try:
            cmd = f"curl -s -o /dev/null -w '%{{http_code}}' https://{self.clean_target} --max-time 10 -k"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            status = result.stdout.strip()
            
            if status in ['200', '301', '302', '403']:
                print(f"{Colors.GREEN}   ✅ Direct HTTPS: {status} - Working{Colors.RESET}")
                return True
            elif status == '429':
                print(f"{Colors.RED}   ⚠️ Direct HTTPS: {status} - RATE LIMITED!{Colors.RESET}")
                self.direct_blocked = True
                return False
            else:
                print(f"{Colors.YELLOW}   ⚠️ Direct HTTPS: {status} - Not working{Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.YELLOW}   ⚠️ Direct connection failed: {str(e)[:30]}{Colors.RESET}")
            return False

    def run_gobuster_scan(self, test_name, cmd, use_proxy=False, proxy=None):
        """Run Gobuster scan with or without proxy"""
        print(f"\n{Colors.CYAN}▶️ {test_name}{Colors.RESET}")
        if use_proxy and proxy:
            print(f"{Colors.YELLOW}   🔄 Using proxy: {proxy[:40]}...{Colors.RESET}")
            full_cmd = f"proxychains4 {cmd}"
        else:
            print(f"{Colors.GREEN}   🔓 Direct mode (no proxy){Colors.RESET}")
            full_cmd = cmd
        
        print(f"{Colors.YELLOW}   CMD: {full_cmd[:120]}...{Colors.RESET}")
        
        try:
            start_time = time.time()
            
            process = subprocess.Popen(
                full_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            found_entries = []
            status_codes = {}
            rate_limited = False
            
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    line = line.rstrip()
                    output_lines.append(line)
                    
                    if line:
                        # Check for rate limiting
                        if '429' in line or 'Too Many Requests' in line:
                            rate_limited = True
                            print(f"{Colors.RED}   🚫 RATE LIMITED! (429){Colors.RESET}")
                        
                        # Parse Gobuster output
                        if 'Found' in line or 'Status' in line or '/' in line:
                            status_match = re.search(r'Status:\s*(\d+)', line)
                            if status_match:
                                status = status_match.group(1)
                                status_codes[status] = status_codes.get(status, 0) + 1
                            
                            path_match = re.search(r'/([a-zA-Z0-9_\-\.]+)', line)
                            if path_match:
                                found_entries.append(path_match.group(1))
                            
                            # Colorize output
                            if 'Status: 200' in line:
                                print(f"{Colors.GREEN}   ✅ {line}{Colors.RESET}")
                            elif 'Status: 301' in line or 'Status: 302' in line:
                                print(f"{Colors.YELLOW}   🔄 {line}{Colors.RESET}")
                            elif 'Status: 403' in line:
                                print(f"{Colors.RED}   ⛔ {line}{Colors.RESET}")
                            elif 'Status: 429' in line:
                                print(f"{Colors.RED}   🚫 {line}{Colors.RESET}")
                            else:
                                # Don't print 404s
                                if 'Status: 404' not in line:
                                    print(f"   {line}")
            
            elapsed = time.time() - start_time
            
            result = {
                'name': test_name,
                'success': len(found_entries) > 0,
                'time': elapsed,
                'found': len(found_entries),
                'entries': found_entries[:10],
                'status_codes': status_codes,
                'rate_limited': rate_limited,
                'used_proxy': use_proxy,
                'proxy_used': proxy
            }
            
            if result['success']:
                print(f"{Colors.GREEN}   ✅ Completed in {elapsed:.2f}s - Found {len(found_entries)} entries{Colors.RESET}")
            else:
                print(f"{Colors.RED}   ❌ No output{Colors.RESET}")
            
            return result
            
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}   ❌ Timeout (120s){Colors.RESET}")
            return {'name': test_name, 'success': False, 'time': 120, 'found': 0, 'entries': [], 'status_codes': {}, 'rate_limited': False, 'used_proxy': use_proxy, 'proxy_used': proxy}
        except Exception as e:
            print(f"{Colors.RED}   ❌ Error: {str(e)[:100]}{Colors.RESET}")
            return {'name': test_name, 'success': False, 'time': 0, 'found': 0, 'entries': [], 'status_codes': {}, 'rate_limited': False, 'used_proxy': use_proxy, 'proxy_used': proxy}

    def run_smart_scan(self):
        """Smart scan - direct first, then proxy fallback"""
        self.print_header("🚀 SMART GOBUSTER SCAN - ALL OPTIONS")
        
        if not self.check_gobuster():
            return
        
        wordlist = self.download_wordlist()
        if not wordlist:
            print(f"{Colors.RED}❌ No wordlist found!{Colors.RESET}")
            return
        
        # Test direct connection first
        direct_works = self.check_direct_connection()
        
        # Test proxies if direct is blocked
        if not direct_works:
            print(f"\n{Colors.YELLOW}⚠️ Direct connection failed. Testing proxies...{Colors.RESET}")
            self.proxy_manager.test_all_proxies(max_workers=20)
            
            if not self.proxy_manager.working_proxies:
                print(f"{Colors.RED}❌ No working proxies found!{Colors.RESET}")
                return
        
        # ============================================================
        # ALL GOBUSTER TESTS - FIXED WITH PROPER FLAGS
        # ============================================================
        
        tests = []
        
        # ===== HTTPS TESTS (with proxy if direct blocked) =====
        use_proxy_for_all = not direct_works
        
        # 1. Standard HTTPS Scan
        tests.append({
            'name': 'HTTPS - Standard Scan',
            'desc': 'Common files and directories',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt,js,css,json -o {self.results_dir}/gobuster_https_standard.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 2. HTTPS with Redirect
        tests.append({
            'name': 'HTTPS - With Redirect (-r)',
            'desc': 'Follow redirects',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -r -o {self.results_dir}/gobuster_https_redirect.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 3. HTTPS - All Status Codes (No Filter)
        tests.append({
            'name': 'HTTPS - All Status Codes',
            'desc': 'No status filter',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_https_allstatus.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 4. HTTPS - Verbose Mode
        tests.append({
            'name': 'HTTPS - Verbose Mode (-v)',
            'desc': 'Verbose output',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -v -o {self.results_dir}/gobuster_https_verbose.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 5. HTTPS - No Extensions
        tests.append({
            'name': 'HTTPS - No Extensions',
            'desc': 'Without file extensions',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -o {self.results_dir}/gobuster_https_noext.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 6. HTTPS - Only 200 Status
        tests.append({
            'name': 'HTTPS - Only 200 Status',
            'desc': 'Only accessible files',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_https_only200.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 7. HTTPS - 200,301,302 Only
        tests.append({
            'name': 'HTTPS - 200,301,302 Only',
            'desc': 'No 403 responses',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_https_200301302.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 8. HTTPS - Slow (2 threads)
        tests.append({
            'name': 'HTTPS - Slow (2 threads)',
            'desc': 'Rate limit friendly',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 2 -s 200,301,302,403 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_https_slow.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 9. HTTPS - Fast (30 threads)
        tests.append({
            'name': 'HTTPS - Fast (30 threads)',
            'desc': 'Maximum speed',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 30 -s 200,301,302,403 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_https_fast.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 10. HTTPS - Redirect + Verbose
        tests.append({
            'name': 'HTTPS - Redirect + Verbose',
            'desc': 'Combined flags',
            'cmd': f"gobuster dir -u https://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -r -v -o {self.results_dir}/gobuster_https_redirect_verbose.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # ===== HTTP TESTS =====
        
        # 11. HTTP - Standard
        tests.append({
            'name': 'HTTP - Standard Scan',
            'desc': 'HTTP common files',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_http_standard.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 12. HTTP - With Redirect
        tests.append({
            'name': 'HTTP - With Redirect (-r)',
            'desc': 'HTTP with redirect follow',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -r -o {self.results_dir}/gobuster_http_redirect.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 13. HTTP - All Status
        tests.append({
            'name': 'HTTP - All Status Codes',
            'desc': 'HTTP no filter',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_http_allstatus.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 14. HTTP - Verbose
        tests.append({
            'name': 'HTTP - Verbose Mode (-v)',
            'desc': 'HTTP verbose output',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -v -o {self.results_dir}/gobuster_http_verbose.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 15. HTTP - No Extensions
        tests.append({
            'name': 'HTTP - No Extensions',
            'desc': 'HTTP without extensions',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -o {self.results_dir}/gobuster_http_noext.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 16. HTTP - Only 200
        tests.append({
            'name': 'HTTP - Only 200 Status',
            'desc': 'HTTP accessible only',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -s 200 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_http_only200.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 17. HTTP - Slow (2 threads)
        tests.append({
            'name': 'HTTP - Slow (2 threads)',
            'desc': 'HTTP rate limit friendly',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 2 -s 200,301,302,403 -b \"\" -x php,html,txt -o {self.results_dir}/gobuster_http_slow.txt",
            'use_proxy': use_proxy_for_all
        })
        
        # 18. HTTP - Redirect + Verbose
        tests.append({
            'name': 'HTTP - Redirect + Verbose',
            'desc': 'HTTP combined flags',
            'cmd': f"gobuster dir -u http://{self.clean_target} -w {wordlist} -t 15 -s 200,301,302,403 -b \"\" -x php,html,txt -r -v -o {self.results_dir}/gobuster_http_redirect_verbose.txt",
            'use_proxy': use_proxy_for_all
        })
        
        print(f"\n{Colors.CYAN}🚀 Running {len(tests)} complete tests...{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 {'Using proxies' if use_proxy_for_all else 'Direct mode'}{Colors.RESET}")
        print(f"{Colors.YELLOW}💡 Fixed: -b \"\" (disabled 404 blacklist){Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*70}{Colors.RESET}")
        
        results = []
        proxy_used = None
        
        for idx, test in enumerate(tests, 1):
            print(f"\n{Colors.BOLD}{Colors.CYAN}📝 Test {idx}/{len(tests)}: {test['name']}{Colors.RESET}")
            print(f"{Colors.BLUE}   {test['desc']}{Colors.RESET}")
            
            # Get proxy if needed
            if test['use_proxy']:
                proxy_used = self.proxy_manager.get_proxy()
                if not proxy_used:
                    print(f"{Colors.YELLOW}   ⚠️ No proxy available, trying direct...{Colors.RESET}")
                    test['use_proxy'] = False
            
            result = self.run_gobuster_scan(
                test['name'], 
                test['cmd'], 
                test['use_proxy'], 
                proxy_used
            )
            results.append(result)
            
            # If rate limited, try to get new proxy
            if result.get('rate_limited') and test['use_proxy']:
                print(f"{Colors.RED}   ⚠️ Rate limited! Getting new proxy...{Colors.RESET}")
                self.proxy_manager.mark_failed(proxy_used)
                proxy_used = self.proxy_manager.get_proxy()
            
            # If proxy failed, mark it and get new one
            if test['use_proxy'] and not result['success'] and proxy_used:
                self.proxy_manager.mark_failed(proxy_used)
                proxy_used = self.proxy_manager.get_proxy()
                if proxy_used:
                    print(f"{Colors.GREEN}   🔄 New proxy: {proxy_used[:40]}...{Colors.RESET}")
            
            # Random delay between tests
            if idx < len(tests):
                delay = random.uniform(0.5, 2)
                print(f"{Colors.BLUE}   ⏳ Waiting {delay:.1f}s...{Colors.RESET}")
                time.sleep(delay)
        
        self.test_results = results
        self.show_summary(results)
        self.show_detailed_results(results)
        self.save_report(results)

    def show_summary(self, results):
        """Show test summary"""
        self.print_header("📊 SCAN SUMMARY")
        
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        total_found = sum(r['found'] for r in results)
        rate_limited = sum(1 for r in results if r.get('rate_limited', False))
        proxy_used = sum(1 for r in results if r.get('used_proxy', False))
        
        print(f"{Colors.CYAN}Total Tests: {total}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Successful: {successful}{Colors.RESET}")
        print(f"{Colors.RED}❌ Failed: {total - successful}{Colors.RESET}")
        print(f"{Colors.BLUE}📊 Total Entries Found: {total_found}{Colors.RESET}")
        print(f"{Colors.YELLOW}🔄 Proxy Used: {proxy_used} tests{Colors.RESET}")
        
        if rate_limited > 0:
            print(f"{Colors.RED}⚠️ Rate Limited: {rate_limited} times{Colors.RESET}")
        
        all_status = {}
        for r in results:
            for status, count in r.get('status_codes', {}).items():
                all_status[status] = all_status.get(status, 0) + count
        
        if all_status:
            print(f"\n{Colors.CYAN}📋 Status Codes:{Colors.RESET}")
            for status, count in sorted(all_status.items()):
                if status == '200':
                    print(f"{Colors.GREEN}   • {status}: {count} times (ACCESSIBLE){Colors.RESET}")
                elif status in ['301', '302']:
                    print(f"{Colors.YELLOW}   • {status}: {count} times (REDIRECT){Colors.RESET}")
                elif status == '403':
                    print(f"{Colors.RED}   • {status}: {count} times (FORBIDDEN){Colors.RESET}")
                elif status == '429':
                    print(f"{Colors.RED}   • {status}: {count} times (RATE LIMITED){Colors.RESET}")
                else:
                    print(f"{Colors.BLUE}   • {status}: {count} times{Colors.RESET}")

    def show_detailed_results(self, results):
        """Show detailed results"""
        self.print_header("📋 DETAILED RESULTS")
        
        for idx, r in enumerate(results, 1):
            status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if r['success'] else f"{Colors.RED}❌ FAIL{Colors.RESET}"
            mode = f"{Colors.GREEN}🔓 Direct{Colors.RESET}" if not r.get('used_proxy', False) else f"{Colors.YELLOW}🔄 Proxy{Colors.RESET}"
            rate = f" {Colors.RED}🚫 RATE LIMITED{Colors.RESET}" if r.get('rate_limited', False) else ""
            
            print(f"\n{Colors.CYAN}[{idx}] {r['name']}{rate}{Colors.RESET}")
            print(f"   {status} | Mode: {mode} | Time: {r['time']:.2f}s | Found: {r['found']} entries")
            if r.get('proxy_used'):
                print(f"   {Colors.BLUE}Proxy: {r['proxy_used'][:40]}...{Colors.RESET}")
            
            if r['entries']:
                print(f"   {Colors.BLUE}Sample entries:{Colors.RESET}")
                for entry in r['entries'][:5]:
                    print(f"   {Colors.GREEN}   • {entry}{Colors.RESET}")
                if len(r['entries']) > 5:
                    print(f"   {Colors.YELLOW}   ... and {len(r['entries'])-5} more{Colors.RESET}")

    def save_report(self, results):
        """Save detailed report"""
        report_file = f"{self.results_dir}/report.txt"
        
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("GOBUSTER SMART SCAN REPORT - ALL OPTIONS\n")
            f.write("="*70 + "\n")
            f.write(f"Target: {self.clean_target}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Results Directory: {self.results_dir}\n")
            f.write(f"Wordlist Used: {self.wordlist_path}\n")
            f.write(f"Total Tests: {len(results)}\n")
            f.write(f"Working Proxies: {len(self.proxy_manager.working_proxies)}\n")
            f.write("\n" + "="*70 + "\n\n")
            
            for r in results:
                f.write(f"Test: {r['name']}\n")
                f.write(f"Status: {'PASS' if r['success'] else 'FAIL'}\n")
                f.write(f"Mode: {'Direct' if not r.get('used_proxy', False) else 'Proxy'}\n")
                f.write(f"Time: {r['time']:.2f}s\n")
                f.write(f"Entries Found: {r['found']}\n")
                if r.get('rate_limited', False):
                    f.write("⚠️ Rate Limited Detected\n")
                if r.get('proxy_used'):
                    f.write(f"Proxy Used: {r['proxy_used']}\n")
                
                if r['entries']:
                    f.write("Sample Entries:\n")
                    for entry in r['entries'][:10]:
                        f.write(f"  - {entry}\n")
                    if len(r['entries']) > 10:
                        f.write(f"  ... and {len(r['entries'])-10} more\n")
                
                f.write("-"*40 + "\n")
        
        print(f"\n{Colors.GREEN}✅ Report saved: {report_file}{Colors.RESET}")

def main():
    print(f"""
{Colors.BOLD}{Colors.MAGENTA}
╔═══════════════════════════════════════════════════════════════╗
║     GOBUSTER SMART SCANNER - ALL OPTIONS                   ║
║     Fixed: -b "" to disable 404 blacklist                  ║
║     18 Complete Tests with Proxy Rotation                  ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(f"{Colors.YELLOW}Enter target domain: {Colors.RESET}").strip()
    
    if not target:
        print(f"{Colors.RED}❌ No target provided!{Colors.RESET}")
        sys.exit(1)
    
    proxy_file = input(f"{Colors.YELLOW}Proxy file path (press Enter for default): {Colors.RESET}").strip()
    if not proxy_file:
        proxy_file = None
    
    scanner = GobusterSmartScanner(target, proxy_file)
    scanner.run_smart_scan()
    
    print(f"\n{Colors.GREEN}✅ Scan completed!{Colors.RESET}")
    print(f"{Colors.CYAN}📁 Results saved in: {scanner.results_dir}{Colors.RESET}")

if __name__ == "__main__":
    import threading
    main()