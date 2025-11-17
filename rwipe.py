#!/usr/bin/python3

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import urllib.request
import os
import argparse
from time import sleep
import sys
import requests
import time

print('''
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

    Original Concept: Utku Sen (Jani) | utkusen.com
    Refactored & Enhanced: Shadow Dev | 2024

    Inspired by Iron Man 3 - House Party Protocol
    "Sometimes you gotta run before you can walk."

''')

def pad(s):
    block_size = AES.block_size
    return s + b"\0" * (block_size - len(s) % block_size)

def encrypt(message, key):
    message = pad(message)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name, 'wb') as fo:
        fo.write(enc)

def create_key(password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    return key, salt

def destroy_directory(location, password):
    key, salt = create_key(password)
    try:
        for root, _, files in os.walk(location):
            for fil in files:
                fname = os.path.join(root, fil)
                encrypt_file(fname, key)
                print(fname + " is encrypted")
        print("---Action completed!---")
    except Exception as e:
        print(f"Error encrypting directory: {e}")

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "start" in response.text:
            return True
    except Exception as e:
        print(f"Error checking URL: {e}")
    return False

def listener_local(location, password):
    print("Press 'Y' and Enter to start action.")
    while True:
        response = input()
        if response.lower() == 'y':
            print("--Action Started!--")
            destroy_directory(location, password)
            break

def listener_remote(url, interval, location, password):
    print("Status: Listening")
    while True:
        if check_url(url):
            print("--Action Started!--")
            destroy_directory(location, password)
            break
        sleep(interval)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store', dest='location', help='Directory to be encrypted', required=True)
    parser.add_argument('-u', action='store', dest='url', help='URL where the program listens for commands', required=False)
    parser.add_argument('-i', action='store', dest='interval', help='Interval for checking the URL (only needed for remote)', required=False, type=int)
    parser.add_argument('-m', action='store', dest='mode', help="Mode: 'local' or 'remote'", required=True)
    parser.add_argument('-p', action='store', dest='password', help='Password for key derivation', required=True)
    argv = parser.parse_args()

    if not os.path.exists(argv.location):
        print("Error: Directory does not exist.")
        sys.exit(1)

    if argv.mode == 'local':
        listener_local(argv.location, argv.password)
    elif argv.mode == 'remote':
        if argv.url and argv.interval:
            listener_remote(argv.url, argv.interval, argv.location, argv.password)
        else:
            print("URL and interval are required for remote mode.")
            sys.exit(1)
    else:
        print("Invalid mode. Choose 'local' or 'remote'.")
        sys.exit(1)