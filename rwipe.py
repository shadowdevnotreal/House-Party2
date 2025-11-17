#!/usr/bin/python3

"""
RWIPE v2.0 - Emergency Evidence Protection System
Original Concept: Utku Sen (Jani) | utkusen.com
Refactored & Enhanced: Shadow Dev | 2024

WARNING: Use only for authorized data protection scenarios.
Misuse may result in criminal charges.
"""

import subprocess
import sys
import os

# Auto-install dependencies
def check_dependencies():
    """Check and install required dependencies."""
    required = {'pycryptodome': 'Crypto', 'requests': 'requests'}
    missing = []

    for package, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"\033[93m⚠️  Missing dependencies: {', '.join(missing)}\033[0m")
        print("\033[96m📦 Installing required packages...\033[0m")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("\033[92m✓ Dependencies installed successfully!\033[0m\n")
        except subprocess.CalledProcessError:
            print("\033[91m❌ Failed to install dependencies. Please run: pip install pycryptodome requests\033[0m")
            sys.exit(1)

check_dependencies()

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import urllib.request
import argparse
from time import sleep
import requests
import time
import logging
from datetime import datetime, timedelta

# ANSI Color codes matching project theme
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(f'''{Colors.OKCYAN}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████╗ ██╗    ██╗██╗██████╗ ███████╗                     ║
║   ██╔══██╗██║    ██║██║██╔══██╗██╔════╝                     ║
║   ██████╔╝██║ █╗ ██║██║██████╔╝█████╗                       ║
║   ██╔══██╗██║███╗██║██║██╔═══╝ ██╔══╝                       ║
║   ██║  ██║╚███╔███╔╝██║██║     ███████╗                     ║
║   ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝                     ║
║                                                               ║
║        🛡️  EMERGENCY EVIDENCE PROTECTION SYSTEM  🛡️          ║
║                    Version 2.0                                ║
║                                                               ║
║   ⚡ House Party Protocol - Activated ⚡                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    {Colors.BOLD}Original Concept:{Colors.ENDC} Utku Sen (Jani) | utkusen.com
    {Colors.BOLD}Refactored & Enhanced:{Colors.ENDC} Shadow Dev | 2024

    {Colors.WARNING}Inspired by Iron Man 3 - House Party Protocol{Colors.ENDC}
    {Colors.OKCYAN}"Sometimes you gotta run before you can walk."{Colors.ENDC}

''')

def setup_logging(verbose=False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format=f'{Colors.OKCYAN}[%(asctime)s]{Colors.ENDC} %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def pad(s):
    """Pad data to AES block size."""
    block_size = AES.block_size
    return s + b"\0" * (block_size - len(s) % block_size)

def encrypt(message, key):
    """Encrypt message with AES-256-CBC."""
    message = pad(message)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def encrypt_file(file_name, key):
    """Encrypt a single file."""
    try:
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = encrypt(plaintext, key)
        with open(file_name, 'wb') as fo:
            fo.write(enc)
        return True
    except Exception as e:
        logging.error(f"Failed to encrypt {file_name}: {e}")
        return False

def create_key(password):
    """Derive encryption key from password using PBKDF2."""
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    return key, salt

def count_files(location):
    """Count total files in directory."""
    total = 0
    for root, _, files in os.walk(location):
        total += len(files)
    return total

def destroy_directory(location, password, confirm=True):
    """Encrypt all files in directory recursively."""
    if confirm:
        total_files = count_files(location)
        print(f"\n{Colors.WARNING}⚠️  WARNING: This will encrypt {total_files} files in: {location}{Colors.ENDC}")
        print(f"{Colors.WARNING}⚠️  This action is IRREVERSIBLE without the password!{Colors.ENDC}")
        confirmation = input(f"\n{Colors.FAIL}Type 'DESTROY' to confirm: {Colors.ENDC}")
        if confirmation != 'DESTROY':
            print(f"{Colors.OKGREEN}✓ Operation cancelled.{Colors.ENDC}")
            return

    key, salt = create_key(password)
    encrypted_count = 0
    failed_count = 0

    print(f"\n{Colors.OKCYAN}🔐 Starting encryption process...{Colors.ENDC}\n")

    try:
        for root, _, files in os.walk(location):
            for fil in files:
                fname = os.path.join(root, fil)
                if encrypt_file(fname, key):
                    encrypted_count += 1
                    print(f"{Colors.OKGREEN}✓{Colors.ENDC} {fname}")
                else:
                    failed_count += 1
                    print(f"{Colors.FAIL}✗{Colors.ENDC} {fname}")

        print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Action completed!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}  Encrypted: {encrypted_count} files{Colors.ENDC}")
        if failed_count > 0:
            print(f"{Colors.WARNING}  Failed: {failed_count} files{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}\n")

    except Exception as e:
        logging.error(f"Error during directory encryption: {e}")
        print(f"{Colors.FAIL}❌ Encryption process encountered an error.{Colors.ENDC}")

def check_url(url):
    """Check URL for trigger command."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "start" in response.text.lower():
            return True
    except Exception as e:
        logging.debug(f"Error checking URL: {e}")
    return False

def check_alive_signal(url):
    """Check for alive signal from URL (dead man switch)."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "alive" in response.text.lower():
            return True
    except Exception as e:
        logging.debug(f"Error checking alive signal: {e}")
    return False

def listener_local(location, password):
    """Local mode: Manual trigger via keyboard input."""
    print(f"{Colors.OKCYAN}🎯 Local Mode Active{Colors.ENDC}")
    print(f"{Colors.BOLD}Press 'Y' and Enter to start action.{Colors.ENDC}\n")

    while True:
        response = input(f"{Colors.WARNING}> {Colors.ENDC}")
        if response.lower() == 'y':
            print(f"\n{Colors.FAIL}--Action Started!--{Colors.ENDC}")
            destroy_directory(location, password)
            break
        elif response.lower() == 'q':
            print(f"{Colors.OKGREEN}✓ Exiting...{Colors.ENDC}")
            break

