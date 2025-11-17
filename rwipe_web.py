#!/usr/bin/python3

"""
RWIPE Web GUI v2.0 - Emergency Evidence Protection Web Interface
For emergency situations where CLI access isn't practical

Original Concept: Utku Sen (Jani) | utkusen.com
Refactored & Enhanced: Shadow Dev | 2024

WARNING: This tool performs PERMANENT, UNRECOVERABLE data destruction.
Use only for authorized data protection.
"""

import subprocess
import sys
import os

# Auto-install dependencies
def check_dependencies():
    """Check and install required dependencies."""
    required = {'flask': 'flask', 'pycryptodome': 'Crypto', 'requests': 'requests'}
    missing = []

    for package, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        print("📦 Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
            print("✓ Dependencies installed successfully!\n")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install dependencies. Please run: pip install {' '.join(missing)}")
            sys.exit(1)

check_dependencies()

from flask import Flask, render_template_string, request, jsonify, session
from datetime import datetime, timedelta
import secrets
import threading
import json
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Store activation status
activation_state = {
    'activated': False,
    'timestamp': None,
    'files_encrypted': 0,
    'target_directory': None
}

# Dead man switch state
deadman_state = {
    'enabled': False,
    'last_checkin': None,
    'grace_period': 3600,  # 1 hour default
    'url_token': secrets.token_hex(16)
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RWIPE - Emergency Protocol</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: #00D9FF;
            color: #1a1a1a;
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0, 217, 255, 0.3);
        }

        .header h1 {
            font-size: 2rem;
            font-weight: bold;
        }

        .header p {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .container {
            flex: 1;
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
            width: 100%;
        }

        .warning-box {
            background: #ff4444;
            border-left: 4px solid #ff0000;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-radius: 4px;
        }

        .warning-box h2 {
            margin-bottom: 0.5rem;
        }

        .info-box {
            background: rgba(0, 217, 255, 0.1);
            border-left: 4px solid #00D9FF;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-radius: 4px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 2rem;
            border: 1px solid rgba(0, 217, 255, 0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.3);
        }

        .card h3 {
            color: #00D9FF;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }

        .card p {
            margin-bottom: 1rem;
            line-height: 1.6;
            color: #ccc;
        }

        .input-group {
            margin-bottom: 1rem;
        }

        .input-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: #00D9FF;
            font-weight: 500;
        }

        .input-group input,
        .input-group select {
            width: 100%;
            padding: 0.75rem;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 217, 255, 0.3);
            border-radius: 4px;
            color: #fff;
            font-size: 1rem;
        }

        .input-group input:focus,
        .input-group select:focus {
            outline: none;
            border-color: #00D9FF;
            box-shadow: 0 0 10px rgba(0, 217, 255, 0.3);
        }

        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin-top: 1rem;
        }

        .btn-primary {
            background: #00D9FF;
            color: #1a1a1a;
        }

        .btn-primary:hover {
            background: #00b8d4;
            transform: scale(1.02);
        }

        .btn-danger {
            background: #ff4444;
            color: #fff;
        }

        .btn-danger:hover {
            background: #ff0000;
            transform: scale(1.02);
        }

        .btn-success {
            background: #00ff00;
            color: #1a1a1a;
        }

        .btn-success:hover {
            background: #00cc00;
        }

        .status {
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1rem;
            text-align: center;
            font-weight: bold;
        }

        .status-safe {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
        }

        .status-warning {
            background: rgba(255, 165, 0, 0.2);
            border: 1px solid #ffa500;
            color: #ffa500;
        }

        .status-danger {
            background: rgba(255, 0, 0, 0.2);
            border: 1px solid #ff0000;
            color: #ff0000;
        }

        .qr-code {
            text-align: center;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            margin-top: 1rem;
        }

        .footer {
            background: rgba(0, 0, 0, 0.3);
            padding: 2rem;
            text-align: center;
            color: #888;
        }

        .panic-button {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: #ff0000;
            border: 4px solid #fff;
            box-shadow: 0 4px 20px rgba(255, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
            z-index: 1000;
        }

        .panic-button:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(255, 0, 0, 0.8);
        }

        .panic-button span {
            font-size: 2rem;
        }

        @media (max-width: 768px) {
            .cards {
                grid-template-columns: 1fr;
            }

            .container {
                padding: 0 1rem;
            }

            .panic-button {
                width: 60px;
                height: 60px;
                bottom: 1rem;
                right: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ RWIPE - Emergency Protocol</h1>
        <p>House Party Protocol Activated | Version 2.0</p>
    </div>

    <div class="container">
        <div class="warning-box">
            <h2>⚠️ CRITICAL WARNING</h2>
            <p><strong>THIS TOOL PERFORMS PERMANENT, UNRECOVERABLE DATA DESTRUCTION.</strong></p>
            <p>Files encrypted with RWIPE cannot be recovered. Ever. By anyone. This is BY DESIGN for maximum protection.</p>
            <p><strong>Use only when you understand and accept the consequences.</strong></p>
        </div>

        <div class="status status-safe" id="status">
            ✓ System Ready | No Active Protocol
        </div>

        <div class="cards">
            <div class="card">
                <h3>🎯 Local Panic Mode</h3>
                <p>Immediate encryption activation. For emergency situations when you need instant protection.</p>

                <div class="input-group">
                    <label for="panic-directory">Target Directory:</label>
                    <input type="text" id="panic-directory" placeholder="/path/to/directory">
                </div>

                <div class="input-group">
                    <label for="panic-password">Password:</label>
                    <input type="password" id="panic-password" placeholder="Strong password">
                </div>

                <button class="btn btn-danger" onclick="activatePanic()">
                    🚨 ACTIVATE PANIC MODE
                </button>
            </div>

            <div class="card">
                <h3>☠️ Dead Man Switch</h3>
                <p>Auto-activation if you don't check in. Perfect for dangerous situations.</p>

                <div class="input-group">
                    <label for="dms-directory">Target Directory:</label>
                    <input type="text" id="dms-directory" placeholder="/path/to/directory">
                </div>

                <div class="input-group">
                    <label for="dms-grace">Grace Period (seconds):</label>
                    <input type="number" id="dms-grace" value="3600" min="60">
                </div>

                <div class="input-group">
                    <label for="dms-password">Password:</label>
                    <input type="password" id="dms-password" placeholder="Strong password">
                </div>

                <button class="btn btn-primary" onclick="enableDeadManSwitch()">
                    ⏱️ ENABLE DEAD MAN SWITCH
                </button>

                <button class="btn btn-success" onclick="checkin()" style="margin-top: 0.5rem;">
                    ✓ CHECK IN (I'm Alive)
                </button>
            </div>

            <div class="card">
                <h3>📡 Remote Trigger</h3>
                <p>Activate from anywhere via special URL. Share with trusted colleagues.</p>

                <div class="info-box">
                    <p><strong>Trigger URL:</strong></p>
                    <p style="word-break: break-all; font-family: monospace; font-size: 0.9rem;">
                        http://localhost:5000/trigger/{{ trigger_token }}
                    </p>
                </div>

                <p style="color: #00D9FF; margin-top: 1rem;">
                    🔒 Keep this URL secret. Anyone with this URL can activate the protocol.
                </p>
            </div>
        </div>

        <div class="info-box">
            <h2>📱 Mobile Access</h2>
            <p>Scan QR code from your phone for instant mobile access:</p>
            <div class="qr-code">
                <p style="color: #000;">QR Code: http://YOUR-IP:5000</p>
                <p style="color: #666; font-size: 0.8rem;">Replace YOUR-IP with this computer's IP address</p>
            </div>
        </div>
    </div>

    <div class="panic-button" onclick="quickPanic()" title="Quick Panic - Click for instant activation">
        <span>🚨</span>
    </div>

    <div class="footer">
        <p>RWIPE v2.0 - Emergency Evidence Protection System</p>
        <p>Made with ⚡ by Shadow Dev | Original concept by Utku Sen</p>
        <p style="margin-top: 1rem; color: #ff4444;">
            ⚠️ Use responsibly and legally. For journalist/whistleblower protection only.
        </p>
    </div>

    <script>
        function activatePanic() {
            const directory = document.getElementById('panic-directory').value;
            const password = document.getElementById('panic-password').value;

            if (!directory || !password) {
                alert('Please fill in all fields');
                return;
            }

            if (!confirm('⚠️ WARNING\\n\\nThis will PERMANENTLY and IRREVERSIBLY encrypt all files in:\\n' + directory + '\\n\\nThere is NO way to recover these files.\\n\\nType DESTROY to confirm:')) {
                return;
            }

            const confirmation = prompt('Type DESTROY to confirm:');
            if (confirmation !== 'DESTROY') {
                alert('Activation cancelled');
                return;
            }

            fetch('/activate-panic', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({directory, password})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('status').className = 'status status-danger';
                    document.getElementById('status').textContent = '🔥 PANIC MODE ACTIVATED | Encryption in Progress...';
                    alert('Panic mode activated! Encryption started.');
                } else {
                    alert('Error: ' + data.message);
                }
            });
        }

        function enableDeadManSwitch() {
            const directory = document.getElementById('dms-directory').value;
            const grace = document.getElementById('dms-grace').value;
            const password = document.getElementById('dms-password').value;

            if (!directory || !password) {
                alert('Please fill in all fields');
                return;
            }

            fetch('/enable-deadman', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({directory, grace_period: parseInt(grace), password})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('status').className = 'status status-warning';
                    document.getElementById('status').textContent = '☠️ DEAD MAN SWITCH ARMED | Grace Period: ' + grace + 's';
                    alert('Dead man switch enabled! Remember to check in regularly.');
                } else {
                    alert('Error: ' + data.message);
                }
            });
        }

        function checkin() {
            fetch('/checkin', {method: 'POST'})
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    alert('✓ Check-in successful! Dead man switch timer reset.');
                } else {
                    alert('Error: ' + data.message);
                }
            });
        }

        function quickPanic() {
            const directory = prompt('Enter target directory for EMERGENCY encryption:');
            if (!directory) return;

            const password = prompt('Enter password:');
            if (!password) return;

            if (confirm('⚠️ FINAL WARNING\\n\\nPermanently encrypt all files in ' + directory + '?\\n\\nNO RECOVERY POSSIBLE')) {
                fetch('/activate-panic', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({directory, password})
                })
                .then(r => r.json())
                .then(data => alert(data.success ? 'Activated!' : 'Error: ' + data.message));
            }
        }

        // Status check every 5 seconds
        setInterval(() => {
            fetch('/status')
            .then(r => r.json())
            .then(data => {
                if (data.activated) {
                    document.getElementById('status').className = 'status status-danger';
                    document.getElementById('status').textContent = '🔥 ACTIVE | ' + data.files_encrypted + ' files encrypted';
                }
            });
        }, 5000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, trigger_token=deadman_state['url_token'])

