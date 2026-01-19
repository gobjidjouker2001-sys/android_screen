import subprocess
import os
import sys

def install_logic():
    """
    تقوم هذه الوظيفة بتثبيت كافة الأدوات الثانوية والجانبية تلقائياً.
    تم تصحيح أسماء الحزم لتناسب تحديثات Kali الأخيرة وتجنب Error 100.
    """
    print("[+] جاري فحص وتثبيت كافة الأدوات الثانوية (Dependencies)...")
    
    # قائمة الحزم الثانوية المطلوبة للاندرويد والايفون ونظام العرض
    packages = [
        "adb",                # لتعريفات الاندرويد
        "scrcpy",             # لمحرك عرض الشاشة
        "python3-pyqt6",      # للواجهة الرسومية
        "libimobiledevice-1.0-6", # بديل الحزمة القديمة (حل مشكلة صورتك)
        "libimobiledevice-utils",
        "usbmuxd",            # لإدارة اتصال USB
        "ifuse"               # لنظام الملفات
    ]
    
    try:
        # تحديث المستودعات أولاً
        subprocess.run(["sudo", "apt", "update"], check=True)
        # تثبيت الكل في أمر واحد
        subprocess.run(["sudo", "apt", "install", "-y"] + packages, check=True)
        print("[✔] تم تثبيت كافة الأدوات الجانبية بنجاح.")
    except subprocess.CalledProcessError as e:
        print(f"[!] خطأ أثناء التثبيت التلقائي: {e}")

class AndroidEngine:
    def __init__(self):
        self.adb = "adb"

    def get_devices(self):
        """اكتشاف الأجهزة المتصلة"""
        try:
            output = subprocess.check_output([self.adb, "devices"]).decode()
            return [line.split('\t')[0] for line in output.splitlines() if '\tdevice' in line]
        except:
            return []

    def start_mirror(self):
        """بدء عرض الشاشة"""
        subprocess.Popen(["scrcpy", "--always-on-top", "--window-title", "Android Mirror Pro"])
