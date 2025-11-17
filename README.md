# 🛡️ RWIPE - Emergency Evidence Protection System

![House Party Protocol](houseparty.jpg)

> *"Sometimes you gotta run before you can walk."* - Tony Stark

**RWIPE** is an advanced file encryption tool designed for emergency data protection scenarios. Inspired by the "House Party Protocol" from Iron Man 3, where Tony Stark activates his entire legion of Iron Man suits in a moment of crisis, this tool provides a similar emergency response for your sensitive data.

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational_Use-FF6B6B?style=flat&logo=open-source-initiative&logoColor=white)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0-00D9FF?style=flat&logo=semver&logoColor=white)](https://github.com/shadowdevnotreal/House-Party2)
[![Encryption](https://img.shields.io/badge/encryption-AES--256-00D9FF?style=flat&logo=lock&logoColor=white)](https://github.com/shadowdevnotreal/House-Party2)

[![Buy Me A Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-Support_Development-00D9FF?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white&labelColor=1a1a1a)](https://www.buymeacoffee.com/diatasso)

</div>

---

## ⚡ Version 2.0 - What's New

This is a complete refactoring and modernization of the original [House Party Protocol](https://github.com/shadowdevnotreal/house-party-py) project, featuring:

### 🆕 New Features
- **☠️ Dead Man Switch Mode**: Activate if no "alive" signal received within grace period
- **🎨 Color-Coded Output**: Terminal colors matching project theme for better UX
- **📦 Auto-Dependency Installation**: Automatically installs missing packages
- **✅ Safety Confirmations**: Must type 'DESTROY' to confirm encryption
- **📊 Enhanced Logging**: Verbose mode with detailed operation logs
- **📈 Progress Tracking**: File count and encryption success/failure reporting

### 🔐 Security Features
- **Military-Grade Encryption**: PBKDF2 key derivation with 1,000,000 iterations + AES-256-CBC
- **Cryptographically Secure RNG**: Using `get_random_bytes()` for all random data
- **Enhanced Error Handling**: Comprehensive validation and informative error messages

### ⚙️ Operational Modes
- **🎯 Local Mode**: Manual trigger via keyboard input
- **📡 Remote Mode**: Automated trigger via HTTP endpoint monitoring
- **☠️ Dead Man Switch**: Activate if check-in missed (NEW!)

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Local Mode](#local-mode)
  - [Remote Mode](#remote-mode)
  - [Dead Man Switch Mode](#dead-man-switch-mode-new)
- [How It Works](#-how-it-works)
- [Security Details](#-security-details)
- [Comparison with Original](#-comparison-with-original)
- [Legal Warning](#-legal-warning)
- [Attribution](#-attribution)
- [Support](#-support)

---

## 🎯 Features

### Core Capabilities
- **AES-256 Encryption**: Military-grade encryption using 256-bit AES in CBC mode
- **PBKDF2 Key Derivation**: Password-based keys with 1 million iterations (NIST recommended)
- **Recursive Directory Encryption**: Encrypts all files in target directory and subdirectories
- **Three Operating Modes**:
  - **Local Mode**: Manual activation via keyboard input
  - **Remote Mode**: Automated trigger via HTTP endpoint monitoring
  - **Dead Man Switch**: Activate if no alive signal within grace period

### Security Enhancements
- ✅ Cryptographically secure random IV generation
- ✅ Proper salt generation for PBKDF2
- ✅ No key reuse (unique encryption per session)
- ✅ Password-based authentication
- ✅ Timeout protection on remote requests
- ✅ Confirmation prompts to prevent accidents

### Operational Features
- ✅ Auto-dependency installation
- ✅ Directory existence validation
- ✅ Comprehensive error handling
- ✅ Real-time progress updates with colors
- ✅ Clean exit codes for scripting
- ✅ Verbose logging mode
- ✅ File count and success/failure tracking
- ✅ Keyboard interrupt handling (Ctrl+C)

---

## 🔧 Installation

### Quick Install

```bash
git clone https://github.com/shadowdevnotreal/House-Party2.git
cd House-Party2
python3 rwipe.py --help
```

**That's it!** Dependencies auto-install on first run.

### Manual Installation

If you prefer to install dependencies manually:

```bash
pip install -r requirements.txt
```

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Internet connection (for auto-install or remote modes)

---

## 💻 Usage

### Local Mode

Perfect for scenarios where you need manual control and immediate activation.

```bash
python3 rwipe.py -d /path/to/directory -m local -p YourStrongPassword123
```

**Parameters:**
- `-d, --directory` : Target directory to encrypt (required)
- `-m, --mode` : Operating mode = `local` (required)
- `-p, --password` : Password for key derivation (required)
- `-v, --verbose` : Enable verbose logging (optional)

**Example:**
```bash
python3 rwipe.py -d /home/user/sensitive_docs -m local -p MySecurePass2024! -v
```

**Activation:**
1. Run the command
2. Review the file count warning
3. Type `DESTROY` to confirm (safety feature)
4. Press `Y` and hit Enter when ready to activate
5. All files will be encrypted immediately

**Output:**
```
🎯 Local Mode Active
Press 'Y' and Enter to start action.

> Y

⚠️  WARNING: This will encrypt 42 files in: /home/user/sensitive_docs
⚠️  This action is IRREVERSIBLE without the password!

Type 'DESTROY' to confirm: DESTROY

🔐 Starting encryption process...

✓ /home/user/sensitive_docs/file1.txt
✓ /home/user/sensitive_docs/file2.pdf
...
```

---

### Remote Mode

Ideal for remote activation scenarios where you need to trigger encryption from anywhere in the world.

```bash
python3 rwipe.py -d /path/to/directory -u https://your-server.com/trigger.txt -i 60 -m remote -p YourStrongPassword123
```

**Parameters:**
- `-d, --directory` : Target directory to encrypt (required)
- `-u, --url` : URL to monitor for trigger command (required)
- `-i, --interval` : Check interval in seconds (default: 60)
- `-m, --mode` : Operating mode = `remote` (required)
- `-p, --password` : Password for key derivation (required)
- `-v, --verbose` : Enable verbose logging (optional)

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

### Dead Man Switch Mode (NEW!)

The most advanced mode - activates encryption if you DON'T check in regularly. Perfect for scenarios where you need automatic protection if something happens to you.

```bash
python3 rwipe.py -d /path/to/directory -u https://your-server.com/alive.txt -i 30 -g 300 -m deadman -p YourStrongPassword123
```

**Parameters:**
- `-d, --directory` : Target directory to encrypt (required)
- `-u, --url` : URL to check for alive signal (required)
- `-i, --interval` : How often to check for signal in seconds (default: 60)
- `-g, --grace` : Grace period before activation in seconds (default: 300)
- `-m, --mode` : Operating mode = `deadman` (required)
- `-p, --password` : Password for key derivation (required)
- `-v, --verbose` : Enable verbose logging (optional)

**Example:**
```bash
python3 rwipe.py -d /home/user/critical_data -u https://example.com/alive.txt -i 60 -g 600 -m deadman -p MySecurePass2024!
```

**How It Works:**

1. **Setup**: Create a text file on your server that contains the word "alive"
2. **Check-In**: RWIPE checks this URL every `-i` seconds
3. **Grace Period**: If "alive" is not found, a countdown begins (-g seconds)
4. **Activation**: If no "alive" signal within grace period, encryption activates

**Dead Man Switch PHP Example:**
```php
<?php
// alive.php - You must visit this page regularly to prevent activation
session_start();

if (isset($_POST['checkin'])) {
    file_put_contents("alive.txt", "alive");
    $_SESSION['last_checkin'] = time();
    echo "Check-in successful!";
} elseif (isset($_POST['disable'])) {
    file_put_contents("alive.txt", "disabled");
    echo "Dead man switch DISABLED";
} else {
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dead Man Switch - Check In</title>
        <meta http-equiv="refresh" content="60">
    </head>
    <body>
        <h1>Dead Man Switch Control</h1>
        <p>Last check-in: <?php echo isset($_SESSION['last_checkin']) ? date('Y-m-d H:i:s', $_SESSION['last_checkin']) : 'Never'; ?></p>

        <form method="post">
            <button type="submit" name="checkin">I'M ALIVE - Check In</button>
        </form>

        <form method="post">
            <button type="submit" name="disable">DISABLE Switch</button>
        </form>
    </body>
    </html>
    <?php
}
?>
```

**Use Cases:**
- Journalist/activist protection if detained
- Whistleblower data protection
- Emergency medical situations
- High-risk travel scenarios

---

## 🔍 How It Works

### Encryption Process

1. **Dependency Check**: Auto-installs `pycryptodome` and `requests` if missing
2. **Key Derivation**: Your password is processed through PBKDF2 with a random salt and 1,000,000 iterations to create a 256-bit encryption key
3. **File Discovery**: The tool recursively walks through all files in the target directory
4. **Confirmation**: In local mode, requires typing 'DESTROY' to prevent accidents
5. **Encryption**: Each file is:
   - Read into memory
   - Padded to AES block size (16 bytes)
   - Encrypted with AES-256 in CBC mode with a unique random IV
   - Overwritten with encrypted data
6. **Completion**: Original files are now permanently encrypted and unrecoverable without the password

### Mode Comparison

| Feature | Local | Remote | Dead Man Switch |
|---------|-------|--------|-----------------|
| **Trigger** | Manual (keyboard) | URL contains "start" | URL missing "alive" |
| **Confirmation** | Required (type 'DESTROY') | Auto-activates | Auto-activates |
| **Network** | Not required | Required | Required |
| **Use Case** | Immediate control | Remote activation | Automatic protection |
| **Grace Period** | N/A | Instant | Configurable (-g) |

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
| Confirmation | None | Required (type 'DESTROY') |
| Logging | None | Optional verbose mode |
| Auto-Install | No | Yes |
| Color Output | No | Yes (theme-matched) |

---

## 📊 Comparison with Original

This project is a complete refactoring of the original [house-party-py](https://github.com/shadowdevnotreal/house-party-py) by Utku Sen.

### Major Improvements

✅ **Cryptographic Security**: Replaced weak random key generation with industry-standard PBKDF2
✅ **Triple Modes**: Added local manual trigger + dead man switch in addition to remote
✅ **Modern Code**: Updated to Python 3.10+, modern libraries, and best practices
✅ **Error Handling**: Comprehensive try-catch blocks and validation
✅ **User Experience**: Color-coded CLI interface with clear progress and status messages
✅ **Safety Features**: Confirmation prompts, file counting, success/failure tracking
✅ **Auto-Installation**: Dependencies install automatically on first run
✅ **Documentation**: Professional README with complete usage examples
✅ **Logging**: Optional verbose mode for debugging
✅ **Flexibility**: More command-line options for customization

### What Stayed the Same

- Core concept: Emergency file encryption system
- AES-256 encryption algorithm
- Recursive directory traversal
- Remote activation capability via URL monitoring
- Tony Stark's spirit of emergency protocols

---

## ⚠️ Legal Warning

### READ THIS CAREFULLY

**This tool is designed for LEGITIMATE data protection scenarios ONLY**, such as:
- Emergency protection of confidential business data from physical theft
- Protecting personal privacy in case of device seizure in authoritarian regimes
- Secure data handling in high-risk journalism or activism contexts
- Emergency response protocols for organizations handling sensitive information
- Whistleblower protection in life-threatening situations

### Important Legal Considerations

⚠️ **Obstruction of Justice**: In many jurisdictions, destroying evidence during or in anticipation of legal proceedings can result in serious criminal charges, even if you are innocent of the underlying investigation.

⚠️ **Criminal Liability**: Using this tool to destroy evidence requested by law enforcement, courts, or regulatory bodies may constitute:
- Obstruction of justice
- Tampering with evidence
- Contempt of court
- Destruction of subpoenaed materials
- Spoliation of evidence

⚠️ **Civil Consequences**: Evidence destruction can lead to adverse inference in civil litigation, meaning the court may assume the destroyed data was incriminating.

### Recommended Use Cases

✅ Protection against thieves stealing your device
✅ Personal privacy protection in travel to high-risk regions
✅ Whistleblower protection in authoritarian contexts
✅ Corporate data breach emergency response
✅ Testing and educational purposes
✅ Journalist source protection in dangerous areas
✅ Activist data protection from oppressive regimes

### DO NOT Use For

❌ Destroying evidence in criminal investigations
❌ Hiding data from legal discovery processes
❌ Avoiding lawful search warrants
❌ Tampering with evidence in any legal proceeding
❌ Violating court orders or subpoenas
❌ Illegal activities of any kind

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
- **Improvements**: Complete code modernization, enhanced cryptography, triple-mode operation, dead man switch, auto-installation, comprehensive documentation

### Inspiration
The concept and name are inspired by the iconic "House Party Protocol" scene from **Iron Man 3** (2013), where Tony Stark summons his entire legion of Iron Man suits to aid him in battle. Just as Tony had an emergency protocol to deploy all his resources, this tool serves as an emergency protocol to protect your data.

> *"J.A.R.V.I.S., you know what to do."*

---

## 💖 Support Development

If RWIPE helps protect your data, consider supporting continued development and maintenance:

<div align="center">

### ☕ Buy Me A Coffee

[![Support via Buy Me A Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-Support_Development-00D9FF?style=for-the-badge&logo=buy-me-a-coffee&logoColor=white&labelColor=1a1a1a)](https://www.buymeacoffee.com/diatasso)

**Every coffee helps fuel new features, security updates, and better documentation!**

---

### Other Ways to Support

[![Star this repo](https://img.shields.io/badge/⭐_Star_this_repo-Support_for_free-00D9FF?style=flat&labelColor=1a1a1a)](https://github.com/shadowdevnotreal/House-Party2)
[![Share on Twitter](https://img.shields.io/badge/Share_on_Twitter-Spread_the_word-00D9FF?style=flat&logo=twitter&logoColor=white&labelColor=1a1a1a)](https://twitter.com/intent/tweet?text=Check%20out%20RWIPE%20v2.0%20-%20Emergency%20Evidence%20Protection%20System%20with%20Dead%20Man%20Switch!&url=https://github.com/shadowdevnotreal/House-Party2)
[![Report Issues](https://img.shields.io/badge/Report_Issues-Help_improve-00D9FF?style=flat&logo=github&logoColor=white&labelColor=1a1a1a)](https://github.com/shadowdevnotreal/House-Party2/issues)

</div>

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

**Areas for Contribution:**
- Additional encryption modes
- GUI interface
- Mobile app versions
- Additional trigger mechanisms
- Security audits
- Documentation improvements
- Language translations

---

## 📞 Contact

**Shadow Dev**
- 💻 GitHub: [@shadowdevnotreal](https://github.com/shadowdevnotreal)
- ☕ Support: [![Buy Me A Coffee](https://img.shields.io/badge/Buy_Me_A_Coffee-diatasso-00D9FF?style=flat&logo=buy-me-a-coffee&logoColor=white)](https://www.buymeacoffee.com/diatasso)
- 📧 Issues: [Report bugs or request features](https://github.com/shadowdevnotreal/House-Party2/issues)

**Original Author - Utku Sen**
- 🌐 Website: [utkusen.com](https://utkusen.com)
- 📦 Original Repo: [house-party-py](https://github.com/shadowdevnotreal/house-party-py)

---

## 🙏 Acknowledgments

- **Utku Sen (Jani)** - For creating the original House Party Protocol concept
- **Marvel Studios / Iron Man 3** - For the inspiration and cool protocol name
- **PyCryptodome Team** - For the excellent cryptography library
- **Python Community** - For the amazing ecosystem
- **Open Source Community** - For making security tools accessible
- **All Contributors** - Thank you for improving this project

---

## 📄 License

This project maintains the spirit of open-source collaboration.

**Original Project**: Licensed under GNU General Public License v2.0

**This Refactor**: Available for educational and authorized security purposes only. Commercial use requires explicit permission.

See repository for full license details.

---

<div align="center">

---

### ⚡ Remember: With great power comes great responsibility. ⚡

*This tool is for protection, not destruction of evidence.*

**Made with ⚡ by [Shadow Dev](https://github.com/shadowdevnotreal) | Original concept by [Utku Sen](https://utkusen.com)**

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Encryption](https://img.shields.io/badge/Encryption-AES--256-00D9FF?style=flat&logo=lock&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00FF00?style=flat&logo=github-actions&logoColor=white)
![MIT License](https://img.shields.io/badge/License-Educational-FF6B6B?style=flat&logo=open-source-initiative&logoColor=white)

[![GitHub stars](https://img.shields.io/github/stars/shadowdevnotreal/House-Party2?style=social)](https://github.com/shadowdevnotreal/House-Party2)
[![GitHub forks](https://img.shields.io/github/forks/shadowdevnotreal/House-Party2?style=social)](https://github.com/shadowdevnotreal/House-Party2/fork)

</div>
