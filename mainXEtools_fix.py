#!/usr/bin/env python3
"""
XE Tools 1.1.2v XE - A Multi-Functional Command Line Utility
-----------------------------------------------------------
Features:
  1. Convert Python scripts (.py) to executables (.exe) using PyInstaller.
  2. IP Analysis: Display your local IP address and geolocation details via ip-api.com.
  3. Send a Discord Webhook Message (generic option).
  4. Nitro Generator: Generate random Discord Nitro gift links (with file saving & webhook sending).
  5. Random IP Generator: Generate random IP addresses (with file saving & webhook sending).
  6. Random Proxy Generator: Generate random proxies (IP:port) (with file saving & webhook sending).
  7. Random Darkweb Links Generator: Generate random .onion links (with file saving & webhook sending).
  8. IP Scanner: Scan a given IP range and display active hosts.
  9. Port Scanner: Scan open ports on a specified IP address.
 10. Website Status Checker.
 11. Hash Generator (MD5, SHA-1, SHA-256).
 12. Code Generator (Python, C++, Java, JavaScript).
 13. Website Info Scanner (retrieves HTTP headers and resolves IP).
 14. Website URL Scanner (extracts status and title).
 15. IP Pinger (pings an IP multiple times).
 16. Bluetooth Spam (choose device type and send messages via Bluetooth RFCOMM).
 17. Self Security (runs a security scan using process data).
 18. Anti Graffer (checks for known screen capture/grabber processes).
 19. Anti Graffer v2 Beta (advanced check for suspicious processes).
 20. About XE Tools (includes Discord and GitHub links).
 21. Exit.
 22. Nitro Generator v2 (sends each generated Nitro code as a separate Discord message with faster sending).
 
Each generator offers an option to save its output to a file and/or send it via a Discord webhook.
Detailed logging is maintained in "xe_tools.log" for debugging purposes.

Developed by devolepaera xynixdev.
License: MIT
"""

# ------------------------ Imports ------------------------
import os
import socket
import requests
import random
import string
import logging
import time
import shutil
import pyfiglet
import re
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor
import subprocess
from pathlib import Path
import hashlib
import psutil  # For process monitoring

# For Bluetooth functionality – requires PyBluez.
try:
    import bluetooth
except ImportError:
    bluetooth = None

# ------------------------ Global Constants ------------------------
BOX_WIDTH = 100  # Width for boxed text

