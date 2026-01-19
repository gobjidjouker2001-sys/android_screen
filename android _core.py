import subprocess
import os

def install_android_deps():
    print("[+] جاري تثبيت متطلبات الأندرويد وكالي...")
    # تم تصحيح أسماء الحزم لتناسب تحديثات كالي الأخيرة وتجنب Error 100
    commands = [
        "sudo apt update",
        "sudo apt install -y adb scrcpy python3-pyqt6 libimobiledevice-1.0-6"
    ]
    for cmd in commands:
        try:
            subprocess.run(cmd.split(), check=True)
        except:
            print(f"[!] خطأ في تنفيذ: {cmd}")

class AndroidCore:
    def __init__(self):
        self.adb_path = "adb"

    def get_devices(self):
        """التحقق من الأجهزة المتصلة عبر ADB"""
        try:
            output = subprocess.check_output([self.adb_path, "devices"]).decode()
            devices = [line.split('\t')[0] for line in output.splitlines() if '\tdevice' in line]
            return devices
        except:
            return []

    def start_mirror(self):
        """بدء عرض الشاشة باستخدام Scrcpy"""
        subprocess.Popen(["scrcpy", "--always-on-top", "--window-title", "شاشة الأندرويد"])

    def kill_adb(self):
        subprocess.run([self.adb_path, "kill-server"])
