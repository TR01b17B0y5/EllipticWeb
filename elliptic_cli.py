#!/usr/bin/env python3
"""
P-256 Elliptic Curve Cryptography CLI
Provides non-visual command-line interface for P-256 elliptic curve operations.
"""

import click
import base64
import json
import os
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidSignature


class P256EllipticCrypto:
    """P-256 Elliptic Curve Cryptography implementation."""
    
    def __init__(self):
        self.curve = ec.SECP256R1()
    
    def generate_key_pair(self):
        """Generate a new P-256 key pair."""
        private_key = ec.generate_private_key(self.curve)
        public_key = private_key.public_key()
        return private_key, public_key
    
    def serialize_private_key(self, private_key, password=None):
        """Serialize private key to PEM format."""
        encryption = serialization.NoEncryption()
        if password:
            encryption = serialization.BestAvailableEncryption(password.encode())
        
        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption
        )
    
    def serialize_public_key(self, public_key):
        """Serialize public key to PEM format."""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def load_private_key(self, pem_data, password=None):
        """Load private key from PEM data."""
        password_bytes = password.encode() if password else None
        return serialization.load_pem_private_key(pem_data, password_bytes)
    
    def load_public_key(self, pem_data):
        """Load public key from PEM data."""
        return serialization.load_pem_public_key(pem_data)
    
    def sign_data(self, private_key, data):
        """Sign data using ECDSA with SHA-256."""
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return base64.b64encode(signature).decode()
    
    def verify_signature(self, public_key, data, signature_b64):
        """Verify ECDSA signature."""
        try:
            signature = base64.b64decode(signature_b64)
            public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
    
    def derive_shared_key(self, private_key, public_key):
        """Derive shared key using ECDH."""
        shared_key = private_key.exchange(ec.ECDH(), public_key)
        # Derive a 256-bit key using HKDF
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'elliptic-web-p256'
        ).derive(shared_key)
        return derived_key
    
    def encrypt_data(self, key, data):
        """Encrypt data using AES-256-GCM."""
        iv = os.urandom(12)  # 96-bit IV for GCM
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        
        # Return IV + tag + ciphertext as base64
        encrypted_data = iv + encryptor.tag + ciphertext
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_data(self, key, encrypted_data_b64):
        """Decrypt data using AES-256-GCM."""
        try:
            encrypted_data = base64.b64decode(encrypted_data_b64)
            iv = encrypted_data[:12]
            tag = encrypted_data[12:28]
            ciphertext = encrypted_data[28:]
            
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext
        except Exception:
            return None


# Global crypto instance
crypto = P256EllipticCrypto()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """P-256 Elliptic Curve Cryptography CLI Tool
    
    Provides command-line interface for P-256 cryptographic operations
    including key generation, digital signatures, and key exchange.
    """
    pass


@cli.command()
@click.option('--output', '-o', help='Output file prefix (default: key)')
@click.option('--password', '-p', help='Password to encrypt private key')
def keygen(output, password):
    """Generate a new P-256 key pair."""
    if not output:
        output = 'key'
    
    try:
        private_key, public_key = crypto.generate_key_pair()
        
        # Save private key
        private_pem = crypto.serialize_private_key(private_key, password)
        private_file = f"{output}_private.pem"
        with open(private_file, 'wb') as f:
            f.write(private_pem)
        
        # Save public key
        public_pem = crypto.serialize_public_key(public_key)
        public_file = f"{output}_public.pem"
        with open(public_file, 'wb') as f:
            f.write(public_pem)
        
        click.echo(f"✓ Key pair generated successfully:")
        click.echo(f"  Private key: {private_file}")
        click.echo(f"  Public key: {public_file}")
        
        if password:
            click.echo("  Private key is encrypted with provided password.")
        
    except Exception as e:
        click.echo(f"✗ Error generating key pair: {e}", err=True)


@cli.command()
@click.argument('private_key_file')
@click.argument('data_file')
@click.option('--password', '-p', help='Password for encrypted private key')
@click.option('--output', '-o', help='Output signature file')
def sign(private_key_file, data_file, password, output):
    """Sign data with private key using ECDSA."""
    try:
        # Load private key
        with open(private_key_file, 'rb') as f:
            private_key = crypto.load_private_key(f.read(), password)
        
        # Load data to sign
        with open(data_file, 'rb') as f:
            data = f.read()
        
        # Sign data
        signature = crypto.sign_data(private_key, data)
        
        # Save signature
        if output:
            with open(output, 'w') as f:
                f.write(signature)
            click.echo(f"✓ Signature saved to: {output}")
        else:
            click.echo(f"Signature: {signature}")
        
    except FileNotFoundError as e:
        click.echo(f"✗ File not found: {e}", err=True)
    except Exception as e:
        click.echo(f"✗ Error signing data: {e}", err=True)