# ------------------------ Initialization ------------------------
init(autoreset=True)
logging.basicConfig(
    filename="xe_tools.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------ Utility Functions ------------------------
def clear_screen():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")

def print_centered(text, width=BOX_WIDTH):
    """Prints the given text centered within the specified width."""
    print(text.center(width))

def print_boxed(text, width=BOX_WIDTH, padding=1, border_color=Fore.RED):
    """
    Prints the text block inside a decorative box.
    :param text: Text to print (supports multiple lines).
    :param width: Overall width of the box.
    :param padding: Number of empty lines above and below the text.
    :param border_color: Color for the border.
    """
    border_line = border_color + "+" + "-" * (width - 2) + "+"
    print(border_line)
    for _ in range(padding):
        print(border_color + "|" + " " * (width - 2) + "|")
    for line in text.splitlines():
        print(border_color + "|" + line.center(width - 2) + "|")
    for _ in range(padding):
        print(border_color + "|" + " " * (width - 2) + "|")
    print(border_line)

def pause():
    """Pauses until the user presses Enter."""
    input(Fore.WHITE + "\nPress Enter to return to the menu...")

def print_header():
    """Prints a centered header banner using pyfiglet."""
    clear_screen()
    try:
        banner = pyfiglet.figlet_format("XE Tools", font="slant")
    except Exception:
        banner = "XE Tools"
    for line in banner.splitlines():
        print(Fore.RED + line.center(BOX_WIDTH))
    print_centered("Version 1.1.2v XE")
    print("\n")

def save_or_send(data, filename):
    """
    Offers the user the option to save the generated data to a file and/or send it via Discord Webhook.
    :param data: The data as a string.
    :param filename: The filename to save the data.
    """
    choice = input("Do you want to save to a file? (y/n): ").strip().lower()
    if choice == "y":
        with open(filename, "w") as f:
            f.write(data)
        print(Fore.GREEN + f"Saved to {filename}")
    webhook_choice = input("Do you want to send via Discord Webhook? (y/n): ").strip().lower()
    if webhook_choice == "y":
        webhook_url = input("Enter your Webhook URL: ").strip()
        try:
            requests.post(webhook_url, json={"content": data})
            print(Fore.GREEN + "Sent to Discord Webhook!")
        except Exception as e:
            print(Fore.RED + "Error sending webhook:", e)

# ------------------------ Core Functions ------------------------

def convert_py_to_exe():
    """Converts a Python script to an executable (.exe) using PyInstaller."""
    print_boxed("Convert .py to .exe", width=BOX_WIDTH)
    file_path = input("Enter the path to the .py file: ").strip()
    if not os.path.exists(file_path):
        print(Fore.RED + "❌ File does not exist! Check the path and try again.")
        return
    icon_path = input("Enter the path to the icon (.ico) or leave empty: ").strip()
    hide_console = input("Hide console? (yes/no): ").strip().lower()
    output_dir = input("Enter the output directory or leave empty for default (dist): ").strip()
    if not output_dir:
        output_dir = "dist"
    extra_options = input("Enter any extra PyInstaller options (or leave empty): ").strip()

    command = ["pyinstaller", "--onefile"]
    if icon_path and os.path.exists(icon_path):
        command.extend(["--icon", icon_path])
    if hide_console == "yes":
        command.append("--noconsole")
    if extra_options:
        command.extend(extra_options.split())
    command.append(file_path)
    command.extend(["--distpath", output_dir])
    
    print("\n🔄 Starting conversion...\n")
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode == 0:
        print(Fore.GREEN + "✅ Conversion completed successfully!")
        exe_file = Path(output_dir) / (Path(file_path).stem + ".exe")
        if exe_file.exists():
            print(f"\nExecutable file is located at: {exe_file.resolve()}")
        else:
            print(Fore.RED + "\nExecutable file not found. Check logs for errors.")
    else:
        print(Fore.RED + "\n❌ An error occurred during conversion!")
        print(process.stderr)
    time.sleep(1)
    print("\n🧹 Cleaning temporary files...")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("__pycache__", ignore_errors=True)
    spec_file = Path(file_path).stem + ".spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
    print(Fore.GREEN + "✅ Cleanup completed!")
    print("\n🎉 Process completed! Check the output directory for your executable.")

def ip_analysis():
    """Displays local IP address and geolocation details."""
    print_boxed("IP Analysis", width=BOX_WIDTH)
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        print(f"Local IP Address: {local_ip}")
    except Exception as e:
        print(Fore.RED + "Error obtaining local IP address:", e)
        return
    try:
        response = requests.get(f"http://ip-api.com/json/{local_ip}", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            print("\nGeolocation Information:")
            print(f"  Country: {data.get('country', 'N/A')}")
            print(f"  Region: {data.get('regionName', 'N/A')}")
            print(f"  City: {data.get('city', 'N/A')}")
            print(f"  ISP: {data.get('isp', 'N/A')}")
            print(f"  Latitude: {data.get('lat', 'N/A')}")
            print(f"  Longitude: {data.get('lon', 'N/A')}")
        else:
            print(Fore.RED + "Failed to retrieve geolocation information.")
    except Exception as e:
        print(Fore.RED + "Error retrieving geolocation information:", e)

def send_discord_webhook_message():
    """Sends a custom message to a Discord webhook."""
    print_boxed("Discord Webhook Message", width=BOX_WIDTH)
    webhook_url = input("Enter the Discord Webhook URL: ").strip()
    message = input("Enter the message to send: ").strip()
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code in (200, 204):
            print(Fore.GREEN + "✅ Message sent successfully!")
        else:
            print(Fore.RED + f"❌ Failed to send message! HTTP status: {response.status_code}")
    except Exception as e:
        print(Fore.RED + "Error sending webhook message:", e)

def nitro_generator():
    """Generates random Discord Nitro gift links with options to save/send."""
    print_boxed("Nitro Generator", width=BOX_WIDTH)
    try:
        num = int(input("Enter the number of Nitro codes to generate: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    output = ""
    for _ in range(num):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        line = f"discord.gift/{code}\n"
        output += line
        print(Fore.GREEN + line, end='')
    save_or_send(output, "nitro_codes.txt")

def nitro_generator_v2():
    """
    Generates random Discord Nitro gift links and sends each as a separate message via Discord Webhook.
    Each message is sent individually with a 0.1-second delay.
    """
    print_boxed("Nitro Generator v2", width=BOX_WIDTH)
    try:
        num = int(input("Enter the number of Nitro codes to generate and send: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    webhook_url = input("Enter your Discord Webhook URL: ").strip()
    sent_success = 0
    for i in range(num):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        content = f"discord.gift/{code}"
        try:
            response = requests.post(webhook_url, json={"content": content}, timeout=5)
            if response.status_code in (200, 204):
                print(Fore.GREEN + f"Message {i+1} sent successfully: {content}")
                sent_success += 1
            else:
                print(Fore.RED + f"Message {i+1} failed (HTTP {response.status_code}): {content}")
        except Exception as e:
            print(Fore.RED + f"Message {i+1} failed: {e}")
        time.sleep(0.1)
    print(Fore.WHITE + f"\nTotal messages sent successfully: {sent_success}/{num}")

def random_ip_generator():
    """Generates random IP addresses with options to save/send."""
    print_boxed("Random IP Generator", width=BOX_WIDTH)
    try:
        num = int(input("Enter the number of IP addresses to generate: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    output = ""
    for _ in range(num):
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        output += ip + "\n"
        print(Fore.GREEN + ip)
    save_or_send(output, "random_ips.txt")

def random_proxy_generator():
    """Generates random proxies (IP:port) with options to save/send."""
    print_boxed("Random Proxy Generator", width=BOX_WIDTH)
    try:
        num = int(input("Enter the number of proxies to generate: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    output = ""
    for _ in range(num):
        ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
        port = random.randint(1024, 65535)
        line = f"{ip}:{port}\n"
        output += line
        print(Fore.GREEN + line, end='')
    save_or_send(output, "random_proxies.txt")

def random_darkweb_links_generator():
    """Generates random darkweb (.onion) links with options to save/send."""
    print_boxed("Random Darkweb Links Generator", width=BOX_WIDTH)
    try:
        num = int(input("Enter the number of darkweb links to generate: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    output = ""
    for _ in range(num):
        link_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        line = f"http://{link_id}.onion\n"
        output += line
        print(Fore.GREEN + line, end='')
    save_or_send(output, "darkweb_links.txt")

def ip_scanner():
    """Scans a given IP range and displays active hosts."""
    print_boxed("IP Scanner", width=BOX_WIDTH)
    subnet = input("Enter subnet (e.g., 192.168.1.): ").strip()
    active_hosts = []
    def ping_host(ip):
        response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1" if os.name != "nt" else f"ping -n 1 {ip} >nul")
        if response == 0:
            active_hosts.append(ip)
            print(Fore.GREEN + f"[ACTIVE] {ip}")
    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(1, 255):
            executor.submit(ping_host, f"{subnet}{i}")
    print("\nActive Hosts:", active_hosts)

def port_scanner():
    """Scans open ports on a specified IP address."""
    print_boxed("Port Scanner", width=BOX_WIDTH)
    target_ip = input("Enter target IP: ").strip()
    ports = [21, 22, 25, 53, 80, 443, 3306, 8080]
    open_ports = []
    def scan_port(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((target_ip, port)) == 0:
                open_ports.append(port)
                print(Fore.GREEN + f"[OPEN] Port {port}")
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_port, ports)
    print("\nOpen Ports:", open_ports)

def website_status_checker():
    """Checks the status of a website."""
    print_boxed("Website Status Checker", width=BOX_WIDTH)
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    try:
        response = requests.get(url, timeout=5)
        print(Fore.GREEN + f"✅ {url} is online. Status Code: {response.status_code}")
    except requests.RequestException:
        print(Fore.RED + f"❌ {url} is unreachable.")

def hash_generator():
    """Generates hash values (MD5, SHA-1, SHA-256) for a given input."""
    print_boxed("Hash Generator", width=BOX_WIDTH)
    text = input("Enter text to hash: ").strip()
    print(Fore.GREEN + f"MD5: {hashlib.md5(text.encode()).hexdigest()}")
    print(Fore.GREEN + f"SHA-1: {hashlib.sha1(text.encode()).hexdigest()}")
    print(Fore.GREEN + f"SHA-256: {hashlib.sha256(text.encode()).hexdigest()}")

def code_generator():
    """Generates a basic script template in Python, C++, Java, or JavaScript."""
    print_boxed("Code Generator", width=BOX_WIDTH)
    languages = {"1": "Python", "2": "C++", "3": "Java", "4": "JavaScript"}
    print("Select language:")
    for key, value in languages.items():
        print(f"{key}. {value}")
    choice = input("Choose (1-4): ").strip()
    templates = {
        "1": "# Python script template\nprint('Hello, World!')",
        "2": "// C++ script template\n#include <iostream>\nusing namespace std;\nint main() { cout << \"Hello, World!\"; return 0; }",
        "3": "// Java script template\npublic class Main { public static void main(String[] args) { System.out.println(\"Hello, World!\"); } }",
        "4": "// JavaScript script template\nconsole.log('Hello, World!');"
    }
    print("\nGenerated Template:\n" + templates.get(choice, "Invalid choice"))

def website_info_scanner():
    """Scans a website by retrieving HTTP headers and resolving its IP address."""
    print_boxed("Website Info Scanner", width=BOX_WIDTH)
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    try:
        response = requests.get(url, timeout=5)
        print(Fore.GREEN + f"Status Code: {response.status_code}")
        print("HTTP Headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        hostname = url.split('//')[-1].split('/')[0]
        try:
            ip = socket.gethostbyname(hostname)
            print(f"Resolved IP: {ip}")
        except Exception as e:
            print(Fore.RED + "Error resolving IP:", e)
    except Exception as e:
        print(Fore.RED + "Error retrieving website info:", e)

def website_url_scanner():
    """Scans a website URL and extracts basic information like status and title."""
    print_boxed("Website URL Scanner", width=BOX_WIDTH)
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    try:
        response = requests.get(url, timeout=5)
        print(Fore.GREEN + f"Status Code: {response.status_code}")
        match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
        title = match.group(1).strip() if match else "N/A"
        print(f"Page Title: {title}")
    except Exception as e:
        print(Fore.RED + "Error scanning website URL:", e)

def ip_pinger():
    """Pings a given IP address a specified number of times and displays the result."""
    print_boxed("IP Pinger", width=BOX_WIDTH)
    ip = input("Enter IP address to ping: ").strip()
    try:
        count = int(input("Enter number of pings: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    cmd = ["ping", "-c", str(count), ip] if os.name != "nt" else ["ping", "-n", str(count), ip]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        print(Fore.GREEN + "Ping results:\n" + output)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + "Error pinging IP:", e.output)

def bluetooth_spam():
    """Sends Bluetooth messages to a selected device using RFCOMM."""
    print_boxed("Bluetooth Spam", width=BOX_WIDTH)
    if bluetooth is None:
        print(Fore.RED + "PyBluez not installed or Bluetooth not supported on this system.")
        return
    print("Scanning for nearby Bluetooth devices...")
    try:
        nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
    except Exception as e:
        print(Fore.RED + "Error during Bluetooth discovery:", e)
        return
    if not nearby_devices:
        print(Fore.YELLOW + "No Bluetooth devices found.")
        return
    print("Found devices:")
    for idx, (addr, name) in enumerate(nearby_devices, start=1):
        print(f"{idx}. {name} ({addr})")
    try:
        choice = int(input("Select a device number to send messages: ").strip())
        if choice < 1 or choice > len(nearby_devices):
            print(Fore.RED + "Invalid choice.")
            return
    except ValueError:
        print(Fore.RED + "Invalid input.")
        return
    target = nearby_devices[choice-1]
    print(Fore.GREEN + f"Selected device: {target[1]} ({target[0]})")
    try:
        num_messages = int(input("Enter the number of messages to send: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    message = input("Enter the message to send: ").strip()
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((target[0], 1))
        for i in range(num_messages):
            sock.send(message)
            print(Fore.CYAN + f"Sent message {i+1}/{num_messages} to {target[1]} ({target[0]})")
            time.sleep(0.5)
        sock.close()
        print(Fore.GREEN + "Bluetooth spam completed successfully.")
    except Exception as e:
        print(Fore.RED + "Error sending Bluetooth messages:", e)

def self_security():
    """Performs a self security check using process data."""
    print_boxed("Self Security Check", width=BOX_WIDTH)
    print("Performing security scan...\n")
    vulnerable_processes = ["telnet.exe", "ftp.exe", "nc.exe"]
    found = False
    for proc in psutil.process_iter(['name']):
        try:
            pname = proc.info['name'].lower()
            for vp in vulnerable_processes:
                if vp in pname:
                    print(Fore.YELLOW + f"Warning: Vulnerable process detected: {pname}")
                    found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not found:
        print(Fore.GREEN + "No vulnerable processes detected.")
    print(Fore.GREEN + "\nSecurity Check Complete.")

def anti_graffer():
    """Checks for suspicious screen capture/grabber processes."""
    print_boxed("Anti Graffer", width=BOX_WIDTH)
    suspicious = ["snippingtool.exe", "greenshot.exe", "lightshot.exe", "gyazo.exe", "screenpresso.exe"]
    found = []
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name'].lower()
            for s in suspicious:
                if s in name:
                    found.append(name)
                    print(Fore.YELLOW + f"Suspicious process detected: {name}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not found:
        print(Fore.GREEN + "No graffer activity detected.")

def anti_graffer_v2_beta():
    """Performs an advanced anti graffer scan (Beta) using CPU usage metrics."""
    print_boxed("Anti Graffer v2 Beta", width=BOX_WIDTH)
    suspicious = ["snippingtool.exe", "greenshot.exe", "lightshot.exe", "gyazo.exe", "screenpresso.exe"]
    found = []
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            name = proc.info['name'].lower()
            cpu = proc.info['cpu_percent']
            for s in suspicious:
                if s in name:
                    found.append((name, cpu))
                    print(Fore.YELLOW + f"Suspicious process: {name}, CPU Usage: {cpu}%")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if not found:
        print(Fore.GREEN + "No suspicious graffer activity detected (Beta).")

def website_info_scanner():
    """Scans a website by retrieving HTTP headers and resolving its IP address."""
    print_boxed("Website Info Scanner", width=BOX_WIDTH)
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    try:
        response = requests.get(url, timeout=5)
        print(Fore.GREEN + f"Status Code: {response.status_code}")
        print("HTTP Headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        hostname = url.split('//')[-1].split('/')[0]
        try:
            ip = socket.gethostbyname(hostname)
            print(f"Resolved IP: {ip}")
        except Exception as e:
            print(Fore.RED + "Error resolving IP:", e)
    except Exception as e:
        print(Fore.RED + "Error retrieving website info:", e)

def website_url_scanner():
    """Scans a website URL and extracts basic information like status and title."""
    print_boxed("Website URL Scanner", width=BOX_WIDTH)
    url = input("Enter website URL (e.g., https://example.com): ").strip()
    try:
        response = requests.get(url, timeout=5)
        print(Fore.GREEN + f"Status Code: {response.status_code}")
        match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
        title = match.group(1).strip() if match else "N/A"
        print(f"Page Title: {title}")
    except Exception as e:
        print(Fore.RED + "Error scanning website URL:", e)

def ip_pinger():
    """Pings a given IP address a specified number of times and displays the result."""
    print_boxed("IP Pinger", width=BOX_WIDTH)
    ip = input("Enter IP address to ping: ").strip()
    try:
        count = int(input("Enter number of pings: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid input. Numeric value required.")
        return
    cmd = ["ping", "-c", str(count), ip] if os.name != "nt" else ["ping", "-n", str(count), ip]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        print(Fore.GREEN + "Ping results:\n" + output)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + "Error pinging IP:", e.output)

def about_xe_tools():
    """Displays information about XE Tools and community links."""
    print_boxed("About XE Tools", width=BOX_WIDTH)
    about_text = (
        "XE Tools is a versatile command line utility offering multiple functions:\n"
        "- Convert Python scripts to executables (.exe) using PyInstaller.\n"
        "- Perform IP analysis and geolocation lookup.\n"
        "- Send messages via Discord webhooks.\n"
        "- Generate random Discord Nitro gift links.\n"
        "- Generate random IP addresses, proxies, and darkweb (.onion) links.\n"
        "- Scan IP ranges and check open ports.\n"
        "- Check website status, retrieve website info, generate hashes, and create code templates.\n"
        "- Ping an IP address multiple times.\n"
        "- Send Bluetooth messages to nearby devices.\n"
        "- Perform a self security check using process data.\n"
        "- Check for suspicious screen capture (graffer) processes (basic and advanced beta).\n\n"
        "Community:\n"
        "  Discord: https://discord.gg/NNdjKNRftv\n"
        "  GitHub: https://github.com/XynixDev\n\n"
        "Developed by devolepaera xynixdev | License: MIT"
    )
    print(Fore.CYAN + about_text)

# ------------------------ Multi-Page Menu Navigation ------------------------

def main_menu():
    """
    Displays a multi-page menu with a centered, bordered interface.
    Menu is divided into 3 pages:
      - Page 1: Options 1-6
      - Page 2: Options 7-11
      - Page 3: Options 12-22
    Navigation: 'n' for next page, 'p' for previous page, 'q' to exit.
    """
    current_page = 1
    while True:
        print_header()
        if current_page == 1:
            box_text = (
                "Main Menu (Page 1 of 3)\n\n"
                "1. Convert .py to .exe\n"
                "2. IP Analysis\n"
                "3. Send Discord Webhook Message\n"
                "4. Nitro Generator\n"
                "5. Random IP Generator\n"
                "6. Random Proxy Generator\n\n"
                "Press 'n' for next page | 'q' to Exit"
            )
            print_boxed(box_text, width=BOX_WIDTH, padding=1)
            choice = input("\nSelect an option: ").strip().lower()
            if choice == "1":
                convert_py_to_exe()
            elif choice == "2":
                ip_analysis()
            elif choice == "3":
                send_discord_webhook_message()
            elif choice == "4":
                nitro_generator()
            elif choice == "5":
                random_ip_generator()
            elif choice == "6":
                random_proxy_generator()
            elif choice == "n":
                current_page = 2
            elif choice == "q":
                print("Exiting XE Tools. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid option!")
            pause()
        elif current_page == 2:
            box_text = (
                "Main Menu (Page 2 of 3)\n\n"
                "7. Random Darkweb Links Generator\n"
                "8. IP Scanner\n"
                "9. Port Scanner\n"
                "10. Website Status Checker\n"
                "11. Hash Generator\n\n"
                "Press 'n' for next page | 'p' for previous page | 'q' to Exit"
            )
            print_boxed(box_text, width=BOX_WIDTH, padding=1)
            choice = input("\nSelect an option: ").strip().lower()
            if choice == "7":
                random_darkweb_links_generator()
            elif choice == "8":
                ip_scanner()
            elif choice == "9":
                port_scanner()
            elif choice == "10":
                website_status_checker()
            elif choice == "11":
                hash_generator()
            elif choice == "n":
                current_page = 3
            elif choice == "p":
                current_page = 1
            elif choice == "q":
                print("Exiting XE Tools. Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid option!")
            pause()
        elif current_page == 3:
            box_text = (
                "Main Menu (Page 3 of 3)\n\n"
                "12. Code Generator\n"
                "13. Website Info Scanner\n"
                "14. Website URL Scanner\n"
                "15. IP Pinger\n"
                "16. Bluetooth Spam\n"
                "17. Self Security\n"
                "18. Anti Graffer\n"
                "19. Anti Graffer v2 Beta\n"
                "20. About XE Tools\n"
                "21. Exit\n"
                "22. Nitro Generator v2\n\n"
                "Press 'p' for previous page | 'q' to Exit"
            )
            print_boxed(box_text, width=BOX_WIDTH, padding=1)
            choice = input("\nSelect an option: ").strip().lower()
            if choice == "12":
                code_generator()
            elif choice == "13":
                website_info_scanner()
            elif choice == "14":
                website_url_scanner()
            elif choice == "15":
                ip_pinger()
            elif choice == "16":
                bluetooth_spam()
            elif choice == "17":
                self_security()
            elif choice == "18":
                anti_graffer()
            elif choice == "19":
                anti_graffer_v2_beta()
            elif choice == "20":
                about_xe_tools()
            elif choice == "21" or choice == "q":
                print("Exiting XE Tools. Goodbye!")
                break
            elif choice == "22":
                nitro_generator_v2()
            elif choice == "p":
                current_page = 2
            else:
                print(Fore.RED + "Invalid option!")
            pause()

# ------------------------ Main Program ------------------------
if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        logging.critical("Unexpected error: " + str(e))
