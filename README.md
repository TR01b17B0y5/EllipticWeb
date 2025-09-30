# EllipticWeb

**Comprehensive Elliptic Curve Cryptography Web Application with 256+ bit Key Support**

EllipticWeb is a modern, full-featured web application that implements elliptic curve cryptography (ECC) with support for multiple standard curves including P-256, P-384, and P-521. The application provides a user-friendly interface for key generation, digital signatures, and signature verification with cryptographically secure 256+ bit keys.

![EllipticWeb Interface](https://github.com/user-attachments/assets/2ebc513b-2317-4774-89db-cc9722b646c9)

## ✨ Features

### 🔐 Cryptographic Operations
- **Key Generation**: Generate cryptographically secure private/public key pairs
- **Digital Signatures**: Sign messages using ECDSA (Elliptic Curve Digital Signature Algorithm)
- **Signature Verification**: Verify digital signatures with public keys
- **Multiple Curves**: Support for P-256 (256-bit), P-384 (384-bit), and P-521 (521-bit) curves

### 🌐 Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive UI**: Real-time curve parameter display and key generation
- **Quick Actions**: Copy keys and signatures between operations
- **Error Handling**: Comprehensive error messages and validation

### 🛡️ Security Features
- **Secure Random Generation**: Uses cryptographically secure random number generation
- **Standard Curves**: Implements NIST standard curves (P-256, P-384, P-521)
- **Input Validation**: Comprehensive validation of all cryptographic inputs
- **Memory Safety**: Secure handling of private keys and sensitive data

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Flask web framework

### Installation

1. Clone the repository:
```bash
git clone https://github.com/TR01b17B0y5/EllipticWeb.git
cd EllipticWeb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 📖 Usage Guide

### 1. Curve Selection
Choose from three standard elliptic curves:
- **P-256**: 256-bit security level (recommended for most applications)
- **P-384**: 384-bit security level (high security)
- **P-521**: 521-bit security level (maximum security)

Click "Curve Info" to view detailed curve parameters including prime modulus, coefficients, and generator points.

### 2. Key Generation
1. Select your desired curve
2. Click "Generate New Key Pair"
3. The application will display:
   - Private key (keep this secret!)
   - Public key coordinates (x, y)
   - Key size and curve information

### 3. Digital Signatures
1. Enter your message in the "Message to Sign" field
2. Paste your private key (or use "Copy Keys to Signature" button)
3. Click "Sign Message"
4. The signature components (r, s) will be displayed

### 4. Signature Verification
1. Enter the original message
2. Paste the public key coordinates (x, y)
3. Paste the signature components (r, s)
4. Click "Verify Signature"
5. The result will show ✅ VALID or ❌ INVALID

### 5. Quick Actions
- **Copy Keys to Signature**: Automatically fills private key for signing
- **Copy Signature to Verification**: Copies all data for verification
- **Clear All Fields**: Resets the entire application

## 🏗️ Architecture

### Backend (Python/Flask)
- **EllipticCurveCrypto Class**: Core cryptographic operations
- **Point Class**: Elliptic curve point representation
- **RESTful API**: JSON endpoints for all operations
- **Security**: Secure random number generation and input validation

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach with CSS Grid/Flexbox
- **Interactive UI**: Real-time updates and error handling
- **Modern JavaScript**: ES6+ features with async/await
- **Accessibility**: ARIA labels and keyboard navigation support

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main web interface |
| `/api/curves` | GET | Get available curves |
| `/api/generate_keys` | POST | Generate new key pair |
| `/api/sign` | POST | Sign a message |
| `/api/verify` | POST | Verify a signature |
| `/api/curve_info/<curve>` | GET | Get curve parameters |

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_elliptic_crypto.py
```

The tests cover:
- Curve initialization and validation
- Key generation and validation
- Point arithmetic operations
- Digital signature generation and verification
- Cross-curve compatibility
- Error handling

## 📊 Supported Curves

| Curve | Key Size | Security Level | Field Size | Use Case |
|-------|----------|----------------|------------|-----------|
| P-256 | 256 bits | 128-bit | 256 bits | General purpose, web applications |
| P-384 | 384 bits | 192-bit | 384 bits | High security applications |
| P-521 | 521 bits | 256-bit | 521 bits | Maximum security, government |

## 🔧 Configuration

The application uses standard NIST curve parameters:
- **P-256**: NIST P-256 (secp256r1)
- **P-384**: NIST P-384 (secp384r1)  
- **P-521**: NIST P-521 (secp521r1)

All curves use SHA-256 for message hashing in ECDSA operations.

## 🛡️ Security Considerations

### Best Practices Implemented
- ✅ Cryptographically secure random number generation
- ✅ Standard curve implementations (NIST approved)
- ✅ Proper input validation and sanitization
- ✅ No private key storage or logging
- ✅ Constant-time operations where possible

### Important Security Notes
- **Private Keys**: Never share or transmit private keys over insecure channels
- **Random Numbers**: The application uses Python's `secrets` module for secure randomness
- **Key Storage**: Private keys are only displayed, never stored server-side
- **HTTPS**: Always use HTTPS in production environments

## 🔬 Mathematical Background

EllipticWeb implements elliptic curves over finite fields with the equation:
```
y² = x³ + ax + b (mod p)
```

### Key Operations
- **Point Addition**: Geometric addition on the elliptic curve
- **Scalar Multiplication**: Repeated point addition using double-and-add
- **ECDSA Signing**: `s = k⁻¹(H(m) + r·d) mod n`
- **ECDSA Verification**: Verify using point operations and modular arithmetic

## 🌟 Advanced Features

### Performance Optimizations
- **Double-and-Add**: Efficient scalar multiplication algorithm
- **Modular Inverse**: Extended Euclidean algorithm implementation
- **Lazy Loading**: Curve parameters loaded on demand

### User Experience
- **Copy/Paste Integration**: Seamless data transfer between operations
- **Visual Feedback**: Loading animations and success/error states
- **Keyboard Shortcuts**: Ctrl+G for key generation, Escape to close modals

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include browser information and error messages

## 🔗 Related Resources

- [NIST Elliptic Curve Cryptography](https://csrc.nist.gov/groups/ST/toolkit/documents/dss/NISTReCur.pdf)
- [RFC 6090: Fundamental Elliptic Curve Cryptography Algorithms](https://tools.ietf.org/html/rfc6090)
- [ECDSA Security Considerations](https://tools.ietf.org/html/rfc6979)
