#!/usr/bin/env python3
"""
============================================================
KIOSBANK Management CLI - VPS Edition
Command-line interface untuk menjalankan semua tools KIOSBANK
Cocok untuk VPS headless (tanpa GUI)
============================================================
"""

import subprocess
import sys
import os
import platform
from datetime import datetime

# Configure UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ==================== COLOR CODES ====================
class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Background colors
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_RED = '\033[41m'

# ==================== HELPER FUNCTIONS ====================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print application header"""
    clear_screen()
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'KIOSBANK MANAGEMENT CONSOLE - CLI VERSION':^60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.CYAN}Integrated VPS Gateway & API Management Tool{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_separator(char='-', length=60):
    """Print separator line"""
    print(f"{Colors.CYAN}{char * length}{Colors.ENDC}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def print_menu():
    """Print main menu"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}CORE OPERATIONS:{Colors.ENDC}")
    print(f"{Colors.GREEN}  1.{Colors.ENDC} 🔐 Sign-On VPS          - Establish session with Kiosbank API")
    print(f"{Colors.GREEN}  2.{Colors.ENDC} 🚇 Start SSH Tunnel     - Open secure SOCKS5 tunnel")
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}DIAGNOSTICS & CHECKS:{Colors.ENDC}")
    print(f"{Colors.GREEN}  3.{Colors.ENDC} 🌐 Check IP Address     - Verify current public IP")
    print(f"{Colors.GREEN}  4.{Colors.ENDC} 🔌 Check Port Status    - Analyze open ports & proxy")
    print(f"{Colors.GREEN}  5.{Colors.ENDC} ✅ Verify Environment   - Validate .env configuration")
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}SYSTEM:{Colors.ENDC}")
    print(f"{Colors.GREEN}  6.{Colors.ENDC} 📊 System Information   - Display system info")
    print(f"{Colors.RED}  0.{Colors.ENDC} 🚪 Exit                 - Quit application")
    
    print_separator()

def get_user_choice():
    """Get user menu choice"""
    try:
        choice = input(f"\n{Colors.BOLD}{Colors.CYAN}Pilih menu [0-6]: {Colors.ENDC}").strip()
        return choice
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program dihentikan oleh user.{Colors.ENDC}")
        sys.exit(0)

def run_script(script_path, script_name):
    """
    Run a Python script and display output in real-time
    
    Args:
        script_path: Path to the script
        script_name: Display name of the script
    """
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}🚀 EXECUTING: {script_name}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.CYAN}📂 File: {script_path}{Colors.ENDC}")
    print_separator()
    print()
    
    try:
        # Configure environment for UTF-8
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'
        
        # Run script and capture output in real-time
        process = subprocess.Popen(
            [sys.executable, '-u', script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=env,
            encoding='utf-8',
            errors='replace'
        )
        
        # Print output in real-time
        for line in process.stdout:
            print(line, end='')
        
        # Wait for process to complete
        return_code = process.wait()
        
        print()
        print_separator()
        
        if return_code == 0:
            print_success("Operation completed successfully!")
        else:
            print_error(f"Operation failed with exit code: {return_code}")
        
        return return_code
        
    except FileNotFoundError:
        print_error(f"Script not found: {script_path}")
        print_info("Make sure the script exists in the correct location.")
        return 1
    except Exception as e:
        print_error(f"Error executing script: {str(e)}")
        return 1

def show_system_info():
    """Display system information"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}📊 SYSTEM INFORMATION{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")
    
    info = {
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Platform": platform.platform(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
        "Python Version": platform.python_version(),
        "Python Implementation": platform.python_implementation(),
        "Current Directory": os.getcwd(),
        "Script Location": os.path.dirname(os.path.abspath(__file__)),
        "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    max_key_length = max(len(key) for key in info.keys())
    
    for key, value in info.items():
        print(f"{Colors.CYAN}{key.ljust(max_key_length)}{Colors.ENDC} : {Colors.GREEN}{value}{Colors.ENDC}")
    
    print_separator()

def pause():
    """Pause and wait for user input"""
    try:
        input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
    except KeyboardInterrupt:
        print()

def confirm_exit():
    """Confirm before exiting"""
    try:
        choice = input(f"\n{Colors.YELLOW}Are you sure you want to exit? (y/n): {Colors.ENDC}").strip().lower()
        return choice in ['y', 'yes']
    except KeyboardInterrupt:
        return True

# ==================== MENU HANDLERS ====================

def handle_signon_vps():
    """Handle Sign-On VPS menu"""
    run_script('app/signon_vps.py', 'Sign-On VPS')
    pause()

def handle_start_tunnel():
    """Handle Start SSH Tunnel menu"""
    print_warning("SSH Tunnel will run in the foreground.")
    print_info("Press Ctrl+C to stop the tunnel.")
    print_info("Or run in background with: nohup python app/start_ssh_tunnel.py &")
    print()
    
    choice = input(f"{Colors.CYAN}Continue? (y/n): {Colors.ENDC}").strip().lower()
    if choice in ['y', 'yes']:
        run_script('app/start_ssh_tunnel.py', 'Start SSH Tunnel')
    else:
        print_info("Cancelled.")
    pause()

def handle_check_ip():
    """Handle Check IP Address menu"""
    run_script('app/check_ip.py', 'Check IP Address')
    pause()

def handle_check_port():
    """Handle Check Port Status menu"""
    run_script('app/cekport_gui.py', 'Check Port Status')
    pause()

def handle_verify_env():
    """Handle Verify Environment menu"""
    run_script('app/verify_env.py', 'Verify Environment')
    pause()

def handle_system_info():
    """Handle System Information menu"""
    show_system_info()
    pause()

# ==================== MAIN PROGRAM ====================

def main():
    """Main program loop"""
    
    # Menu handlers mapping
    menu_handlers = {
        '1': handle_signon_vps,
        '2': handle_start_tunnel,
        '3': handle_check_ip,
        '4': handle_check_port,
        '5': handle_verify_env,
        '6': handle_system_info,
    }
    
    while True:
        try:
            print_header()
            print_menu()
            
            choice = get_user_choice()
            
            if choice == '0':
                if confirm_exit():
                    clear_screen()
                    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.ENDC}")
                    print(f"{Colors.BOLD}{Colors.GREEN}Thank you for using KIOSBANK Management Console!{Colors.ENDC}")
                    print(f"{Colors.BOLD}{Colors.GREEN}{'='*60}{Colors.ENDC}\n")
                    sys.exit(0)
                else:
                    continue
            
            elif choice in menu_handlers:
                handler = menu_handlers[choice]
                handler()
            
            else:
                print_error("Invalid choice! Please select 0-6.")
                pause()
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Program interrupted by user.{Colors.ENDC}")
            if confirm_exit():
                sys.exit(0)
        
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}")
            pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Program terminated.{Colors.ENDC}")
        sys.exit(0)