@app.route('/activate-panic', methods=['POST'])
def activate_panic():
    try:
        data = request.json
        directory = data.get('directory')
        password = data.get('password')

        if not directory or not password:
            return jsonify({'success': False, 'message': 'Missing parameters'})

        if not os.path.exists(directory):
            return jsonify({'success': False, 'message': 'Directory does not exist'})

        # Launch rwipe.py in background
        subprocess.Popen([
            sys.executable, 'rwipe.py',
            '-d', directory,
            '-m', 'local',
            '-p', password,
            '--no-confirm'
        ])

        activation_state['activated'] = True
        activation_state['timestamp'] = datetime.now()
        activation_state['target_directory'] = directory

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/enable-deadman', methods=['POST'])
def enable_deadman():
    try:
        data = request.json
        deadman_state['enabled'] = True
        deadman_state['last_checkin'] = datetime.now()
        deadman_state['grace_period'] = data.get('grace_period', 3600)
        deadman_state['directory'] = data.get('directory')
        deadman_state['password'] = data.get('password')

        # Start monitoring thread
        threading.Thread(target=monitor_deadman, daemon=True).start()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/checkin', methods=['POST'])
def checkin():
    if deadman_state['enabled']:
        deadman_state['last_checkin'] = datetime.now()
        return jsonify({'success': True, 'message': 'Check-in successful'})
    return jsonify({'success': False, 'message': 'Dead man switch not enabled'})

