"""
ECC Web Interface
=================

Web interface for the elliptic curve cryptography system.
Provides REST API endpoints and a simple HTML interface for:
- Key generation
- Message signing and verification
- Key exchange
- Address generation
"""

import json
import base64
from typing import Dict, Any, Optional, Tuple
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser
from pathlib import Path

from elliptic_core import secp256k1, EllipticCurvePoint
from cryptographic_operations import KeyPair, ECDSA, ECDH, ECCUtils


class ECCWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for ECC web interface."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self._serve_html()
        elif path == '/api/generate_keys':
            self._handle_generate_keys()
        elif path == '/api/health':
            self._handle_health()
        else:
            self._send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8')) if content_length > 0 else {}
        except (ValueError, json.JSONDecodeError):
            self._send_error(400, "Invalid JSON")
            return
        
        if path == '/api/sign':
            self._handle_sign(data)
        elif path == '/api/verify':
            self._handle_verify(data)
        elif path == '/api/ecdh':
            self._handle_ecdh(data)
        elif path == '/api/address':
            self._handle_address(data)
        else:
            self._send_error(404, "Not Found")
    
    def _serve_html(self):
        """Serve the main HTML interface."""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EllipticWeb - ECC Cryptography</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #718096;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        .section {
            margin: 30px 0;
            padding: 25px;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            background: #f8fafc;
        }
        .section h2 {
            color: #2d3748;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        input, textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e0;
            border-radius: 6px;
            font-size: 14px;
            margin: 5px 0;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
            font-family: monospace;
            resize: vertical;
        }
        .key-display {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 6px;
            font-family: monospace;
            word-break: break-all;
            margin: 10px 0;
            font-size: 12px;
            line-height: 1.4;
        }
        .result {
            background: #f0fff4;
            border: 1px solid #9ae6b4;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        .error {
            background: #fed7d7;
            border: 1px solid #fc8181;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        @media (max-width: 768px) {
            .grid {
                grid-template-columns: 1fr;
            }
            .container {
                padding: 15px;
            }
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-online {
            background-color: #48bb78;
        }
        .status-offline {
            background-color: #f56565;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 EllipticWeb</h1>
        <p class="subtitle">
            Comprehensive Elliptic Curve Cryptography with 256-bit Security
            <br>
            <span id="status"><span class="status-indicator status-offline"></span>Checking connection...</span>
        </p>

        <div class="section">
            <h2>🔑 Key Generation</h2>
            <button onclick="generateKeys()">Generate New Key Pair</button>
            <div id="keys-result"></div>
        </div>

        <div class="grid">
            <div class="section">
                <h2>✍️ Digital Signature (ECDSA)</h2>
                <input type="text" id="sign-private-key" placeholder="Private Key (hex)" />
                <textarea id="sign-message" placeholder="Message to sign"></textarea>
                <button onclick="signMessage()">Sign Message</button>
                <div id="sign-result"></div>
            </div>

            <div class="section">
                <h2>✅ Signature Verification</h2>
                <input type="text" id="verify-public-key" placeholder="Public Key (compressed hex)" />
                <textarea id="verify-message" placeholder="Original message"></textarea>
                <input type="text" id="verify-signature-r" placeholder="Signature R (hex)" />
                <input type="text" id="verify-signature-s" placeholder="Signature S (hex)" />
                <button onclick="verifySignature()">Verify Signature</button>
                <div id="verify-result"></div>
            </div>
        </div>

        <div class="grid">
            <div class="section">
                <h2>🤝 Key Exchange (ECDH)</h2>
                <input type="text" id="ecdh-private-key" placeholder="Your Private Key (hex)" />
                <input type="text" id="ecdh-public-key" placeholder="Other's Public Key (compressed hex)" />
                <button onclick="performECDH()">Generate Shared Secret</button>
                <div id="ecdh-result"></div>
            </div>

            <div class="section">
                <h2>🏠 Address Generation</h2>
                <input type="text" id="address-public-key" placeholder="Public Key (compressed hex)" />
                <button onclick="generateAddress()">Generate Address</button>
                <div id="address-result"></div>
            </div>
        </div>

        <div class="section">
            <h2>ℹ️ About</h2>
            <p>This interface provides access to a comprehensive elliptic curve cryptography implementation featuring:</p>
            <ul>
                <li><strong>secp256k1 Curve:</strong> The same 256-bit curve used by Bitcoin</li>
                <li><strong>ECDSA:</strong> Digital signature algorithm for message authentication</li>
                <li><strong>ECDH:</strong> Key exchange protocol for secure communication</li>
                <li><strong>Point Compression:</strong> Efficient storage and transmission of public keys</li>
                <li><strong>Address Generation:</strong> Bitcoin-style address generation from public keys</li>
            </ul>
            <p><strong>Security Note:</strong> This is a demonstration implementation. Use established libraries for production applications.</p>
        </div>
    </div>

    <script>
        // Check server status
        async function checkStatus() {
            try {
                const response = await fetch('/api/health');
                if (response.ok) {
                    document.getElementById('status').innerHTML = 
                        '<span class="status-indicator status-online"></span>Server Online';
                } else {
                    throw new Error('Server error');
                }
            } catch (error) {
                document.getElementById('status').innerHTML = 
                    '<span class="status-indicator status-offline"></span>Server Offline';
            }
        }

        // Generate new key pair
        async function generateKeys() {
            try {
                const response = await fetch('/api/generate_keys');
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('keys-result').innerHTML = `
                        <div class="result">
                            <h3>New Key Pair Generated</h3>
                            <p><strong>Private Key:</strong></p>
                            <div class="key-display">${data.private_key}</div>
                            <p><strong>Public Key (Compressed):</strong></p>
                            <div class="key-display">${data.public_key_compressed}</div>
                            <p><strong>Address:</strong></p>
                            <div class="key-display">${data.address}</div>
                        </div>
                    `;
                } else {
                    showError('keys-result', data.error);
                }
            } catch (error) {
                showError('keys-result', 'Network error: ' + error.message);
            }
        }

        // Sign message
        async function signMessage() {
            const privateKey = document.getElementById('sign-private-key').value;
            const message = document.getElementById('sign-message').value;

            if (!privateKey || !message) {
                showError('sign-result', 'Please provide both private key and message');
                return;
            }

            try {
                const response = await fetch('/api/sign', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        private_key: privateKey,
                        message: message
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('sign-result').innerHTML = `
                        <div class="result">
                            <h3>Message Signed</h3>
                            <p><strong>Signature R:</strong></p>
                            <div class="key-display">${data.signature.r}</div>
                            <p><strong>Signature S:</strong></p>
                            <div class="key-display">${data.signature.s}</div>
                            <p><strong>DER Encoded:</strong></p>
                            <div class="key-display">${data.signature.der}</div>
                        </div>
                    `;
                } else {
                    showError('sign-result', data.error);
                }
            } catch (error) {
                showError('sign-result', 'Network error: ' + error.message);
            }
        }

        // Verify signature
        async function verifySignature() {
            const publicKey = document.getElementById('verify-public-key').value;
            const message = document.getElementById('verify-message').value;
            const signatureR = document.getElementById('verify-signature-r').value;
            const signatureS = document.getElementById('verify-signature-s').value;

            if (!publicKey || !message || !signatureR || !signatureS) {
                showError('verify-result', 'Please provide all required fields');
                return;
            }

            try {
                const response = await fetch('/api/verify', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        public_key: publicKey,
                        message: message,
                        signature_r: signatureR,
                        signature_s: signatureS
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    const resultClass = data.valid ? 'result' : 'error';
                    const resultText = data.valid ? 'VALID ✅' : 'INVALID ❌';
                    
                    document.getElementById('verify-result').innerHTML = `
                        <div class="${resultClass}">
                            <h3>Signature Verification: ${resultText}</h3>
                        </div>
                    `;
                } else {
                    showError('verify-result', data.error);
                }
            } catch (error) {
                showError('verify-result', 'Network error: ' + error.message);
            }
        }

        // Perform ECDH key exchange
        async function performECDH() {
            const privateKey = document.getElementById('ecdh-private-key').value;
            const publicKey = document.getElementById('ecdh-public-key').value;

            if (!privateKey || !publicKey) {
                showError('ecdh-result', 'Please provide both private and public keys');
                return;
            }

            try {
                const response = await fetch('/api/ecdh', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        private_key: privateKey,
                        public_key: publicKey
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('ecdh-result').innerHTML = `
                        <div class="result">
                            <h3>Shared Secret Generated</h3>
                            <div class="key-display">${data.shared_secret}</div>
                            <p><strong>Derived AES Key:</strong></p>
                            <div class="key-display">${data.derived_key}</div>
                        </div>
                    `;
                } else {
                    showError('ecdh-result', data.error);
                }
            } catch (error) {
                showError('ecdh-result', 'Network error: ' + error.message);
            }
        }

        // Generate address
        async function generateAddress() {
            const publicKey = document.getElementById('address-public-key').value;

            if (!publicKey) {
                showError('address-result', 'Please provide a public key');
                return;
            }

            try {
                const response = await fetch('/api/address', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        public_key: publicKey
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('address-result').innerHTML = `
                        <div class="result">
                            <h3>Address Generated</h3>
                            <div class="key-display">${data.address}</div>
                        </div>
                    `;
                } else {
                    showError('address-result', data.error);
                }
            } catch (error) {
                showError('address-result', 'Network error: ' + error.message);
            }
        }

        // Show error message
        function showError(elementId, message) {
            document.getElementById(elementId).innerHTML = `
                <div class="error">
                    <strong>Error:</strong> ${message}
                </div>
            `;
        }

        // Initialize
        checkStatus();
        setInterval(checkStatus, 30000); // Check status every 30 seconds
    </script>
</body>
</html>
        """
        
        self._send_response(200, html_content, 'text/html')
    
    def _handle_generate_keys(self):
        """Handle key generation request."""
        try:
            keypair = KeyPair.generate()
            
            response = {
                'success': True,
                'private_key': f"{keypair.private_key:064x}",
                'public_key_compressed': keypair.public_key.compress().hex(),
                'address': ECCUtils.point_to_address(keypair.public_key)
            }
            
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(str(e))
    
    def _handle_sign(self, data: Dict[str, Any]):
        """Handle message signing request."""
        try:
            private_key_hex = data.get('private_key', '').strip()
            message = data.get('message', '').encode('utf-8')
            
            if not private_key_hex or not message:
                raise ValueError("Private key and message are required")
            
            private_key = int(private_key_hex, 16)
            ecdsa = ECDSA()
            signature = ecdsa.sign(message, private_key)
            
            der_signature = ECCUtils.signature_to_der(signature)
            
            response = {
                'success': True,
                'signature': {
                    'r': f"{signature[0]:064x}",
                    's': f"{signature[1]:064x}",
                    'der': der_signature.hex()
                }
            }
            
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(str(e))
    
    def _handle_verify(self, data: Dict[str, Any]):
        """Handle signature verification request."""
        try:
            public_key_hex = data.get('public_key', '').strip()
            message = data.get('message', '').encode('utf-8')
            signature_r_hex = data.get('signature_r', '').strip()
            signature_s_hex = data.get('signature_s', '').strip()
            
            if not all([public_key_hex, message, signature_r_hex, signature_s_hex]):
                raise ValueError("All fields are required")
            
            # Decompress public key
            public_key_bytes = bytes.fromhex(public_key_hex)
            public_key = EllipticCurvePoint.decompress(public_key_bytes, secp256k1)
            
            # Parse signature
            signature_r = int(signature_r_hex, 16)
            signature_s = int(signature_s_hex, 16)
            signature = (signature_r, signature_s)
            
            # Verify signature
            ecdsa = ECDSA()
            is_valid = ecdsa.verify(message, signature, public_key)
            
            response = {
                'success': True,
                'valid': is_valid
            }
            
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(str(e))
    
    def _handle_ecdh(self, data: Dict[str, Any]):
        """Handle ECDH key exchange request."""
        try:
            private_key_hex = data.get('private_key', '').strip()
            public_key_hex = data.get('public_key', '').strip()
            
            if not private_key_hex or not public_key_hex:
                raise ValueError("Both private and public keys are required")
            
            private_key = int(private_key_hex, 16)
            public_key_bytes = bytes.fromhex(public_key_hex)
            public_key = EllipticCurvePoint.decompress(public_key_bytes, secp256k1)
            
            # Perform ECDH
            ecdh = ECDH()
            shared_secret = ecdh.generate_shared_secret(private_key, public_key)
            derived_key = ecdh.derive_key(shared_secret, b"AES-256", 32)
            
            response = {
                'success': True,
                'shared_secret': shared_secret.hex(),
                'derived_key': derived_key.hex()
            }
            
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(str(e))
    
    def _handle_address(self, data: Dict[str, Any]):
        """Handle address generation request."""
        try:
            public_key_hex = data.get('public_key', '').strip()
            
            if not public_key_hex:
                raise ValueError("Public key is required")
            
            public_key_bytes = bytes.fromhex(public_key_hex)
            public_key = EllipticCurvePoint.decompress(public_key_bytes, secp256k1)
            
            address = ECCUtils.point_to_address(public_key)
            
            response = {
                'success': True,
                'address': address
            }
            
            self._send_json_response(response)
        except Exception as e:
            self._send_error_response(str(e))
    
    def _handle_health(self):
        """Handle health check request."""
        response = {
            'success': True,
            'status': 'healthy',
            'curve': 'secp256k1',
            'features': ['ECDSA', 'ECDH', 'Key Generation', 'Address Generation']
        }
        self._send_json_response(response)
    
    def _send_response(self, status_code: int, content: str, content_type: str = 'application/json'):
        """Send HTTP response."""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def _send_json_response(self, data: Dict[str, Any]):
        """Send JSON response."""
        content = json.dumps(data, indent=2)
        self._send_response(200, content)
    
    def _send_error_response(self, error_message: str):
        """Send error response."""
        response = {
            'success': False,
            'error': error_message
        }
        self._send_json_response(response)
    
    def _send_error(self, status_code: int, message: str):
        """Send HTTP error response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to reduce log noise."""
        pass


def start_server(host: str = 'localhost', port: int = 8080, open_browser: bool = True):
    """
    Start the ECC web server.
    
    Args:
        host: Server host address
        port: Server port number
        open_browser: Whether to open browser automatically
    """
    try:
        server = HTTPServer((host, port), ECCWebHandler)
        server_url = f"http://{host}:{port}"
        
        print(f"🔐 EllipticWeb Server Starting...")
        print(f"📡 Server URL: {server_url}")
        print(f"🌐 Open your browser to access the interface")
        print(f"⏹️  Press Ctrl+C to stop the server")
        
        if open_browser:
            threading.Thread(target=lambda: webbrowser.open(server_url), daemon=True).start()
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print(f"\n🛑 Server shutting down...")
        server.server_close()
    except Exception as e:
        print(f"❌ Server error: {e}")


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    host = 'localhost'
    port = 8080
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8080.")
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    start_server(host, port)