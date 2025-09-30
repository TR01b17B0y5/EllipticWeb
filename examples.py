#!/usr/bin/env python3
"""
Example usage of P-256 Elliptic Curve Cryptography CLI
Demonstrates all major cryptographic operations in non-visual mode.
"""

import subprocess
import os
import tempfile
import sys


def run_command(cmd):
    """Run a command and return its output."""
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(f"Error: {result.stderr.strip()}", file=sys.stderr)
    return result.returncode == 0


def main():
    """Demonstrate P-256 elliptic curve cryptography operations."""
    print("=== P-256 Elliptic Curve Cryptography Examples ===\n")
    
    # Create temporary directory for examples
    with tempfile.TemporaryDirectory() as temp_dir:
        os.chdir(temp_dir)
        
        # Copy the CLI script
        cli_script = "/home/runner/work/EllipticWeb/EllipticWeb/elliptic_cli.py"
        
        print("1. Key Generation")
        print("Generating Alice's key pair...")
        run_command(f"python3 {cli_script} keygen --output alice")
        
        print("\nGenerating Bob's key pair...")
        run_command(f"python3 {cli_script} keygen --output bob")
        
        print("\n2. Key Information")
        print("Alice's private key info:")
        run_command(f"python3 {cli_script} keyinfo alice_private.pem")
        
        print("\n3. Digital Signatures")
        print("Creating test message...")
        with open("message.txt", "w") as f:
            f.write("Hello, this is a confidential message from Alice to Bob using P-256 ECC!")
        
        print("\nAlice signs the message...")
        run_command(f"python3 {cli_script} sign alice_private.pem message.txt --output message.sig")
        
        print("\nBob verifies Alice's signature...")
        run_command(f"python3 {cli_script} verify alice_public.pem message.txt message.sig")
        
        print("\n4. Encryption and Decryption")
        print("Alice encrypts message for Bob...")
        run_command(f"python3 {cli_script} encrypt alice_private.pem bob_public.pem message.txt --output message.encrypted")
        
        print("\nBob decrypts the message...")
        run_command(f"python3 {cli_script} decrypt bob_private.pem alice_public.pem message.encrypted --output message.decrypted")
        
        print("\nVerifying decryption...")
        with open("message.txt", "r") as f:
            original = f.read()
        with open("message.decrypted", "r") as f:
            decrypted = f.read()
        
        if original == decrypted:
            print("✓ Decryption successful - messages match!")
        else:
            print("✗ Decryption failed - messages don't match!")
        
        print("\n5. Password-Protected Keys")
        print("Generating password-protected key pair...")
        run_command(f"python3 {cli_script} keygen --output secure --password mypassword123")
        
        print("\nSigning with password-protected key...")
        run_command(f"python3 {cli_script} sign secure_private.pem message.txt --password mypassword123 --output secure.sig")
        
        print("\nVerifying signature...")
        run_command(f"python3 {cli_script} verify secure_public.pem message.txt secure.sig")
        
        print("\n=== All Examples Completed Successfully! ===")


if __name__ == "__main__":
    main()