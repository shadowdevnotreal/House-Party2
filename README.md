# House-Party2
Certainly! Below is a complete README.md file for the enhanced cleanslate.py script:

# An Ultimate Evidence Wiper v1.1

## Overview
An Ultimate Evidence Wiper is a Python script designed to encrypt files in a specified directory, making them unreadable. This tool can operate in two modes: local and remote. In local mode, it waits for user input to start the encryption process. In remote mode, it continuously checks a specified URL for a command to initiate encryption.

## Features
- **AES-256 Encryption**: Uses 256-bit AES encryption for secure file encryption.
- **Key Derivation**: Derives encryption keys from a user-provided password using PBKDF2.
- **Local and Remote Modes**: Operates in either local or remote mode based on user preference.
- **Error Handling**: Provides detailed error messages and checks for directory existence.
- **Progress Logging**: Displays progress during the encryption process.

## Requirements
- Python 3.10+
- `pycryptodome` library: Install using `pip install pycryptodome`
- `requests` library: Install using `pip install requests`

## Usage

### Local Mode
1. Open your Command Prompt/Terminal.
2. Navigate to the directory containing the script.
3. Run the following command:
   ```bash
   python cleanslate.py -d /path/to/directory -m local -p your_password
Replace /path/to/directory with the path to the directory you want to encrypt.
Replace your_password with a strong password for key derivation.
Press 'Y' and Enter to start the encryption process.
Remote Mode
Open your Command Prompt/Terminal.
Navigate to the directory containing the script.
Run the following command:
python cleanslate.py -d /path/to/directory -u https://your-url.com -i 10 -m remote -p your_password
Replace /path/to/directory with the path to the directory you want to encrypt.
Replace https://your-url.com with the URL to monitor.
Replace 10 with the interval in seconds for checking the URL.
Replace your_password with a strong password for key derivation.
Example
Local Mode Example
python cleanslate.py -d /home/user/documents -m local -p mySecurePassword
Remote Mode Example
python cleanslate.py -d /home/user/documents -u https://example.com/check -i 60 -m remote -p mySecurePassword
Caution
Irreversible Process: Ensure you only run this tool on directories that you intend to encrypt, as the process is irreversible.
Secure URL: In remote mode, make sure the specified URL is secure and known only to trusted individuals.
Troubleshooting
Directory Not Found: Ensure the specified directory exists and the path is correct.
URL Issues: Check that the URL is accessible and returns the expected response.
Password Strength: Use a strong password to ensure secure key derivation.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Contact
Utku Sen (Jani) - utkusen.com

Refactored by Shadow Dev


### **Explanation:**
- **Overview**: Brief description of the tool and its purpose.
- **Features**: Highlights the key features of the script.
- **Requirements**: Lists the necessary dependencies and how to install them.
- **Usage**: Detailed instructions on how to use the script in both local and remote modes, including example commands.
- **Example**: Provides concrete examples of how to run the script.
- **Caution**: Warnings and best practices for using the tool.
- **Troubleshooting**: Common issues and their solutions.
- **License**: Specifies the licensing terms.
- **Contributing**: Guidelines for contributing to the project.
- **Contact**: Information about the original author and the refactorer.

This `README.md` file should provide a comprehensive guide for users to understand and utilize the `cleanslate.py` script effectively.
