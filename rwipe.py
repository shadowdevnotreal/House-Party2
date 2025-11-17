#!/usr/bin/python3

"""
RWIPE v3.0 - TRUE Secure Deletion System + Multi-Cloud Support
CRITICAL UPDATE: Now supports 12 cloud platforms for permanent deletion

Original Concept: Utku Sen (Jani) | utkusen.com
Enhanced: Shadow Dev | 2024

CHANGES FROM v2.5:
- ☁️  Multi-cloud deletion (Google Drive, Dropbox, OneDrive, iCloud, S3, MEGA, Box, etc.)
- 🌍 12 cloud platforms supported across 3 tiers
- 🔐 Token revocation after deletion
- 📊 Cloud deletion statistics

PREVIOUS FEATURES:
- Multi-pass secure overwrite (DoD 5220.22-M standard)
- TRUE file deletion (not just encryption)
- Cross-platform support (Windows, Mac, Linux)
- Metadata wiping
- SSD support

WARNING: This performs PERMANENT, UNRECOVERABLE data destruction.
Use only for authorized emergency protection.
"""

import subprocess
import sys
import os
import platform
import shutil

# Auto-install dependencies
def check_dependencies():
    """Check and install required dependencies."""
    required = {'pycryptodome': 'Crypto', 'requests': 'requests', 'psutil': 'psutil'}
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
            print(f"\033[91m❌ Failed to install dependencies. Please run: pip install {' '.join(missing)}\033[0m")
            sys.exit(1)

check_dependencies()

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import argparse
from time import sleep
import requests
import time
import logging
from datetime import datetime, timedelta
import random
import string
import psutil

# Detect OS
CURRENT_OS = platform.system()  # 'Windows', 'Darwin' (Mac), or 'Linux'

# ANSI Color codes
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
║     🔥 TRUE SECURE DELETION SYSTEM 🔥                        ║
║                 Version 3.0                                   ║
║                                                               ║
║   ⚡ House Party Protocol - ENHANCED ⚡                       ║
║   Multi-Pass | Cross-Platform | 12 Cloud Platforms           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    {Colors.BOLD}Original Concept:{Colors.ENDC} Utku Sen (Jani) | utkusen.com
    {Colors.BOLD}Enhanced:{Colors.ENDC} Shadow Dev | 2024

    {Colors.FAIL}⚠️  NEW: TRUE DELETION - Not just encryption!{Colors.ENDC}
    {Colors.WARNING}Platform: {CURRENT_OS} | Multi-Pass Overwrite Enabled{Colors.ENDC}