@app.route('/trigger/<token>')
def trigger(token):
    if token == deadman_state['url_token']:
        # Activate panic mode
        if deadman_state.get('directory') and deadman_state.get('password'):
            subprocess.Popen([
                sys.executable, 'rwipe.py',
                '-d', deadman_state['directory'],
                '-m', 'local',
                '-p', deadman_state['password'],
                '--no-confirm'
            ])
            return "Protocol Activated", 200
    return "Invalid Token", 403

@app.route('/status')
def status():
    return jsonify({
        'activated': activation_state['activated'],
        'files_encrypted': activation_state.get('files_encrypted', 0),
        'timestamp': str(activation_state.get('timestamp', ''))
    })

def monitor_deadman():
    """Monitor dead man switch and activate if no check-in."""
    while deadman_state['enabled']:
        if deadman_state['last_checkin']:
            elapsed = (datetime.now() - deadman_state['last_checkin']).total_seconds()
            if elapsed > deadman_state['grace_period']:
                # Activate!
                if deadman_state.get('directory') and deadman_state.get('password'):
                    subprocess.Popen([
                        sys.executable, 'rwipe.py',
                        '-d', deadman_state['directory'],
                        '-m', 'local',
                        '-p', deadman_state['password'],
                        '--no-confirm'
                    ])
                    deadman_state['enabled'] = False
                    break
        sleep(10)

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        🛡️  RWIPE WEB GUI - EMERGENCY PROTOCOL  🛡️        ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

Starting web interface on http://localhost:5000

Access from mobile: http://YOUR-IP-ADDRESS:5000

⚠️  WARNING: This tool performs PERMANENT data destruction.
   Use only for authorized emergency protection.

Press Ctrl+C to stop the server.
""")
    app.run(host='0.0.0.0', port=5000, debug=False)
