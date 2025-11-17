# Contributing to RWIPE

Thank you for your interest in contributing to RWIPE - Emergency Evidence Protection System. This project saves lives by protecting journalists, whistleblowers, and human rights defenders.

## 🎯 Mission

Every contribution to RWIPE helps protect people who risk their lives exposing truth and fighting for justice.

---

## 🚨 Before You Contribute

### Understanding the Purpose

RWIPE is designed for **PERMANENT, UNRECOVERABLE** data destruction in emergency situations. This is not a backup tool, not a temporary encryption tool - it's a last-resort protection mechanism for people in danger.

**Key Principles:**
1. **Safety First:** Changes must not compromise data destruction reliability
2. **Simplicity:** Emergency tools must be simple to use under stress
3. **No Recovery:** Any "decrypt" or "recover" features will be rejected
4. **Legal Use:** All features must support legal, authorized use only

---

## 📋 Ways to Contribute

### 1. Code Contributions

#### Areas for Contribution:
- 🌐 **Cloud Storage Integration** (Google Drive, Dropbox, OneDrive destruction)
- 📱 **Mobile Apps** (iOS, Android)
- 🔧 **Hardware Integration** (USB panic buttons, NFC triggers)
- 🌍 **Internationalization** (Translations for global users)
- 🧪 **Testing** (Unit tests, integration tests)
- 📊 **Monitoring** (Better status reporting, logs)
- 🎨 **UI/UX** (Web GUI improvements)

#### What We DON'T Want:
- ❌ Decryption features
- ❌ Data recovery tools
- ❌ "Undo" functionality
- ❌ Features that reduce destruction effectiveness
- ❌ Telemetry or analytics (privacy violation)

### 2. Documentation

- 📚 **Tutorials** (How-to guides for specific scenarios)
- 🌍 **Translations** (README, SECURITY.md in other languages)
- 📖 **Use Cases** (Real-world deployment examples)
- 🎓 **Training Materials** (For news organizations, NGOs)

### 3. Security

- 🔒 **Security Audits** (Professional security reviews)
- 🐛 **Bug Reports** (Security vulnerabilities)
- 🧪 **Penetration Testing** (Authorized testing only)
- 📋 **Threat Modeling** (New attack vectors)

### 4. Community

- 💬 **Support** (Help users in issues/discussions)
- 📢 **Advocacy** (Share with journalists, activists)
- 🎓 **Training** (Teach responsible use)
- 📰 **Articles** (Write about use cases, success stories)

---

## 🔧 Development Setup

### Prerequisites
```bash
Python 3.10+
pip
git
```

### Setup
```bash
# Clone repository
git clone https://github.com/shadowdevnotreal/House-Party2.git
cd House-Party2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests (when available)
python -m pytest tests/
```

### Testing Your Changes
```bash
# Test on dummy data ONLY
mkdir test_dir
echo "test file" > test_dir/test.txt

# Test local mode
python3 rwipe.py -d test_dir -m local -p testpassword123

# Test web GUI
python3 rwipe_web.py
# Visit: http://localhost:5000
```

---

## 📝 Pull Request Process

### 1. Fork & Branch
```bash
# Fork repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/House-Party2.git
cd House-Party2

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, documented code
- Follow existing code style
- Add tests if applicable
- Update documentation

### 3. Commit
```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add [feature]: Brief description

Detailed explanation of what changed and why.

