# EllipticWeb - P-256 Elliptic Curve Cryptography

A complete implementation of P-256 elliptic curve cryptography with command-line interface for non-visual (real mode) operations.

## Features

- **P-256 Elliptic Curve**: SECP256R1 curve with 256-bit key length
- **Key Management**: Generate, store, and load P-256 key pairs
- **Digital Signatures**: ECDSA with SHA-256 for data authentication
- **Encryption/Decryption**: ECDH key exchange with AES-256-GCM
- **Password Protection**: Optional password encryption for private keys
- **Non-Visual Interface**: Complete command-line interface for automated/scripted use
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make the CLI script executable:
```bash
chmod +x elliptic_cli.py
```

## Usage

### Key Generation

Generate a new P-256 key pair:
```bash
python3 elliptic_cli.py keygen --output mykey
```

Generate password-protected keys:
```bash
python3 elliptic_cli.py keygen --output secure --password mypassword
```

### Key Information

Display key information:
```bash
python3 elliptic_cli.py keyinfo mykey_private.pem
python3 elliptic_cli.py keyinfo mykey_public.pem
```

### Digital Signatures

Sign data:
```bash
python3 elliptic_cli.py sign private_key.pem data.txt --output signature.txt
```

Verify signature:
```bash
python3 elliptic_cli.py verify public_key.pem data.txt signature.txt
```

### Encryption/Decryption

Encrypt data (requires sender's private key and recipient's public key):
```bash
python3 elliptic_cli.py encrypt sender_private.pem recipient_public.pem data.txt --output encrypted.txt
```

Decrypt data (requires recipient's private key and sender's public key):
```bash
python3 elliptic_cli.py decrypt recipient_private.pem sender_public.pem encrypted.txt --output decrypted.txt
```

## Examples

Run the example script to see all operations in action:
```bash
python3 examples.py
```

## Command Reference

### `keygen` - Generate Key Pair
```
python3 elliptic_cli.py keygen [OPTIONS]

Options:
  --output, -o TEXT    Output file prefix (default: key)
  --password, -p TEXT  Password to encrypt private key
```

### `sign` - Sign Data
```
python3 elliptic_cli.py sign PRIVATE_KEY_FILE DATA_FILE [OPTIONS]

Options:
  --password, -p TEXT  Password for encrypted private key
  --output, -o TEXT    Output signature file
```

### `verify` - Verify Signature
```
python3 elliptic_cli.py verify PUBLIC_KEY_FILE DATA_FILE SIGNATURE
```

### `encrypt` - Encrypt Data
```
python3 elliptic_cli.py encrypt PRIVATE_KEY_FILE PUBLIC_KEY_FILE DATA_FILE [OPTIONS]

Options:
  --private-password, -pp TEXT  Password for private key
  --output, -o TEXT            Output encrypted file
```

### `decrypt` - Decrypt Data
```
python3 elliptic_cli.py decrypt PRIVATE_KEY_FILE PUBLIC_KEY_FILE ENCRYPTED_FILE [OPTIONS]

Options:
  --private-password, -pp TEXT  Password for private key
  --output, -o TEXT            Output decrypted file
```

### `keyinfo` - Display Key Information
```
python3 elliptic_cli.py keyinfo KEY_FILE [OPTIONS]

Options:
  --password, -p TEXT  Password for encrypted private key
```

## Security Features

- **P-256 Curve**: Uses the secure SECP256R1 elliptic curve
- **Strong Cryptography**: ECDSA with SHA-256, AES-256-GCM encryption
- **Key Protection**: Optional password protection for private keys
- **Secure Random**: Uses cryptographically secure random number generation
- **Memory Safety**: Secure key handling with proper cleanup

## Technical Details

- **Curve**: SECP256R1 (P-256)
- **Key Size**: 256 bits
- **Signature Algorithm**: ECDSA with SHA-256
- **Key Exchange**: ECDH (Elliptic Curve Diffie-Hellman)
- **Encryption**: AES-256-GCM with HKDF key derivation
- **Key Format**: PEM (PKCS#8 for private keys, SubjectPublicKeyInfo for public keys)

## License

This project implements standard cryptographic algorithms and is intended for educational and practical use.