@cli.command()
@click.argument('public_key_file')
@click.argument('data_file')
@click.argument('signature')
def verify(public_key_file, data_file, signature):
    """Verify signature with public key."""
    try:
        # Load public key
        with open(public_key_file, 'rb') as f:
            public_key = crypto.load_public_key(f.read())
        
        # Load data
        with open(data_file, 'rb') as f:
            data = f.read()
        
        # If signature is a file, read it
        if os.path.isfile(signature):
            with open(signature, 'r') as f:
                signature = f.read().strip()
        
        # Verify signature
        is_valid = crypto.verify_signature(public_key, data, signature)
        
        if is_valid:
            click.echo("✓ Signature is VALID")
        else:
            click.echo("✗ Signature is INVALID", err=True)
            
    except FileNotFoundError as e:
        click.echo(f"✗ File not found: {e}", err=True)
    except Exception as e:
        click.echo(f"✗ Error verifying signature: {e}", err=True)


@cli.command()
@click.argument('private_key_file')
@click.argument('public_key_file')
@click.argument('data_file')
@click.option('--private-password', '-pp', help='Password for private key')
@click.option('--output', '-o', help='Output encrypted file')
def encrypt(private_key_file, public_key_file, data_file, private_password, output):
    """Encrypt data using ECDH key exchange and AES-256-GCM."""
    try:
        # Load keys
        with open(private_key_file, 'rb') as f:
            private_key = crypto.load_private_key(f.read(), private_password)
        
        with open(public_key_file, 'rb') as f:
            public_key = crypto.load_public_key(f.read())
        
        # Load data
        with open(data_file, 'rb') as f:
            data = f.read()
        
        # Derive shared key and encrypt
        shared_key = crypto.derive_shared_key(private_key, public_key)
        encrypted_data = crypto.encrypt_data(shared_key, data)
        
        # Save encrypted data
        output_file = output or f"{data_file}.encrypted"
        with open(output_file, 'w') as f:
            f.write(encrypted_data)
        
        click.echo(f"✓ Data encrypted and saved to: {output_file}")
        
    except FileNotFoundError as e:
        click.echo(f"✗ File not found: {e}", err=True)
    except Exception as e:
        click.echo(f"✗ Error encrypting data: {e}", err=True)


@cli.command()
@click.argument('private_key_file')
@click.argument('public_key_file')
@click.argument('encrypted_file')
@click.option('--private-password', '-pp', help='Password for private key')
@click.option('--output', '-o', help='Output decrypted file')
def decrypt(private_key_file, public_key_file, encrypted_file, private_password, output):
    """Decrypt data using ECDH key exchange and AES-256-GCM."""
    try:
        # Load keys
        with open(private_key_file, 'rb') as f:
            private_key = crypto.load_private_key(f.read(), private_password)
        
        with open(public_key_file, 'rb') as f:
            public_key = crypto.load_public_key(f.read())
        
        # Load encrypted data
        with open(encrypted_file, 'r') as f:
            encrypted_data = f.read().strip()
        
        # Derive shared key and decrypt
        shared_key = crypto.derive_shared_key(private_key, public_key)
        decrypted_data = crypto.decrypt_data(shared_key, encrypted_data)
        
        if decrypted_data is None:
            click.echo("✗ Failed to decrypt data (invalid key or corrupted data)", err=True)
            return
        
        # Save decrypted data
        output_file = output or f"{encrypted_file}.decrypted"
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        click.echo(f"✓ Data decrypted and saved to: {output_file}")
        
    except FileNotFoundError as e:
        click.echo(f"✗ File not found: {e}", err=True)
    except Exception as e:
        click.echo(f"✗ Error decrypting data: {e}", err=True)


@cli.command()
@click.argument('key_file')
@click.option('--password', '-p', help='Password for encrypted private key')
def keyinfo(key_file, password):
    """Display information about a key file."""
    try:
        with open(key_file, 'rb') as f:
            key_data = f.read()
        
        # Try to load as private key first
        try:
            private_key = crypto.load_private_key(key_data, password)
            public_key = private_key.public_key()
            
            click.echo(f"Key file: {key_file}")
            click.echo(f"Type: Private Key (P-256)")
            click.echo(f"Curve: SECP256R1")
            click.echo(f"Key size: 256 bits")
            
            # Get public key info
            public_numbers = public_key.public_numbers()
            click.echo(f"Public key X: {hex(public_numbers.x)}")
            click.echo(f"Public key Y: {hex(public_numbers.y)}")
            
        except:
            # Try as public key
            public_key = crypto.load_public_key(key_data)
            
            click.echo(f"Key file: {key_file}")
            click.echo(f"Type: Public Key (P-256)")
            click.echo(f"Curve: SECP256R1")
            click.echo(f"Key size: 256 bits")
            
            # Get public key info
            public_numbers = public_key.public_numbers()
            click.echo(f"Public key X: {hex(public_numbers.x)}")
            click.echo(f"Public key Y: {hex(public_numbers.y)}")
        
    except FileNotFoundError:
        click.echo(f"✗ File not found: {key_file}", err=True)
    except Exception as e:
        click.echo(f"✗ Error reading key file: {e}", err=True)


if __name__ == '__main__':
    cli()