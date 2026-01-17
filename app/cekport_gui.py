#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CekPort - GUI Version (Non-Interactive)
Menampilkan semua port yang terbuka di sistem
"""

import sys
import psutil
import platform
from env_config import get_env_int

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def get_open_ports():
    """Mengambil daftar port yang terbuka."""
    open_ports = []
    for conn in psutil.net_connections():
        if conn.status == 'LISTEN':
            try:
                # Get process info
                process = psutil.Process(conn.pid)
                proc_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                proc_name = "Unknown"
            
            open_ports.append({
                'port': conn.laddr.port,
                'pid': conn.pid,
                'process': proc_name,
                'address': conn.laddr.ip if conn.laddr.ip else '*'
            })
    
    # Sort by port number
    return sorted(open_ports, key=lambda x: x['port'])

def is_port_open(port):
    """Memeriksa apakah port tertentu terbuka."""
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == 'LISTEN':
            return True
    return False

def main():
    print("=" * 80)
    print("Port Status Checker")
    print("=" * 80)
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python Version: {platform.python_version()}")
    print("=" * 80)
    
    # Check specific port for proxy
    proxy_port = get_env_int('PROXY_PORT', default=1080)
    print(f"\n🔍 Checking Proxy Port ({proxy_port}):")
    print("-" * 80)
    
    if is_port_open(proxy_port):
        print(f"✅ Port {proxy_port} is OPEN (SSH Tunnel is running)")
        
        # Get process info
        for conn in psutil.net_connections():
            if conn.laddr.port == proxy_port and conn.status == 'LISTEN':
                try:
                    process = psutil.Process(conn.pid)
                    print(f"   Process: {process.name()} (PID: {conn.pid})")
                    print(f"   Command: {' '.join(process.cmdline()[:3])}...")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    print(f"   Process: Unknown (PID: {conn.pid})")
                break
    else:
        print(f"❌ Port {proxy_port} is CLOSED (SSH Tunnel NOT running)")
        print(f"   To start SSH tunnel, click 'Start SSH Tunnel' button")
    
    # Get all open ports
    print(f"\n📋 All Open Ports:")
    print("-" * 80)
    
    ports = get_open_ports()
    
    if ports:
        # Group by port ranges
        common_ports = []
        high_ports = []
        
        for port_info in ports:
            if port_info['port'] < 10000:
                common_ports.append(port_info)
            else:
                high_ports.append(port_info)
        
        if common_ports:
            print("\n📌 Common Ports (< 10000):")
            print(f"{'Port':<8} {'Address':<15} {'PID':<8} {'Process':<30}")
            print("-" * 80)
            for p in common_ports[:20]:  # Limit to 20 to avoid too much output
                print(f"{p['port']:<8} {p['address']:<15} {p['pid']:<8} {p['process']:<30}")
            
            if len(common_ports) > 20:
                print(f"\n... and {len(common_ports) - 20} more ports")
        
        if high_ports:
            print(f"\n📌 High Ports (>= 10000): {len(high_ports)} ports")
            # Show only first 10 high ports
            if len(high_ports) <= 10:
                print(f"{'Port':<8} {'Address':<15} {'PID':<8} {'Process':<30}")
                print("-" * 80)
                for p in high_ports:
                    print(f"{p['port']:<8} {p['address']:<15} {p['pid']:<8} {p['process']:<30}")
            else:
                print(f"   (Too many to display, showing first 5)")
                print(f"{'Port':<8} {'Address':<15} {'PID':<8} {'Process':<30}")
                print("-" * 80)
                for p in high_ports[:5]:
                    print(f"{p['port']:<8} {p['address']:<15} {p['pid']:<8} {p['process']:<30}")
        
        print(f"\n📊 Summary:")
        print(f"   Total open ports: {len(ports)}")
        print(f"   Common ports: {len(common_ports)}")
        print(f"   High ports: {len(high_ports)}")
        
    else:
        print("❌ No open ports found")
    
    print("\n" + "=" * 80)
    print("✓ Port check completed")
    print("=" * 80)

if __name__ == "__main__":
    main()
