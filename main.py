#!/usr/bin/env python3
"""
EllipticWeb Main Entry Point
============================

Main command-line interface for the EllipticWeb ECC library.
Provides easy access to all functionality including tests, examples, and web interface.
"""

import sys
import argparse
from pathlib import Path


def run_tests():
    """Run the comprehensive test suite."""
    print("🧪 Running ECC Test Suite...")
    try:
        from test_ecc import run_all_tests
        success = run_all_tests()
        if success:
            print("✅ All tests passed!")
            return 0
        else:
            print("❌ Some tests failed!")
            return 1
    except ImportError as e:
        print(f"❌ Could not import test module: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def run_examples():
    """Run example demonstrations."""
    print("📚 Running ECC Examples...")
    try:
        from examples import run_all_examples
        success = run_all_examples()
        if success:
            print("✅ All examples completed successfully!")
            return 0
        else:
            print("❌ Some examples failed!")
            return 1
    except ImportError as e:
        print(f"❌ Could not import examples module: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        return 1


def start_web_server(host='localhost', port=8080, open_browser=True):
    """Start the web interface server."""
    print("🌐 Starting ECC Web Interface...")
    try:
        from ecc_web_interface import start_server
        start_server(host, port, open_browser)
        return 0
    except ImportError as e:
        print(f"❌ Could not import web interface module: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        return 1


def interactive_mode():
    """Start interactive Python shell with ECC modules loaded."""
    print("🐍 Starting Interactive Mode...")
    print("ECC modules have been imported and are ready to use:")
    print()
    print("Available imports:")
    print("  from elliptic_core import secp256k1, EllipticCurvePoint")
    print("  from cryptographic_operations import KeyPair, ECDSA, ECDH, ECCUtils")
    print()
    print("Quick start:")
    print("  keypair = KeyPair.generate()")
    print("  ecdsa = ECDSA()")
    print("  signature = ecdsa.sign(b'message', keypair.private_key)")
    print()
    
    try:
        # Import all modules
        from elliptic_core import secp256k1, EllipticCurvePoint, ModularArithmetic
        from cryptographic_operations import KeyPair, ECDSA, ECDH, ECCUtils, SecureRandom
        
        # Start interactive shell
        import code
        local_vars = {
            'secp256k1': secp256k1,
            'EllipticCurvePoint': EllipticCurvePoint,
            'ModularArithmetic': ModularArithmetic,
            'KeyPair': KeyPair,
            'ECDSA': ECDSA,
            'ECDH': ECDH,
            'ECCUtils': ECCUtils,
            'SecureRandom': SecureRandom
        }
        
        code.interact(local=local_vars)
        return 0
        
    except ImportError as e:
        print(f"❌ Could not import ECC modules: {e}")
        return 1
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")
        return 1


def show_info():
    """Show information about the ECC implementation."""
    try:
        from elliptic_core import secp256k1
        from cryptographic_operations import KeyPair
        
        print("🔐 EllipticWeb - Comprehensive ECC Implementation")
        print("=" * 60)
        print()
        print("Curve Information:")
        print(f"  Curve: secp256k1")
        print(f"  Prime (p): {secp256k1.p:x}")
        print(f"  Order (n): {secp256k1.n:x}")
        print(f"  Generator: ({secp256k1.G.x:x}, {secp256k1.G.y:x})")
        print()
        print("Features:")
        print("  ✅ 256-bit elliptic curve cryptography")
        print("  ✅ ECDSA digital signatures")
        print("  ✅ ECDH key exchange")
        print("  ✅ Secure key generation")
        print("  ✅ Point compression/decompression")
        print("  ✅ Address generation")
        print("  ✅ Web interface")
        print("  ✅ Comprehensive test suite")
        print()
        print("Security:")
        print("  🔒 Cryptographically secure random number generation")
        print("  🔒 Constant-time operations where possible")
        print("  🔒 Input validation and error handling")
        print("  🔒 Standard curve parameters (secp256k1)")
        print()
        
        # Generate sample keypair to show format
        print("Sample Key Generation:")
        keypair = KeyPair.generate()
        print(f"  Private Key: {keypair.private_key:064x}")
        print(f"  Public Key:  {keypair.public_key.compress().hex()}")
        
        from cryptographic_operations import ECCUtils
        address = ECCUtils.point_to_address(keypair.public_key)
        print(f"  Address:     {address}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error showing info: {e}")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='EllipticWeb - Comprehensive Elliptic Curve Cryptography',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s test                    # Run test suite
  %(prog)s examples                # Run examples
  %(prog)s web                     # Start web interface
  %(prog)s web --port 9000         # Start web interface on port 9000
  %(prog)s interactive             # Start interactive Python shell
  %(prog)s info                    # Show implementation information
        """
    )
    
    parser.add_argument('command', 
                       choices=['test', 'examples', 'web', 'interactive', 'info'],
                       help='Command to execute')
    
    # Web server options
    parser.add_argument('--host', default='localhost',
                       help='Web server host (default: localhost)')
    parser.add_argument('--port', type=int, default=8080,
                       help='Web server port (default: 8080)')
    parser.add_argument('--no-browser', action='store_true',
                       help='Do not open browser automatically')
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'test':
        return run_tests()
    elif args.command == 'examples':
        return run_examples()
    elif args.command == 'web':
        return start_web_server(args.host, args.port, not args.no_browser)
    elif args.command == 'interactive':
        return interactive_mode()
    elif args.command == 'info':
        return show_info()
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)