def listener_remote(url, interval, location, password):
    """Remote mode: Trigger via URL monitoring."""
    print(f"{Colors.OKCYAN}📡 Remote Mode Active{Colors.ENDC}")
    print(f"{Colors.BOLD}Monitoring: {url}{Colors.ENDC}")
    print(f"{Colors.BOLD}Check interval: {interval}s{Colors.ENDC}\n")
    print(f"{Colors.OKGREEN}Status: Listening...{Colors.ENDC}")

    while True:
        if check_url(url):
            print(f"\n{Colors.FAIL}🚨 TRIGGER DETECTED!{Colors.ENDC}")
            print(f"{Colors.FAIL}--Action Started!--{Colors.ENDC}")
            destroy_directory(location, password, confirm=False)
            break
        sleep(interval)

def listener_deadman(url, check_interval, grace_period, location, password):
    """Dead man switch mode: Activate if no alive signal received."""
    print(f"{Colors.FAIL}☠️  Dead Man Switch Mode Active{Colors.ENDC}")
    print(f"{Colors.BOLD}Monitoring: {url}{Colors.ENDC}")
    print(f"{Colors.BOLD}Check interval: {check_interval}s{Colors.ENDC}")
    print(f"{Colors.BOLD}Grace period: {grace_period}s{Colors.ENDC}\n")

    last_alive = datetime.now()
    grace_deadline = last_alive + timedelta(seconds=grace_period)

    print(f"{Colors.WARNING}⏱️  Dead man switch armed.{Colors.ENDC}")
    print(f"{Colors.WARNING}⏱️  Grace period ends: {grace_deadline.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")

    while True:
        if check_alive_signal(url):
            last_alive = datetime.now()
            grace_deadline = last_alive + timedelta(seconds=grace_period)
            print(f"{Colors.OKGREEN}✓ Alive signal received at {last_alive.strftime('%H:%M:%S')}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}  Next deadline: {grace_deadline.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
        else:
            time_since_alive = (datetime.now() - last_alive).total_seconds()

            if time_since_alive >= grace_period:
                print(f"\n{Colors.FAIL}☠️  DEAD MAN SWITCH TRIGGERED!{Colors.ENDC}")
                print(f"{Colors.FAIL}⚠️  No alive signal for {int(time_since_alive)}s (grace: {grace_period}s){Colors.ENDC}")
                print(f"{Colors.FAIL}--Action Started!--{Colors.ENDC}")
                destroy_directory(location, password, confirm=False)
                break
            else:
                remaining = grace_period - int(time_since_alive)
                print(f"{Colors.WARNING}⏳ No signal. Time until trigger: {remaining}s{Colors.ENDC}")

        sleep(check_interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='RWIPE v2.0 - Emergency Evidence Protection System',
        epilog='Use responsibly. For authorized data protection only.'
    )

    # Required arguments
    parser.add_argument('-d', '--directory', action='store', dest='location',
                        help='Directory to be encrypted', required=True)
    parser.add_argument('-m', '--mode', action='store', dest='mode',
                        help="Mode: 'local', 'remote', or 'deadman'", required=True)
    parser.add_argument('-p', '--password', action='store', dest='password',
                        help='Password for key derivation', required=True)

    # Optional arguments
    parser.add_argument('-u', '--url', action='store', dest='url',
                        help='URL for remote/deadman mode')
    parser.add_argument('-i', '--interval', action='store', dest='interval',
                        help='Check interval in seconds (default: 60)',
                        required=False, type=int, default=60)
    parser.add_argument('-g', '--grace', action='store', dest='grace_period',
                        help='Grace period for deadman mode in seconds (default: 300)',
                        required=False, type=int, default=300)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    parser.add_argument('--no-confirm', action='store_true',
                        help='Skip confirmation prompt (dangerous!)')

    argv = parser.parse_args()

    # Setup logging
    setup_logging(argv.verbose)

    # Validate directory
    if not os.path.exists(argv.location):
        print(f"{Colors.FAIL}❌ Error: Directory does not exist: {argv.location}{Colors.ENDC}")
        sys.exit(1)

    if not os.path.isdir(argv.location):
        print(f"{Colors.FAIL}❌ Error: Path is not a directory: {argv.location}{Colors.ENDC}")
        sys.exit(1)

    # Execute based on mode
    try:
        if argv.mode == 'local':
            listener_local(argv.location, argv.password)

        elif argv.mode == 'remote':
            if not argv.url:
                print(f"{Colors.FAIL}❌ Error: URL (-u) is required for remote mode.{Colors.ENDC}")
                sys.exit(1)
            listener_remote(argv.url, argv.interval, argv.location, argv.password)

        elif argv.mode == 'deadman':
            if not argv.url:
                print(f"{Colors.FAIL}❌ Error: URL (-u) is required for deadman mode.{Colors.ENDC}")
                sys.exit(1)
            listener_deadman(argv.url, argv.interval, argv.grace_period,
                           argv.location, argv.password)

        else:
            print(f"{Colors.FAIL}❌ Invalid mode: {argv.mode}{Colors.ENDC}")
            print(f"{Colors.WARNING}Valid modes: local, remote, deadman{Colors.ENDC}")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Interrupted by user.{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Exiting safely...{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"{Colors.FAIL}❌ Fatal error occurred. Check logs.{Colors.ENDC}")
        sys.exit(1)