Addresses #issue_number (if applicable)"
```

### 4. Push & PR
```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Fill in PR template
```

### 5. PR Review
- Respond to feedback
- Make requested changes
- Be patient - this is critical security software

---

## 📜 Code Style

### Python Style
- **PEP 8** compliant
- **Type hints** where practical
- **Docstrings** for all functions
- **Comments** for complex logic

### Example:
```python
def encrypt_file(file_path: str, key: bytes) -> bool:
    """
    Encrypt a single file with AES-256-CBC.

    Args:
        file_path: Absolute path to file
        key: 256-bit encryption key

    Returns:
        True if successful, False otherwise

    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If no write permission
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        return False
```

---

## 🧪 Testing Guidelines

### What to Test
- ✅ Encryption works on various file types
- ✅ Dead man switch activates correctly
- ✅ Remote triggers work
- ✅ Error handling (missing directories, permissions, etc.)
- ✅ Web GUI functionality
- ✅ Password validation

### What NOT to Test on Real Data
- ❌ NEVER test on real sensitive data
- ❌ NEVER test on production systems
- ❌ NEVER test on backup-less systems

### Test Data
```bash
# Create test directory
mkdir test_data
cd test_data

# Create various test files
echo "text file" > test.txt
dd if=/dev/urandom of=binary.bin bs=1M count=1
echo '{"key": "value"}' > data.json

# Run tests
cd ..
python3 rwipe.py -d test_data -m local -p TestPassword123!
```

---

## 🔒 Security Considerations

### Responsible Disclosure
If you find a security vulnerability:

1. **DO NOT** create a public issue
2. **DO** email security details to: [Create private security advisory on GitHub]
3. **DO** allow 90 days for patch before disclosure
4. **DO** provide:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

### Security Review Checklist
- [ ] No unintended data leakage
- [ ] No weak cryptography
- [ ] No bypass mechanisms
- [ ] No credential storage
- [ ] No telemetry/tracking
- [ ] Proper error handling
- [ ] Input validation
- [ ] No SQL injection (if adding database)
- [ ] No command injection
- [ ] No XSS (in web GUI)

---

## 📋 Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `security`: Security fix

### Example:
```
feat: Add Google Drive integration for cloud destruction

Implements Google Drive API integration to allow permanent
deletion of files from cloud storage in emergency situations.

Features:
- OAuth 2.0 authentication
- Recursive folder deletion
- Progress tracking
- Error handling for network issues

Addresses #42
```

---

## 🌍 Internationalization

### Adding Translations

1. Create language file: `i18n/[language_code].json`
2. Translate all strings
3. Update `rwipe.py` to load translations
4. Test thoroughly

### Example Translation File:
```json
{
  "warning_permanent": "ADVERTENCIA: Esta herramienta destruye datos PERMANENTEMENTE",
  "confirm_destroy": "¿Está seguro? Escriba DESTRUIR para confirmar",
  "encryption_started": "Cifrado iniciado...",
  "encryption_complete": "¡Cifrado completado!",
  "files_encrypted": "archivos cifrados"
}
```

---

## 📞 Getting Help

### Resources:
- **Issues:** [GitHub Issues](https://github.com/shadowdevnotreal/House-Party2/issues)
- **Discussions:** [GitHub Discussions](https://github.com/shadowdevnotreal/House-Party2/discussions)
- **Security:** [SECURITY.md](SECURITY.md)
- **Documentation:** [README.md](README.md)

### Questions?
- Check existing issues first
- Search discussions
- If new question, create an issue with:
  - Clear title
  - Detailed description
  - Steps to reproduce (if bug)
  - Expected vs actual behavior
  - System information (OS, Python version)

---

## 🙏 Recognition

### Contributors
All contributors will be recognized in:
- README.md acknowledgments section
- GitHub contributors page
- Release notes

### Significant Contributions
Major features or security improvements will be highlighted in release announcements.

---

## 📄 License

By contributing to RWIPE, you agree that your contributions will be licensed under the GNU General Public License v2.0.

---

## ⚡ Final Thoughts

Every line of code you contribute helps protect:
- 🗞️ Journalists exposing corruption
- 📢 Whistleblowers revealing wrongdoing
- ✊ Activists fighting oppression
- 🛡️ Human rights defenders protecting the vulnerable

**Your contribution saves lives.**

Thank you for making the world safer for those who speak truth to power.

---

**Made with ⚡ by Shadow Dev | Original concept by Utku Sen**

*"With great power comes great responsibility."*
