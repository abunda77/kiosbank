#!/usr/bin/env python3
"""
============================================================
SSH SOCKS5 Tunnel untuk KIOSBANK API
VPS: Load from .env
User: Load from .env
============================================================
"""

import subprocess
import sys
import platform
from env_config import get_env, get_env_int

def print_header():
    """Print informasi header tunnel"""
    vps_ip = get_env('VPS_IP', required=True)
    vps_user = get_env('VPS_USER', required=True)
    proxy_port = get_env_int('PROXY_PORT', default=1080)
    
    print("=" * 60)
    print("Starting SSH SOCKS5 Tunnel to VPS")
    print("=" * 60)
    print()
    print(f"VPS IP: {vps_ip}")
    print(f"User: {vps_user}")
    print(f"Local SOCKS5 Port: {proxy_port}")
    print()
    print("IMPORTANT: Keep this window OPEN while using the proxy!")
    print("Press Ctrl+C to stop the tunnel.")
    print()
    print("=" * 60)
    print()

def start_ssh_tunnel():
    """
    Memulai SSH SOCKS5 tunnel ke VPS
    
    Parameters:
    -D 1080 = SOCKS5 proxy on port 1080
    -N = No command execution (just tunnel)
    -v = Verbose (show connection details)
    """
    try:
        # Print header
        print_header()
        
        # Load configuration from environment variables
        vps_ip = get_env('VPS_IP', required=True)
        vps_user = get_env('VPS_USER', required=True)
        proxy_port = get_env_int('PROXY_PORT', default=1080)
        
        # SSH command
        ssh_command = [
            "ssh",
            "-D", str(proxy_port),  # SOCKS5 proxy on configured port
            "-N",                   # No command execution (just tunnel)
            "-v",                   # Verbose (show connection details)
            f"{vps_user}@{vps_ip}"
        ]
        
        # Jalankan SSH tunnel
        # subprocess.run akan menunggu sampai proses selesai
        result = subprocess.run(ssh_command)
        
        # Jika keluar dengan normal (Ctrl+C atau error)
        print()
        print("=" * 60)
        print("SSH Tunnel Stopped")
        print("=" * 60)
        
        return result.returncode
        
    except KeyboardInterrupt:
        # Handle Ctrl+C dengan graceful
        print()
        print()
        print("=" * 60)
        print("SSH Tunnel Stopped (Interrupted by user)")
        print("=" * 60)
        return 0
        
    except FileNotFoundError:
        print()
        print("ERROR: SSH command not found!")
        print("Please make sure SSH client is installed on your system.")
        print()
        if platform.system() == "Windows":
            print("On Windows 10/11, OpenSSH should be available by default.")
            print("If not, you can install it via Settings > Apps > Optional Features")
        return 1
        
    except Exception as e:
        print()
        print(f"ERROR: {str(e)}")
        return 1

def main():
    """Main function"""
    exit_code = start_ssh_tunnel()
    
    # Pause sebelum keluar (seperti 'pause' di batch)
    if platform.system() == "Windows":
        input("\nPress Enter to exit...")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