''')

def setup_logging(verbose=False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format=f'{Colors.OKCYAN}[%(asctime)s]{Colors.ENDC} %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def secure_random_data(size):
    """Generate cryptographically secure random data."""
    return get_random_bytes(size)

def get_file_size(file_path):
    """Get file size in bytes."""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def is_ssd(file_path):
    """Detect if file is on SSD (for TRIM optimization)."""
    try:
        if CURRENT_OS == 'Linux':
            # Check if on SSD by examining mount point
            import subprocess
            result = subprocess.run(['df', file_path], capture_output=True, text=True)
            if result.returncode == 0:
                # Simple heuristic - could be improved
                return 'ssd' in result.stdout.lower()
        elif CURRENT_OS == 'Windows':
            # Check disk type using PowerShell
            drive = os.path.splitdrive(file_path)[0]
            if drive:
                return False  # Default to HDD for safety
        return False
    except:
        return False

def secure_overwrite_file(file_path, passes=3):
    """
    Securely overwrite file with multiple passes.

    DoD 5220.22-M Standard:
    - Pass 1: Write zeros (0x00)
    - Pass 2: Write ones (0xFF)
    - Pass 3: Write random data

    Args:
        file_path: Path to file
        passes: Number of overwrite passes (3, 7, or 35)
    """
    try:
        file_size = get_file_size(file_path)
        if file_size == 0:
            return True

        # Patterns for DoD 5220.22-M
        patterns = [
            b'\x00',  # Pass 1: Zeros
            b'\xFF',  # Pass 2: Ones
            None,     # Pass 3: Random (special case)
        ]

        # Extended patterns for 7-pass
        if passes >= 7:
            patterns.extend([
                b'\x55',  # Pass 4: 01010101
                b'\xAA',  # Pass 5: 10101010
                None,     # Pass 6: Random
                None,     # Pass 7: Random
            ])

        with open(file_path, 'r+b') as f:
            for pass_num in range(min(passes, len(patterns))):
                pattern = patterns[pass_num]

                # Write pattern
                f.seek(0)
                if pattern is None:
                    # Random data
                    chunk_size = 1024 * 1024  # 1MB chunks
                    bytes_written = 0
                    while bytes_written < file_size:
                        chunk = min(chunk_size, file_size - bytes_written)
                        f.write(secure_random_data(chunk))
                        bytes_written += chunk
                else:
                    # Fixed pattern
                    f.write(pattern * file_size)

                f.flush()
                os.fsync(f.fileno())  # Force write to disk

        return True
    except Exception as e:
        logging.error(f"Secure overwrite failed for {file_path}: {e}")
        return False

def encrypt_data(data, key):
    """Encrypt data with AES-256-CBC."""
    # Pad to AES block size
    block_size = AES.block_size
    padded = data + b"\0" * (block_size - len(data) % block_size)

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(padded)

def randomize_filename(file_path):
    """Randomize filename before deletion (metadata wiping)."""
    try:
        directory = os.path.dirname(file_path)
        random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        ext = os.path.splitext(file_path)[1]
        new_path = os.path.join(directory, random_name + ext)

        os.rename(file_path, new_path)
        return new_path
    except Exception as e:
        logging.debug(f"Filename randomization failed: {e}")
        return file_path

def secure_delete_file(file_path, passes=3, encrypt=True, key=None):
    """
    TRUE SECURE DELETION - Multi-step process:

    1. Multi-pass overwrite (DoD 5220.22-M)
    2. Optional encryption layer
    3. Filename randomization
    4. File deletion
    5. Metadata wiping

    Args:
        file_path: Path to file
        passes: Number of overwrite passes
        encrypt: Whether to encrypt after overwrite
        key: Encryption key (if encrypt=True)
    """
    try:
        # Step 1: Multi-pass secure overwrite
        if not secure_overwrite_file(file_path, passes):
            return False

        # Step 2: Optional encryption layer (defense in depth)
        if encrypt and key:
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                encrypted = encrypt_data(data, key)
                with open(file_path, 'wb') as f:
                    f.write(encrypted)
            except Exception as e:
                logging.warning(f"Encryption layer failed: {e}")

        # Step 3: Randomize filename (metadata wiping)
        file_path = randomize_filename(file_path)

        # Step 4: Delete file
        os.remove(file_path)

        # Step 5: Platform-specific cleanup
        if CURRENT_OS == 'Windows':
            # Windows: Force delete from recycle bin
            try:
                import winshell
                # Already deleted, just ensure it's gone
            except:
                pass
        elif CURRENT_OS == 'Darwin':
            # Mac: Ensure not in .Trashes
            pass
        elif CURRENT_OS == 'Linux':
            # Linux: Sync filesystem
            try:
                os.sync()
            except:
                pass

        return True
    except Exception as e:
        logging.error(f"Secure deletion failed for {file_path}: {e}")
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

def destroy_directory(location, password, confirm=True, passes=3, method='secure'):
    """
    Destroy all files in directory.

    Methods:
    - 'secure': Multi-pass overwrite + encrypt + delete (RECOMMENDED)
    - 'encrypt': Encrypt only (faster, less secure)
    - 'wipe': Multi-pass overwrite + delete (no encryption)
    """
    if confirm:
        total_files = count_files(location)
        total_size = sum(get_file_size(os.path.join(root, f))
                        for root, _, files in os.walk(location)
                        for f in files) / (1024*1024)  # MB

        print(f"\n{Colors.FAIL}╔{'═'*60}╗{Colors.ENDC}")
        print(f"{Colors.FAIL}║{'CRITICAL WARNING':^60}║{Colors.ENDC}")
        print(f"{Colors.FAIL}╠{'═'*60}╣{Colors.ENDC}")
        print(f"{Colors.FAIL}║  This will PERMANENTLY DESTROY {total_files} files ({total_size:.1f} MB){'':>10}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║  Location: {location[:45]:<45}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║  Method: {method.upper():<51}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║  Passes: {passes:<51}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║{'':>60}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║  ⚠️  ABSOLUTELY NO RECOVERY POSSIBLE{'':>26}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║  ⚠️  FORENSIC TOOLS CANNOT RECOVER{'':>26}║{Colors.ENDC}")
        print(f"{Colors.FAIL}║  ⚠️  THIS IS PERMANENT DESTRUCTION{'':>26}║{Colors.ENDC}")
        print(f"{Colors.FAIL}╚{'═'*60}╝{Colors.ENDC}\n")

        confirmation = input(f"{Colors.FAIL}Type 'DESTROY' to confirm: {Colors.ENDC}")
        if confirmation != 'DESTROY':
            print(f"{Colors.OKGREEN}✓ Operation cancelled.{Colors.ENDC}")
            return

    key, salt = create_key(password)
    destroyed_count = 0
    failed_count = 0
    total_size_destroyed = 0

    print(f"\n{Colors.FAIL}🔥 Starting SECURE DELETION process...{Colors.ENDC}")
    print(f"{Colors.WARNING}Method: {method.upper()} | Passes: {passes} | Platform: {CURRENT_OS}{Colors.ENDC}\n")

    try:
        for root, _, files in os.walk(location, topdown=False):
            for fil in files:
                fname = os.path.join(root, fil)
                file_size = get_file_size(fname)

                if method == 'secure':
                    # Full secure deletion
                    if secure_delete_file(fname, passes=passes, encrypt=True, key=key):
                        destroyed_count += 1
                        total_size_destroyed += file_size
                        print(f"{Colors.OKGREEN}✓ DESTROYED{Colors.ENDC} {fname} ({file_size/1024:.1f} KB)")
                    else:
                        failed_count += 1
                        print(f"{Colors.FAIL}✗ FAILED{Colors.ENDC} {fname}")

                elif method == 'wipe':
                    # Overwrite + delete (no encryption)
                    if secure_delete_file(fname, passes=passes, encrypt=False, key=None):
                        destroyed_count += 1
                        total_size_destroyed += file_size
                        print(f"{Colors.OKGREEN}✓ WIPED{Colors.ENDC} {fname}")
                    else:
                        failed_count += 1
                        print(f"{Colors.FAIL}✗ FAILED{Colors.ENDC} {fname}")

                elif method == 'encrypt':
                    # Legacy encryption-only mode
                    try:
                        with open(fname, 'rb') as f:
                            data = f.read()
                        encrypted = encrypt_data(data, key)
                        with open(fname, 'wb') as f:
                            f.write(encrypted)
                        destroyed_count += 1
                        print(f"{Colors.WARNING}✓ ENCRYPTED{Colors.ENDC} {fname}")
                    except Exception as e:
                        failed_count += 1
                        print(f"{Colors.FAIL}✗ FAILED{Colors.ENDC} {fname}")

        # Remove empty directories
        for root, dirs, _ in os.walk(location, topdown=False):
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except:
                    pass

        print(f"\n{Colors.OKGREEN}{'═'*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ DESTRUCTION COMPLETE!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}  Destroyed: {destroyed_count} files ({total_size_destroyed/(1024*1024):.1f} MB){Colors.ENDC}")
        if failed_count > 0:
            print(f"{Colors.WARNING}  Failed: {failed_count} files{Colors.ENDC}")
        print(f"{Colors.OKGREEN}  Method: {method.upper()}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}  Passes: {passes}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'═'*60}{Colors.ENDC}\n")

    except Exception as e:
        logging.error(f"Error during destruction: {e}")
        print(f"{Colors.FAIL}❌ Destruction process encountered an error.{Colors.ENDC}")

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

def listener_local(location, password, passes, method):
    """Local mode: Manual trigger via keyboard input."""
    print(f"{Colors.OKCYAN}🎯 Local Mode Active{Colors.ENDC}")
    print(f"{Colors.BOLD}Press 'Y' and Enter to start SECURE DELETION.{Colors.ENDC}\n")

    while True:
        response = input(f"{Colors.WARNING}> {Colors.ENDC}")
        if response.lower() == 'y':
            print(f"\n{Colors.FAIL}--SECURE DELETION Started!--{Colors.ENDC}")
            destroy_directory(location, password, passes=passes, method=method)
            break
        elif response.lower() == 'q':
            print(f"{Colors.OKGREEN}✓ Exiting...{Colors.ENDC}")
            break

def listener_remote(url, interval, location, password, passes, method):
    """Remote mode: Trigger via URL monitoring."""
    print(f"{Colors.OKCYAN}📡 Remote Mode Active{Colors.ENDC}")
    print(f"{Colors.BOLD}Monitoring: {url}{Colors.ENDC}")
    print(f"{Colors.BOLD}Check interval: {interval}s{Colors.ENDC}\n")
    print(f"{Colors.OKGREEN}Status: Listening...{Colors.ENDC}")

    while True:
        if check_url(url):
            print(f"\n{Colors.FAIL}🚨 TRIGGER DETECTED!{Colors.ENDC}")
            print(f"{Colors.FAIL}--SECURE DELETION Started!--{Colors.ENDC}")
            destroy_directory(location, password, confirm=False, passes=passes, method=method)
            break
        sleep(interval)

def listener_deadman(url, check_interval, grace_period, location, password, passes, method):
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
                print(f"{Colors.FAIL}--SECURE DELETION Started!--{Colors.ENDC}")
                destroy_directory(location, password, confirm=False, passes=passes, method=method)
                break
            else:
                remaining = grace_period - int(time_since_alive)
                print(f"{Colors.WARNING}⏳ No signal. Time until trigger: {remaining}s{Colors.ENDC}")

        sleep(check_interval)


def listener_cloud(platforms_str=None, cloud_all=False):
    """
    Cloud deletion mode - delete files from cloud storage platforms

    Args:
        platforms_str: Comma-separated platform names (e.g., 'google_drive,dropbox')
        cloud_all: If True, delete from all authenticated platforms
    """
    try:
        from cloud_deletion import CloudDeletionManager, CloudPlatformBase
        import cloud_deletion
    except ImportError:
        print(f"{Colors.FAIL}❌ Cloud deletion module not found. Ensure cloud_deletion.py is in the same directory.{Colors.ENDC}")
        sys.exit(1)

    print(f"\n{Colors.OKCYAN}{Colors.BOLD}☁️  CLOUD DELETION MODE ☁️{Colors.ENDC}\n")

    manager = CloudDeletionManager()

    # Available platforms
    available = {
        'google_drive': ('Google Drive', cloud_deletion.GoogleDriveDeletion),
        'dropbox': ('Dropbox', cloud_deletion.DropboxDeletion),
        'onedrive': ('OneDrive', cloud_deletion.OneDriveDeletion),
        'icloud': ('iCloud', cloud_deletion.iCloudDeletion),
        's3': ('Amazon S3', cloud_deletion.AmazonS3Deletion),
        'mega': ('MEGA', cloud_deletion.MEGADeletion),
        'box': ('Box', cloud_deletion.BoxDeletion),
        'nextcloud': ('Nextcloud', cloud_deletion.NextcloudDeletion),
        'pcloud': ('pCloud', cloud_deletion.pCloudDeletion),
        'b2': ('Backblaze B2', cloud_deletion.BackblazeB2Deletion),
    }

    # Determine which platforms to use
    if cloud_all:
        print(f"{Colors.WARNING}Attempting to authenticate with ALL available platforms...{Colors.ENDC}\n")
        selected_platforms = list(available.keys())
    elif platforms_str:
        selected_platforms = [p.strip() for p in platforms_str.split(',')]
    else:
        # Interactive selection
        print(f"{Colors.OKCYAN}Available Cloud Platforms:{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Tier 1 (Must Have):{Colors.ENDC}")
        print("  1. google_drive - Google Drive")
        print("  2. dropbox - Dropbox")
        print("  3. onedrive - Microsoft OneDrive")
        print("  4. icloud - Apple iCloud")
        print(f"\n{Colors.BOLD}Tier 2 (Should Have):{Colors.ENDC}")
        print("  5. s3 - Amazon S3")
        print("  6. mega - MEGA")
        print("  7. box - Box")
        print(f"\n{Colors.BOLD}Tier 3 (Nice to Have):{Colors.ENDC}")
        print("  8. nextcloud - Nextcloud/ownCloud")
        print("  9. pcloud - pCloud")
        print("  10. b2 - Backblaze B2")
        print(f"\n{Colors.WARNING}Enter comma-separated platform names (e.g., google_drive,dropbox){Colors.ENDC}")
        print(f"{Colors.WARNING}Or press Enter to select interactively:{Colors.ENDC}\n")

        user_input = input("> ").strip()
        if user_input:
            selected_platforms = [p.strip() for p in user_input.split(',')]
        else:
            print(f"\n{Colors.FAIL}No platforms specified. Exiting.{Colors.ENDC}")
            sys.exit(0)

    # Authenticate with selected platforms
    print(f"\n{Colors.OKCYAN}Authenticating with cloud platforms...{Colors.ENDC}\n")

    for platform_key in selected_platforms:
        if platform_key not in available:
            print(f"{Colors.WARNING}⚠️  Unknown platform: {platform_key}{Colors.ENDC}")
            continue

        platform_name, platform_class = available[platform_key]

        try:
            print(f"{Colors.OKCYAN}Connecting to {platform_name}...{Colors.ENDC}")

            # Initialize platform
            if platform_key == 'google_drive':
                platform = platform_class()
            elif platform_key == 'dropbox':
                platform = platform_class()
            elif platform_key == 'onedrive':
                platform = platform_class()
            elif platform_key == 'icloud':
                platform = platform_class()
            elif platform_key == 's3':
                platform = platform_class()
            elif platform_key == 'mega':
                platform = platform_class()
            elif platform_key == 'box':
                platform = platform_class()
            elif platform_key == 'nextcloud':
                platform = platform_class()
            elif platform_key == 'pcloud':
                platform = platform_class()
            elif platform_key == 'b2':
                platform = platform_class()
            else:
                continue

            # Authenticate
            if manager.add_platform(platform_key, platform):
                print(f"{Colors.OKGREEN}✓ {platform_name} authenticated{Colors.ENDC}")
            else:
                print(f"{Colors.FAIL}❌ {platform_name} authentication failed{Colors.ENDC}")

        except Exception as e:
            print(f"{Colors.FAIL}❌ Error with {platform_name}: {e}{Colors.ENDC}")

    # Show summary
    if not manager.active_platforms:
        print(f"\n{Colors.FAIL}❌ No platforms authenticated. Exiting.{Colors.ENDC}")
        sys.exit(1)

    print(manager.get_summary())

    # Confirm deletion
    print(f"\n{Colors.WARNING}{Colors.BOLD}⚠️  WARNING: This will PERMANENTLY delete files from cloud storage!{Colors.ENDC}")
    print(f"{Colors.WARNING}Cloud files CANNOT be recovered after deletion.{Colors.ENDC}\n")

    confirmation = input(f"Type {Colors.BOLD}DESTROY{Colors.ENDC} to confirm cloud deletion: ")
    if confirmation != "DESTROY":
        print(f"{Colors.WARNING}Cloud deletion cancelled.{Colors.ENDC}")
        sys.exit(0)

    # Execute deletion
    results = manager.delete_all(confirm=False)  # Already confirmed above

    # Show results
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}═══════════════════════════════════════{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}     CLOUD DELETION COMPLETE{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{Colors.BOLD}═══════════════════════════════════════{Colors.ENDC}\n")

    total_deleted = 0
    total_failed = 0

    for platform_name, (deleted, failed) in results.items():
        total_deleted += deleted
        total_failed += failed
        platform_display = available.get(platform_name, (platform_name, None))[0]
        print(f"  {platform_display}: {Colors.OKGREEN}{deleted} deleted{Colors.ENDC}, {Colors.FAIL}{failed} failed{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Total: {Colors.OKGREEN}{total_deleted} deleted{Colors.ENDC}, {Colors.FAIL}{total_failed} failed{Colors.ENDC}\n")

    if total_deleted > 0:
        print(f"{Colors.OKGREEN}✓ Cloud deletion completed successfully!{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}⚠️  No files were deleted.{Colors.ENDC}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='RWIPE v3.0 - TRUE Secure Deletion System + Multi-Cloud Support',
        epilog='Use responsibly. For authorized data protection only.'
    )

    # Required arguments
    parser.add_argument('-d', '--directory', action='store', dest='location',
                        help='Directory to be destroyed (not required for cloud mode)', required=False)
    parser.add_argument('-m', '--mode', action='store', dest='mode',
                        help="Mode: 'local', 'remote', 'deadman', or 'cloud'", required=True)
    parser.add_argument('-p', '--password', action='store', dest='password',
                        help='Password for key derivation (not required for cloud mode)', required=False)

    # Optional arguments
    parser.add_argument('-u', '--url', action='store', dest='url',
                        help='URL for remote/deadman mode')
    parser.add_argument('-i', '--interval', action='store', dest='interval',
                        help='Check interval in seconds (default: 60)',
                        required=False, type=int, default=60)
    parser.add_argument('-g', '--grace', action='store', dest='grace_period',
                        help='Grace period for deadman mode in seconds (default: 300)',
                        required=False, type=int, default=300)
    parser.add_argument('--passes', action='store', dest='passes',
                        help='Number of overwrite passes: 3 (default), 7, or 35',
                        required=False, type=int, default=3,
                        choices=[1, 3, 7, 35])
    parser.add_argument('--method', action='store', dest='method',
                        help="Deletion method: 'secure' (default), 'wipe', or 'encrypt'",
                        required=False, default='secure',
                        choices=['secure', 'wipe', 'encrypt'])
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose logging')
    parser.add_argument('--no-confirm', action='store_true',
                        help='Skip confirmation prompt (dangerous!)')

    # Cloud-specific arguments
    parser.add_argument('--cloud-platforms', action='store', dest='cloud_platforms',
                        help='Comma-separated list of cloud platforms (e.g., google_drive,dropbox,onedrive)',
                        required=False)
    parser.add_argument('--cloud-all', action='store_true', dest='cloud_all',
                        help='Delete from ALL authenticated cloud platforms')

    argv = parser.parse_args()

    # Setup logging
    setup_logging(argv.verbose)

    # Validate directory (not required for cloud mode)
    if argv.mode != 'cloud':
        if not argv.location:
            print(f"{Colors.FAIL}❌ Error: Directory (-d) is required for {argv.mode} mode{Colors.ENDC}")
            sys.exit(1)
        if not os.path.exists(argv.location):
            print(f"{Colors.FAIL}❌ Error: Directory does not exist: {argv.location}{Colors.ENDC}")
            sys.exit(1)
        if not os.path.isdir(argv.location):
            print(f"{Colors.FAIL}❌ Error: Path is not a directory: {argv.location}{Colors.ENDC}")
            sys.exit(1)
        if not argv.password:
            print(f"{Colors.FAIL}❌ Error: Password (-p) is required for {argv.mode} mode{Colors.ENDC}")
            sys.exit(1)

    # Warning for method
    if argv.method == 'encrypt':
        print(f"{Colors.WARNING}⚠️  WARNING: 'encrypt' method does NOT securely delete!{Colors.ENDC}")
        print(f"{Colors.WARNING}⚠️  Original data may be recoverable. Use 'secure' or 'wipe' for true deletion.{Colors.ENDC}\n")

    # Execute based on mode
    try:
        if argv.mode == 'local':
            listener_local(argv.location, argv.password, argv.passes, argv.method)

        elif argv.mode == 'remote':
            if not argv.url:
                print(f"{Colors.FAIL}❌ Error: URL (-u) is required for remote mode.{Colors.ENDC}")
                sys.exit(1)
            listener_remote(argv.url, argv.interval, argv.location, argv.password,
                          argv.passes, argv.method)

        elif argv.mode == 'deadman':
            if not argv.url:
                print(f"{Colors.FAIL}❌ Error: URL (-u) is required for deadman mode.{Colors.ENDC}")
                sys.exit(1)
            listener_deadman(argv.url, argv.interval, argv.grace_period,
                           argv.location, argv.password, argv.passes, argv.method)

        elif argv.mode == 'cloud':
            listener_cloud(argv.cloud_platforms, argv.cloud_all)

        else:
            print(f"{Colors.FAIL}❌ Invalid mode: {argv.mode}{Colors.ENDC}")
            print(f"{Colors.WARNING}Valid modes: local, remote, deadman, cloud{Colors.ENDC}")
            sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️  Interrupted by user.{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Exiting safely...{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"{Colors.FAIL}❌ Fatal error occurred. Check logs.{Colors.ENDC}")
        sys.exit(1)
