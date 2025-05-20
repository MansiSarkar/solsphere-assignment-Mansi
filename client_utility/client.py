import platform
import subprocess
import requests
import time
import psutil
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox,ttk


# ================== 1. DISK ENCRYPTION STATUS ==================
def show_security_warnings(data):
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    warnings = []
    if not data["disk_encryption"]:
        warnings.append("Disk Encryption is OFF!")
    if data["antivirus"] == False:
        warnings.append("Antivirus is DISABLED!")
    if not data["sleep_settings"]:
        warnings.append("Inactivity Sleep Setting is not configured.")

    if warnings:
        messagebox.showwarning("⚠️ System Security Alert", "\n".join(warnings))

def check_disk_encryption():
    os_name = platform.system()
    if os_name == "Windows":
        try:
            result = subprocess.run(["manage-bde", "-status", "C:"], capture_output=True, text=True)
            return "Percentage Encrypted: 100%" in result.stdout
        except:
            return False
    elif os_name == "Darwin":  # macOS
        try:
            result = subprocess.run(["fdesetup", "status"], capture_output=True, text=True)
            return "FileVault is On" in result.stdout
        except:
            return False
    elif os_name == "Linux":
        try:
            result = subprocess.run(["lsblk", "-o", "NAME,TYPE"], capture_output=True, text=True)
            return "crypt" in result.stdout
        except:
            return False
    return False

# ================== 2. OS UPDATES STATUS ==================
def check_os_updates():
    os_name = platform.system()
    try:
        if os_name == "Windows":
            result = subprocess.run(["powershell", "Get-WindowsUpdate"], capture_output=True, text=True)
            return "No updates available" in result.stdout or "0 updates" in result.stdout
        elif os_name == "Darwin":
            result = subprocess.run(["softwareupdate", "-l"], capture_output=True, text=True)
            return "No new software available." in result.stdout
        elif os_name == "Linux":
            result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
            return "upgradable from" not in result.stdout
    except:
        return False
    return False

# ================== 3. ANTIVIRUS STATUS ==================
def check_antivirus():
    os_name = platform.system()
    if os_name == "Windows":
        try:
            result = subprocess.run(["powershell", "(Get-MpComputerStatus).AntivirusEnabled"], capture_output=True, text=True)
            return "True" in result.stdout
        except:
            return False
    elif os_name == "Darwin" or os_name == "Linux":
        # Many UNIX systems don't have default antivirus
        return "N/A"
    return False

# ================== 4. INACTIVITY SLEEP SETTINGS ==================
def check_sleep_settings():
    os_name = platform.system()
    try:
        if os_name == "Windows":
            result = subprocess.run(["powercfg", "-query"], capture_output=True, text=True)
            return "Sleep" in result.stdout
        elif os_name == "Darwin":
            result = subprocess.run(["pmset", "-g"], capture_output=True, text=True)
            return "sleep" in result.stdout
        elif os_name == "Linux":
            result = subprocess.run(["gsettings", "get", "org.gnome.settings-daemon.plugins.power", "sleep-inactive-ac-timeout"], capture_output=True, text=True)
            return "0" not in result.stdout
    except:
        return False
    return False

# ================== 5. COLLECT ALL DATA ==================
def show_gui(data):
    root = tk.Tk()
    root.title("🔐 Solsphere Security & Health Status")
    root.geometry("400x400")
    root.resizable(False, False)

    heading = ttk.Label(root, text="System Status", font=("Arial", 16, "bold"))
    heading.pack(pady=10)

    # Function to create status labels
    def add_status(name, status):
        color = "green" if status is True or status == "N/A" else "red"
        text = f"✅ {name}" if color == "green" else f"❌ {name}"
        label = ttk.Label(root, text=text, font=("Arial", 12))
        label.pack()
        label.configure(foreground=color)

    # Add statuses
    add_status("Disk Encryption", data["disk_encryption"])
    add_status("OS Updates", data["os_updates"])
    add_status("Antivirus", data["antivirus"])
    add_status("Sleep Settings", data["sleep_settings"])

    # CPU and Memory usage
    cpu = f"CPU Usage: {data['cpu_usage']}%"
    mem = f"RAM Used: {data['memory']['percent']}%"

    ttk.Label(root, text=cpu, font=("Arial", 12)).pack(pady=5)
    ttk.Label(root, text=mem, font=("Arial", 12)).pack()

    ttk.Label(root, text=f"Platform: {data['platform']}", font=("Arial", 10, "italic")).pack(pady=10)

    # Exit button
    ttk.Button(root, text="Close", command=root.destroy).pack(pady=10)

    root.mainloop()

def collect_data():
    data = {
        "disk_encryption": check_disk_encryption(),
        "os_updates": check_os_updates(),
        "antivirus": check_antivirus(),
        "sleep_settings": check_sleep_settings(),
        "platform": platform.system(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
    }
    return data

# ================== 6. SEND DATA TO SERVER ==================
def send_to_server(data):
    # REPLACE THIS WITH THE ACTUAL API ENDPOINT
    url = "https://example.com/api/system-report"

    try:
        response = requests.post(url, json=data)
        print(f"Sent: {response.status_code}")
    except Exception as e:
        print("Error sending data:", e)

# ================== 7. MAIN LOOP (EVERY 30 MINS) ==================

def log_data_to_file(data):
    log_file = "system_log.txt"
    with open(log_file, "a") as f:
        f.write(f"\n--- {datetime.now()} ---\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")

def main():
    print("Starting Solsphere System Client...")
    old_data = {}
    #show_gui(new_data)
    while True:
        new_data = collect_data()
        log_data_to_file(new_data)
        #show_security_warnings(new_data)
        if new_data != old_data:
            send_to_server(new_data)
            old_data = new_data
        else:
            print("No changes. Skipping send.")
        time.sleep(1800)  # Sleep for 30 minutes


if __name__ == "__main__":
    main()
