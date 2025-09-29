# EllipticWeb

A modern web-based application for elliptic curve cryptography operations with 256-bit key support.

## Overview

EllipticWeb is a complete cryptographic toolkit that runs entirely in your browser, providing secure key generation, encryption, decryption, and digital signature capabilities using elliptic curve cryptography.

## Features

### 🔑 Key Generation
- Support for multiple elliptic curves (secp256k1, P-256, P-384, P-521)
- Cryptographically secure key pair generation
- Key export and import functionality
- Local key storage and management

### 🔒 Encryption & Decryption
- Secure message encryption using public keys
- Message decryption with private keys
- Base64 encoding for safe text transmission
- Copy-to-clipboard functionality

### ✍️ Digital Signatures
- Message signing with private keys
- Signature verification using public keys
- Cryptographic proof of authenticity
- JSON format for easy sharing

### 💾 Key Management
- Save and organize multiple key pairs
- Import/export keys in JSON format
- Local browser storage (no server required)
- Key deletion and management

### 🎨 Modern UI/UX
- Clean, responsive design
- Dark/light theme toggle
- Mobile-friendly interface
- Accessibility features
- Toast notifications and loading states

## Getting Started

### Prerequisites
- Node.js and npm (for development)
- Modern web browser with JavaScript enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/TR01b17B0y5/EllipticWeb.git
cd EllipticWeb
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Open your browser to `http://localhost:8080`

### Usage

1. **Generate Keys**: Select an elliptic curve and click "Generate Keys"
2. **Encrypt Messages**: Paste a public key and message, then click "Encrypt"
3. **Decrypt Messages**: Paste encrypted data and click "Decrypt"
4. **Sign Messages**: Use your private key to sign messages for authenticity
5. **Verify Signatures**: Check message signatures using public keys
6. **Manage Keys**: Save, load, and organize your cryptographic keys

## Security Features

- **Client-side only**: All operations run in your browser
- **No data transmission**: Keys and messages never leave your device
- **Secure key generation**: Uses cryptographically secure random number generation
- **Industry standard curves**: Support for NIST and Bitcoin elliptic curves
- **Best practices**: Follows cryptographic security guidelines

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Cryptography**: Elliptic curve cryptography
- **Styling**: Custom CSS with CSS Variables for theming
- **Icons**: Emoji-based icons for cross-platform compatibility
- **Storage**: Local browser storage (localStorage)

## Browser Support

- Chrome/Chromium 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Development

### Project Structure
```
EllipticWeb/
├── index.html          # Main application HTML
├── styles.css          # Application styling
├── script.js           # Full cryptographic implementation
├── script-simple.js    # Demo version for testing
├── package.json        # Project dependencies
└── README.md          # Documentation
```

### Scripts
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm test`: Run tests (if implemented)

## Security Considerations

⚠️ **Important Security Notes:**

- Never share your private keys
- Verify public keys through secure channels
- Use this tool only for educational/demo purposes in production environments
- For production use, implement additional security measures
- This demo version uses simplified cryptographic operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Built with modern web technologies
- Uses elliptic curve cryptography standards
- Inspired by the need for accessible cryptographic tools
