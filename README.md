# 🛡️ RWIPE - Emergency Evidence Protection System

![House Party Protocol](https://via.placeholder.com/800x400/1a1a1a/00ff00?text=House+Party+Protocol+-+Add+Iron+Man+3+Image+Here)

> *"Sometimes you gotta run before you can walk."* - Tony Stark

**RWIPE** is an advanced file encryption tool designed for emergency data protection scenarios. Inspired by the "House Party Protocol" from Iron Man 3, where Tony Stark activates his entire legion of Iron Man suits in a moment of crisis, this tool provides a similar emergency response for your sensitive data.

## ⚡ Version 2.0 - What's New

This is a complete refactoring and modernization of the original [House Party Protocol](https://github.com/shadowdevnotreal/house-party-py) project, featuring:

- **🔐 Military-Grade Encryption**: PBKDF2 key derivation with 1,000,000 iterations + AES-256-CBC
- **🎯 Dual Operation Modes**: Local manual trigger OR remote command-and-control
- **🛡️ Enhanced Security**: Cryptographically secure random number generation
- **⚙️ Better Error Handling**: Comprehensive validation and informative error messages
- **🚀 Modern Architecture**: Updated dependencies and Python 3.10+ support
- **📦 Improved UX**: Clear status messages and progress tracking

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Local Mode](#local-mode)
  - [Remote Mode](#remote-mode)
- [How It Works](#-how-it-works)
- [Security Details](#-security-details)
- [Comparison with Original](#-comparison-with-original)
- [Legal Warning](#-legal-warning)
- [Attribution](#-attribution)
- [License](#-license)

---

## 🎯 Features

### Core Capabilities
- **AES-256 Encryption**: Military-grade encryption using 256-bit AES in CBC mode
- **PBKDF2 Key Derivation**: Password-based keys with 1 million iterations (NIST recommended)
- **Recursive Directory Encryption**: Encrypts all files in target directory and subdirectories
- **Two Operating Modes**:
  - **Local Mode**: Manual activation via keyboard input
  - **Remote Mode**: Automated trigger via HTTP endpoint monitoring

### Security Enhancements
- ✅ Cryptographically secure random IV generation
- ✅ Proper salt generation for PBKDF2
- ✅ No key reuse (unique encryption per session)
- ✅ Password-based authentication
- ✅ Timeout protection on remote requests

### Operational Features
- ✅ Directory existence validation
- ✅ Comprehensive error handling
- ✅ Real-time progress updates
- ✅ Clean exit codes for scripting
- ✅ Detailed help documentation

---

## 🔧 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Install Dependencies

```bash
pip install pycryptodome requests
```

### Download

```bash
git clone https://github.com/shadowdevnotreal/House-Party2.git
cd House-Party2
chmod +x rwipe.py
```

---

## 💻 Usage

### Local Mode

Perfect for scenarios where you need manual control and immediate activation.

```bash
python3 rwipe.py -d /path/to/directory -m local -p YourStrongPassword123
```

**Parameters:**
- `-d` : Target directory to encrypt (required)
- `-m` : Operating mode = `local` (required)
- `-p` : Password for key derivation (required)

**Example:**
```bash
python3 rwipe.py -d /home/user/sensitive_docs -m local -p MySecurePass2024!
```

**Activation:**
1. Run the command
2. Press `Y` and hit Enter when ready to activate
3. All files will be encrypted immediately

---

### Remote Mode

Ideal for remote activation scenarios where you need to trigger encryption from anywhere in the world.

```bash
python3 rwipe.py -d /path/to/directory -u https://your-server.com/trigger.txt -i 60 -m remote -p YourStrongPassword123
```

**Parameters:**
- `-d` : Target directory to encrypt (required)
- `-u` : URL to monitor for trigger command (required for remote)
- `-i` : Check interval in seconds (required for remote)
- `-m` : Operating mode = `remote` (required)
- `-p` : Password for key derivation (required)

**Example:**
```bash
python3 rwipe.py -d /home/user/documents -u https://example.com/command.txt -i 30 -m remote -p MySecurePass2024!
```

**Remote Trigger Setup:**

Create a simple text file on your web server (`trigger.txt`) that initially contains nothing or any text without "start". When you want to activate the protocol, update the file to contain the word "start".

**Simple PHP Example:**
```php
<?php
// trigger.php
$password = "your_secure_password";

if (isset($_POST["password"]) && $_POST["password"] === $password) {
    file_put_contents("trigger.txt", "start");
    echo "Protocol Activated";
} else {
    echo '<form method="post">
            Password: <input type="password" name="password">
            <input type="submit" value="Activate Protocol">
          </form>';
}
?>
```

---

## 🔍 How It Works

### Encryption Process

1. **Key Derivation**: Your password is processed through PBKDF2 with a random salt and 1,000,000 iterations to create a 256-bit encryption key
2. **File Discovery**: The tool recursively walks through all files in the target directory
3. **Encryption**: Each file is:
   - Read into memory
   - Padded to AES block size (16 bytes)
   - Encrypted with AES-256 in CBC mode with a unique random IV
   - Overwritten with encrypted data
4. **Completion**: Original files are now permanently encrypted and unrecoverable without the password

### Mode Differences

**Local Mode:**
- Waits for user input ('Y') before activation
- Immediate execution
- No network dependencies

**Remote Mode:**
- Continuously polls specified URL at defined intervals
- Activates when URL returns HTTP 200 and contains "start"
- Can be triggered remotely from anywhere

---

## 🔒 Security Details

### Cryptographic Specifications

| Component | Specification |
|-----------|--------------|
| **Encryption Algorithm** | AES-256-CBC |
| **Key Derivation** | PBKDF2-HMAC-SHA256 |
| **KDF Iterations** | 1,000,000 |
| **Key Length** | 256 bits (32 bytes) |
| **Salt Length** | 128 bits (16 bytes) |
| **IV Generation** | Cryptographically secure PRNG |
| **Padding Scheme** | Null byte padding to block size |

### Security Improvements Over Original

| Feature | Original v1.0 | RWIPE v2.0 |
|---------|---------------|------------|
| Key Generation | Random strings | PBKDF2 (1M iterations) |
| Randomness Source | `random.choice()` | `get_random_bytes()` |
| Key Strength | Weak alphanumeric | Cryptographic hash |
| Error Handling | Minimal | Comprehensive |
| Input Validation | None | Full validation |
| HTTP Library | urllib | requests (with timeout) |

---

## 📊 Comparison with Original

This project is a complete refactoring of the original [house-party-py](https://github.com/shadowdevnotreal/house-party-py) by Utku Sen.

### Major Improvements

✅ **Cryptographic Security**: Replaced weak random key generation with industry-standard PBKDF2
✅ **Dual Modes**: Added local manual trigger mode in addition to remote
✅ **Modern Code**: Updated to Python 3.10+, modern libraries, and best practices
✅ **Error Handling**: Comprehensive try-catch blocks and validation
✅ **User Experience**: Better CLI interface with clear progress and status messages
✅ **Documentation**: Professional README with complete usage examples

### What Stayed the Same

- Core concept: Emergency file encryption system
- AES-256 encryption algorithm
- Recursive directory traversal
- Remote activation capability via URL monitoring

---

## ⚠️ Legal Warning

### READ THIS CAREFULLY

**This tool is designed for LEGITIMATE data protection scenarios ONLY**, such as:
- Emergency protection of confidential business data from physical theft
- Protecting personal privacy in case of device seizure in authoritarian regimes
- Secure data handling in high-risk journalism or activism contexts
- Emergency response protocols for organizations handling sensitive information

### Important Legal Considerations

⚠️ **Obstruction of Justice**: In many jurisdictions, destroying evidence during or in anticipation of legal proceedings can result in serious criminal charges, even if you are innocent of the underlying investigation.

⚠️ **Criminal Liability**: Using this tool to destroy evidence requested by law enforcement, courts, or regulatory bodies may constitute:
- Obstruction of justice
- Tampering with evidence
- Contempt of court
- Destruction of subpoenaed materials

⚠️ **Civil Consequences**: Evidence destruction can lead to adverse inference in civil litigation, meaning the court may assume the destroyed data was incriminating.

### Recommended Use Cases

✅ Protection against thieves stealing your device
✅ Personal privacy protection in travel to high-risk regions
✅ Whistleblower protection in authoritarian contexts
✅ Corporate data breach emergency response
✅ Testing and educational purposes

### DO NOT Use For

❌ Destroying evidence in criminal investigations
❌ Hiding data from legal discovery processes
❌ Avoiding lawful search warrants
❌ Tampering with evidence in any legal proceeding

**USE AT YOUR OWN RISK. The authors are not responsible for any legal consequences of using this tool.**

---

## 🎖️ Attribution

### Original Project
**House Party Protocol (Python Edition)**
- **Author**: Utku Sen (Jani)
- **Website**: [utkusen.com](https://utkusen.com)
- **Repository**: [house-party-py](https://github.com/shadowdevnotreal/house-party-py)
- **Inspiration**: Iron Man 3 (2013) - House Party Protocol scene
- **Original Version**: 1.0

### This Refactor
**RWIPE v2.0**
- **Refactored & Enhanced By**: Shadow Dev
- **Year**: 2024
- **Improvements**: Complete code modernization, enhanced cryptography, dual-mode operation, comprehensive documentation

### Inspiration
The concept and name are inspired by the iconic "House Party Protocol" scene from **Iron Man 3** (2013), where Tony Stark summons his entire legion of Iron Man suits to aid him in battle. Just as Tony had an emergency protocol to deploy all his resources, this tool serves as an emergency protocol to protect your data.

> *"J.A.R.V.I.S., you know what to do."*

---

## 📄 License

This project maintains the spirit of open-source collaboration.

**Original Project**: Licensed under GNU General Public License v2.0

**This Refactor**: Available for educational and authorized security purposes only. Commercial use requires explicit permission.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📞 Contact

**Shadow Dev**
- GitHub: [@shadowdevnotreal](https://github.com/shadowdevnotreal)

**Original Author - Utku Sen**
- Website: [utkusen.com](https://utkusen.com)

---

## 🙏 Acknowledgments

- **Utku Sen (Jani)** - For creating the original House Party Protocol concept
- **Marvel Studios / Iron Man 3** - For the inspiration and cool protocol name
- **PyCryptodome Team** - For the excellent cryptography library
- The open-source security community

---

<div align="center">

**Remember: With great power comes great responsibility.**

*This tool is for protection, not destruction of evidence.*

Made with ⚡ by Shadow Dev | Original concept by Utku Sen

</div>
