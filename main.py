#!/usr/bin/env python3
"""
============================================================
KIOSBANK Management GUI - Professional Edition
Unified interface untuk menjalankan semua tools KIOSBANK
============================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import queue
import sys
import os
import platform
from datetime import datetime

# ==================== THEME CONFIGURATION ====================
THEME = {
    "bg_main": "#F3F4F6",          # Light gray background
    "bg_header": "#1F2937",        # Dark blue-gray for header
    "bg_output": "#111827",        # Very dark gray for terminal
    "text_header": "#F9FAFB",      # Checking white
    "text_primary": "#374151",     # Dark gray text
    "accent_color": "#2563EB",     # Professional Blue
    "accent_hover": "#1D4ED8",     # Darker Blue
    "success": "#10B981",          # Green
    "warning": "#F59E0B",          # Amber
    "danger": "#EF4444",           # Red
    "white": "#FFFFFF",
    
    # Terminal Colors (Bootstrap-like)
    "term_default": "#D1D5DB",     # Gray-300 (Basic Text)
    "term_success": "#2ECC71",     # Emerald (Success)
    "term_warning": "#F1C40F",     # Sunflower (Warning)
    "term_danger": "#E74C3C",      # Alizarin (Error)
    "term_info": "#3498DB",        # Peter River (Info)
    
    "font_header": ("Segoe UI", 16, "bold"),
    "font_subheader": ("Segoe UI", 10),
    "font_button": ("Segoe UI", 10, "bold"),
    "font_desc": ("Segoe UI", 8),
    "font_terminal": ("Consolas", 10),
}

class ModernButton(tk.Button):
    """Custom Button dengan Hover EffectModern"""
    def __init__(self, master, **kwargs):
        self.default_bg = kwargs.get('bg', THEME['accent_color'])
        self.hover_bg = kwargs.pop('hover_bg', THEME['accent_hover'])
        
        kwargs.setdefault('font', THEME['font_button'])
        kwargs.setdefault('fg', THEME['white'])
        kwargs.setdefault('relief', tk.FLAT)
        kwargs.setdefault('pady', 8)
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('cursor', 'hand2')
        
        super().__init__(master, **kwargs)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['bg'] = self.hover_bg
        
    def on_leave(self, e):
        self['bg'] = self.default_bg

class KiosbankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("KIOSBANK Management Console")
        self.root.geometry("950x750")
        self.root.minsize(900, 700)
        self.root.configure(bg=THEME['bg_main'])
        
        # Queue & State
        self.output_queue = queue.Queue()
        self.current_process = None
        self.is_running = False
        self.tunnel_process = None  # Track SSH tunnel process
        
        self.setup_ui()
        self.check_queue()
        
    def setup_ui(self):
        # ==================== HEADER ====================
        header_frame = tk.Frame(self.root, bg=THEME['bg_header'], height=80, pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        # Title Container
        title_container = tk.Frame(header_frame, bg=THEME['bg_header'])
        title_container.pack(anchor="w")
        
        title_label = tk.Label(
            title_container, 
            text="KIOSBANK MANAGER", 
            font=THEME['font_header'],
            bg=THEME['bg_header'], 
            fg=THEME['text_header']
        )
        title_label.pack(anchor="w")
        
        subtitle_label = tk.Label(
            title_container,
            text="Integrated VPS Gateway & API Management Tool",
            font=THEME['font_subheader'],
            bg=THEME['bg_header'],
            fg="#9CA3AF"
        )
        subtitle_label.pack(anchor="w")
        
        # ==================== MAIN CONTENT AREA ====================
        main_container = tk.Frame(self.root, bg=THEME['bg_main'], padx=25, pady=25)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # --- LEFT PANEL: CONTROLS ---
        left_panel = tk.Frame(main_container, bg=THEME['bg_main'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Group: Core Operations
        self.create_card(left_panel, "CORE OPERATIONS", [
            {
                'name': '🔐 Sign-On VPS',
                'script': 'app/signon_vps.py',
                'desc': 'Establish session with Kiosbank API',
                'color': THEME['accent_color']
            },
            {
                'name': '🚇 Start Tunnel',
                'script': 'app/start_ssh_tunnel.py',
                'desc': 'Open secure SOCKS5 tunnel',
                'color': THEME['accent_color'],
                'separate_window': True  # Run in separate terminal
            },
            {
                'name': '⏹ Stop Tunnel',
                'action': 'stop_tunnel',
                'desc': 'Close SSH tunnel window',
                'color': THEME['danger'],
                'hover': '#DC2626'
            }
        ])
        
        tk.Frame(left_panel, height=20, bg=THEME['bg_main']).pack() # Spacer

        # Group: Diagnostics
        self.create_card(left_panel, "DIAGNOSTICS & CHECKS", [
            {
                'name': '🌐 Check IP Address',
                'script': 'app/check_ip.py',
                'desc': 'Verify current public IP',
                'color': '#4B5563', 
                'hover': '#374151'
            },
            {
                'name': '🔌 Check Port Status',
                'script': 'app/cekport_gui.py',
                'desc': 'Analyze open ports & proxy',
                'color': '#4B5563',
                'hover': '#374151'
            },
            {
                'name': '✅ Verify Environment',
                'script': 'app/verify_env.py',
                'desc': 'Validate .env configuration',
                'color': '#059669',
                'hover': '#047857'
            }
        ])

        # --- RIGHT PANEL: OUTPUT ---
        right_panel = tk.Frame(main_container, bg=THEME['bg_main'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Output Header (Controls)
        output_controls = tk.Frame(right_panel, bg=THEME['bg_main'], pady=5)
        output_controls.pack(fill=tk.X)
        
        lbl_console = tk.Label(
            output_controls, 
            text="CONSOLE OUTPUT", 
            font=("Segoe UI", 9, "bold"), 
            fg=THEME['text_primary'], 
            bg=THEME['bg_main']
        )
        lbl_console.pack(side=tk.LEFT, pady=5)

        # Action Buttons (Small)
        btn_frame = tk.Frame(output_controls, bg=THEME['bg_main'])
        btn_frame.pack(side=tk.RIGHT)

        self.stop_btn = tk.Button(
            btn_frame, text="⏹ STOP", command=self.stop_process,
            bg=THEME['danger'], fg="white", font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT, state=tk.DISABLED, padx=10, cursor="hand2"
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text="🗑 CLEAR", command=self.clear_output,
            bg="white", fg=THEME['text_primary'], font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT, bd=1, padx=10, cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)

        # Terminal Area
        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=THEME['font_terminal'],
            bg=THEME['bg_output'],
            fg=THEME['term_default'], # Default Light Gray
            insertbackground="white",
            bd=0,
            padx=15,
            pady=15,
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure Terminal Color Tags
        self.output_text.tag_config("success", foreground=THEME['term_success'])
        self.output_text.tag_config("warning", foreground=THEME['term_warning'])
        self.output_text.tag_config("danger", foreground=THEME['term_danger'])
        self.output_text.tag_config("info", foreground=THEME['term_info'])
        self.output_text.tag_config("highlight", foreground="#F39C12") # Special highlight
        
        # ==================== STATUS BAR ====================
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=("Segoe UI", 9),
            bg="#E5E7EB",
            fg=THEME['text_primary'],
            pady=8,
            padx=20,
            anchor="w"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_card(self, parent, title, buttons):
        """Helper untuk membuat group tombol"""
        frame = tk.Frame(parent, bg="white", padx=1, pady=1) # Border effect
        frame.pack(fill=tk.X, pady=5)
        
        inner = tk.Frame(frame, bg="white", padx=15, pady=15)
        inner.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            inner, text=title, font=("Segoe UI", 8, "bold"),
            fg="#9CA3AF", bg="white"
        ).pack(anchor="w", pady=(0, 10))
        
        for btn_data in buttons:
            btn_frame = tk.Frame(inner, bg="white", pady=2)
            btn_frame.pack(fill=tk.X, pady=3)
            
            # Determine command based on action or script
            if 'action' in btn_data:
                cmd = lambda s=btn_data: self.handle_action(s['action'])
            else:
                cmd = lambda s=btn_data: self.run_script(s)
            
            ModernButton(
                btn_frame,
                text=btn_data['name'],
                command=cmd,
                bg=btn_data.get('color', THEME['accent_color']),
                hover_bg=btn_data.get('hover'),
                width=20
            ).pack(side=tk.LEFT, fill=tk.Y)
            
            tk.Label(
                btn_frame,
                text=btn_data['desc'],
                font=THEME['font_desc'],
                fg="#6B7280",
                bg="white"
            ).pack(side=tk.LEFT, padx=10)

    def append_output(self, text, color=None):
        """Append text ke output area dengan smart highlighting"""
        self.output_text.config(state=tk.NORMAL)
        
        tag = None
        
        if color:
             # Custom color passed directly
             tag_name = f"color_{color}"
             self.output_text.tag_config(tag_name, foreground=color)
             tag = tag_name
        else:
            # Auto-detect syntax highlighting based on text content
            text_lower = text.lower()
            
            if any(k in text for k in ["❌", "FAILED", "ERROR", "gagal", "ConnectionError", "Exception"]):
                tag = "danger"
            elif any(k in text for k in ["⚠️", "WARNING", "Warning", "check", "Checking", "Troubleshooting"]):
                tag = "warning"
            elif any(k in text for k in ["✅", "✓", "SUCCESS", "MATCH", "OPEN", "berhasil", "connected"]):
                tag = "success"
            elif any(k in text for k in ["ℹ️", "Starting", "Executing", "Process", "Running"]):
                tag = "info"
            elif "=" * 10 in text: # Highlight separator lines
                tag = "info"
        
        if tag:
            self.output_text.insert(tk.END, text, tag)
        else:
            self.output_text.insert(tk.END, text)
        
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.update_status("Output cleared")

    def update_status(self, message, status_type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Consistent status styling
        bg_color = "#E5E7EB"
        fg_color = THEME['text_primary']
        
        if status_type == "running":
            bg_color = THEME['accent_color']
            fg_color = "white"
        elif status_type == "success":
            bg_color = THEME['success']
            fg_color = "white"
        elif status_type == "error":
            bg_color = THEME['danger']
            fg_color = "white"
            
        self.status_bar.config(text=f"[{timestamp}] {message}", bg=bg_color, fg=fg_color)

    def run_script(self, script_info):
        # Check if this should run in separate window (for SSH tunnel)
        if script_info.get('separate_window', False):
            self.run_in_separate_window(script_info)
            return
        
        if self.is_running:
            self.append_output("\n⚠️  Process is already running! Please wait.\n\n", THEME['warning'])
            return
        
        self.is_running = True
        self.stop_btn.config(state=tk.NORMAL, bg=THEME['danger'])
        
        self.clear_output()
        self.append_output(f"🚀 EXECUTING: {script_info['name']}...\n", THEME['accent_color'])
        self.append_output(f"📂 File: {script_info['script']}\n", "#6B7280")
        self.append_output("-" * 60 + "\n", "#374151")
        
        self.update_status(f"Running {script_info['name']}...", "running")
        
        thread = threading.Thread(
            target=self.execute_script,
            args=(script_info['script'],),
            daemon=True
        )
        thread.start()

    def run_in_separate_window(self, script_info):
        """Run script in a separate terminal window (for long-running processes like SSH tunnel)"""
        try:
            script_name = script_info['script']
            
            # Check if tunnel is already running
            if self.tunnel_process and self.tunnel_process.poll() is None:
                self.append_output("\n⚠️  SSH Tunnel is already running in a separate window!\n", THEME['warning'])
                self.append_output("Close the tunnel window first or use 'Stop Tunnel' button.\n\n")
                return
            
            self.clear_output()
            self.append_output(f"🚀 LAUNCHING: {script_info['name']} in separate window...\n", THEME['accent_color'])
            self.append_output(f"📂 File: {script_name}\n", "#6B7280")
            self.append_output("-" * 60 + "\n", "#374151")
            self.append_output("\n✅ Tunnel window opened successfully!\n", THEME['success'])
            self.append_output("ℹ️  The SSH tunnel is now running in a separate terminal window.\n", THEME['term_info'])
            self.append_output("ℹ️  You can continue using other menu options in this GUI.\n", THEME['term_info'])
            self.append_output("ℹ️  To stop the tunnel, click 'Stop Tunnel' or close the terminal window.\n\n", THEME['term_info'])
            
            # Windows: Use CREATE_NEW_CONSOLE flag
            if platform.system() == "Windows":
                CREATE_NEW_CONSOLE = 0x00000010
                self.tunnel_process = subprocess.Popen(
                    [sys.executable, script_name],
                    creationflags=CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac: Use terminal emulator
                terminal_commands = [
                    ['gnome-terminal', '--', sys.executable, script_name],
                    ['xterm', '-e', sys.executable, script_name],
                    ['konsole', '-e', sys.executable, script_name],
                ]
                
                for cmd in terminal_commands:
                    try:
                        self.tunnel_process = subprocess.Popen(cmd)
                        break
                    except FileNotFoundError:
                        continue
                else:
                    raise Exception("No suitable terminal emulator found")
            
            self.update_status("SSH Tunnel running in separate window", "success")
            
        except Exception as e:
            self.append_output(f"\n❌ ERROR: Failed to open separate window\n", THEME['danger'])
            self.append_output(f"Details: {str(e)}\n\n")
            self.update_status("Failed to start tunnel", "error")

    def handle_action(self, action_name):
        """Handle special actions (not script execution)"""
        if action_name == 'stop_tunnel':
            self.stop_tunnel()
        else:
            self.append_output(f"\n⚠️  Unknown action: {action_name}\n", THEME['warning'])

    def stop_tunnel(self):
        """Stop the SSH tunnel running in separate window"""
        if not self.tunnel_process or self.tunnel_process.poll() is not None:
            self.clear_output()
            self.append_output("ℹ️  No active SSH tunnel found.\n", THEME['term_info'])
            self.append_output("The tunnel may have already been closed.\n\n")
            self.update_status("No active tunnel", "info")
            return
        
        try:
            self.clear_output()
            self.append_output("⏹ Stopping SSH Tunnel...\n", THEME['warning'])
            
            # Terminate the tunnel process
            self.tunnel_process.terminate()
            
            # Wait for process to end (with timeout)
            try:
                self.tunnel_process.wait(timeout=3)
                self.append_output("✅ SSH Tunnel stopped successfully!\n", THEME['success'])
                self.update_status("Tunnel stopped", "success")
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                self.tunnel_process.kill()
                self.append_output("⚠️  Tunnel forcefully terminated.\n", THEME['warning'])
                self.update_status("Tunnel killed", "warning")
            
            self.tunnel_process = None
            
        except Exception as e:
            self.append_output(f"\n❌ ERROR: Failed to stop tunnel\n", THEME['danger'])
            self.append_output(f"Details: {str(e)}\n\n")
            self.update_status("Failed to stop tunnel", "error")


    def execute_script(self, script_name):
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            
            self.current_process = subprocess.Popen(
                [sys.executable, '-u', script_name],
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
            
            for line in self.current_process.stdout:
                self.output_queue.put(("output", line))
            
            return_code = self.current_process.wait()
            
            if return_code == 0:
                self.output_queue.put(("status", "success"))
            else:
                self.output_queue.put(("status", "error"))
                
        except Exception as e:
            self.output_queue.put(("output", f"\n❌ SYSTEM ERROR: {str(e)}\n"))
            self.output_queue.put(("status", "error"))
        finally:
            self.current_process = None
            self.is_running = False
            self.output_queue.put(("finished", None))

    def stop_process(self):
        if self.current_process:
            self.current_process.terminate()
            self.append_output("\n⏹ PROCESS TERMINATED BY USER\n", THEME['danger'])
            self.stop_btn.config(state=tk.DISABLED)

    def check_queue(self):
        try:
            while True:
                msg_type, data = self.output_queue.get_nowait()
                if msg_type == "output":
                    self.append_output(data)
                elif msg_type == "status":
                    if data == "success":
                        self.append_output("\n✨ SUCCESS: Operation completed successfully.\n", THEME['success'])
                        self.update_status("Operation completed", "success")
                    elif data == "error":
                        self.append_output("\n💀 FAILED: Operation encountered errors.\n", THEME['danger'])
                        self.update_status("Operation failed", "error")
                elif msg_type == "finished":
                    self.stop_btn.config(state=tk.DISABLED)
                    # Reset status bar after delay if success/error
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = KiosbankGUI(root)
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2) 
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.mainloop()
