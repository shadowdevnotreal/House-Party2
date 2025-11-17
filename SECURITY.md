# Security Policy

## ⚠️ Critical Security Notice

**RWIPE is designed for PERMANENT, UNRECOVERABLE data destruction.**

This tool is specifically created for legitimate emergency data protection scenarios:
- 🗞️ **Journalists** protecting confidential sources
- 📢 **Whistleblowers** safeguarding evidence before exposure
- ✊ **Activists** in authoritarian regimes protecting contacts
- 🛡️ **Human rights workers** securing sensitive information

## 🔒 Security Features

### Encryption Specifications
- **Algorithm:** AES-256-CBC
- **Key Derivation:** PBKDF2-HMAC-SHA256
- **Iterations:** 1,000,000 (NIST recommended)
- **Salt:** 128-bit cryptographically secure random
- **IV:** Unique per file, cryptographically secure random

### Data Permanence
**THIS TOOL MAKES DATA PERMANENTLY UNRECOVERABLE.**

Files encrypted with RWIPE cannot be decrypted because:
1. Random salt generated per session (not stored)
2. Encryption key derived from password + salt
3. Without exact salt, decryption is cryptographically impossible
4. This is BY DESIGN for maximum protection

### Cloud Deletion Security (NEW in v3.0)

**Cloud deletion operates differently from local file deletion:**

#### What Cloud Deletion Does:
✅ **Permanent Deletion** - Files removed from cloud storage (bypasses trash)
✅ **Token Revocation** - OAuth tokens automatically revoked after deletion
✅ **Multi-Platform** - Delete from 12 cloud platforms simultaneously
✅ **Audit Trail** - Statistics show deleted/failed counts per platform

#### What Cloud Deletion Does NOT Do:
❌ **Multi-Pass Overwrite** - Cloud providers control physical storage
❌ **Metadata Wiping** - Cloud providers maintain internal logs
❌ **Physical Destruction** - Data may remain in cloud provider backups

#### Cloud Security Considerations:

1. **Cloud Provider Backups**
   - Cloud providers may retain backup copies (disaster recovery)
   - Deletion removes files from YOUR account, not provider infrastructure
   - Consult cloud provider's data retention policy

2. **Authentication Security**
   - OAuth 2.0 tokens stored temporarily
   - Tokens revoked immediately after deletion
   - Credential files protected by `.gitignore`

3. **Network Security**
   - All authentication uses HTTPS
   - API calls encrypted in transit
   - No credentials stored in code

4. **Supported Authentication Methods:**
   - **Google Drive**: OAuth 2.0 (Google Cloud Console)
   - **Dropbox**: Access token (Dropbox App Console)
   - **OneDrive**: Microsoft Graph API (Azure App Registration)
   - **iCloud**: Username/password + 2FA
   - **S3**: AWS credentials (IAM keys)
   - **MEGA**: Username/password
   - **Box**: OAuth 2.0 (Box Developer Console)
   - **Nextcloud**: WebDAV (username/password)
   - **pCloud**: Username/password
   - **Backblaze B2**: Application keys

#### Environment Variables:
Sensitive credentials should be set via environment variables, NOT hardcoded:
```bash
export DROPBOX_ACCESS_TOKEN="..."
export ICLOUD_USERNAME="..."
export MEGA_EMAIL="..."
```

#### Credential Files (.gitignore protected):
- `google_credentials.json`
- `token_google.json`
- `onedrive_credentials.json`
- `box_config.json`
- ALL credential files automatically excluded from git

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

### DO:
✅ Email: [Create issue on GitHub](https://github.com/shadowdevnotreal/House-Party2/issues) with tag `security`
✅ Provide detailed description
✅ Include steps to reproduce (if applicable)
✅ Allow 90 days for patch before public disclosure

### DON'T:
❌ Publicly disclose before patch
❌ Exploit vulnerabilities
❌ Use for malicious purposes

## 🛡️ Responsible Use

### Legitimate Use Cases
✅ Protecting sources from oppressive governments
✅ Emergency privacy protection during travel
✅ Whistleblower evidence protection
✅ Activist data security
✅ Testing and educational purposes

### Prohibited Use
❌ Destroying evidence in criminal investigations
❌ Avoiding lawful discovery processes
❌ Violating court orders or subpoenas
❌ Any illegal activity

## 📋 Security Best Practices

### Before Using RWIPE:

1. **Understand Permanence**
   - Data encrypted with RWIPE is GONE FOREVER
   - No decryption is possible
   - No recovery tools exist

2. **Test First**
   - Use on test files first
   - Verify you understand the process
   - Ensure you're targeting correct directory

3. **Backup Critical Data**
   - If you might need data later, DON'T use RWIPE
   - This is for data you want PERMANENTLY DESTROYED

4. **Strong Password**
   - Use unique, strong password
   - Don't reuse passwords
   - Longer = better (20+ characters recommended)

5. **Verify Target**
   - Double-check directory path
   - Ensure no important files in target
   - Remember: PERMANENT destruction

## 🔐 Cryptographic Assurance

### Why Data is Unrecoverable:

The mathematical impossibility of recovery without the salt:

```
Key = PBKDF2(password, random_salt, 1000000 iterations)
```

- `random_salt` is generated per session
- Salt is NOT stored anywhere
- Without salt, trying all possible salts would take:
  - 2^128 possibilities (128-bit salt)
  - At 1 billion tries/second: 10^28 years
  - Age of universe: 13.8 billion years
  - **Conclusion: Cryptographically impossible**

This is not a bug - it's a feature for maximum protection.

## 🌍 Threat Model

RWIPE protects against:
✅ Physical device seizure
✅ Legal discovery orders
✅ Forensic analysis
✅ Data recovery tools
✅ Brute force attacks (with strong password)

RWIPE does NOT protect against:
❌ Keyloggers (capturing password)
❌ Live RAM analysis (while running)
❌ Backup systems (cloud, external drives)
❌ Compromised systems (rootkits, malware)

## 📞 Contact

For security concerns:
- **GitHub Issues:** [Report here](https://github.com/shadowdevnotreal/House-Party2/issues)
- **Shadow Dev:** [@shadowdevnotreal](https://github.com/shadowdevnotreal)

---

**Remember: With great power comes great responsibility.**

*Use RWIPE only for legitimate protection, never for evidence destruction.*
