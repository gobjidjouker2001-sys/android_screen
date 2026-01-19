import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLabel, QHBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

# استيراد المحرك (تأكد من وجود android_core.py في نفس المكان)
try:
    from android_core import AndroidCore, install_android_deps
except ImportError:
    print("[!] خطأ: ملف android_core.py غير موجود في هذا المجلد!")
    sys.exit()

class AndroidMirrorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        install_android_deps() # تثبيت التبعيات تلقائياً
        self.core = AndroidCore()
        self.init_ui()
        
        # موقت لفحص الاتصال كل ثانيتين
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)

    def init_ui(self):
        self.setWindowTitle("أداة عرض شاشة الأندرويد - كالي")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #121212; color: white;")

        central_widget = QWidget()
        layout = QVBoxLayout()

        # العنوان واللوجو
        header = QHBoxLayout()
        self.logo = QLabel()
        if os.path.exists("logo.png"):
            self.logo.setPixmap(QPixmap("logo.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        header.addWidget(self.logo)
        header.addWidget(QLabel("Android Screen Mirror"))
        layout.addLayout(header)

        self.status_label = QLabel("الحالة: جاري البحث عن أجهزة...")
        layout.addWidget(self.status_label)

        self.btn_mirror = QPushButton("▶ بدء عرض الشاشة")
        self.btn_mirror.setEnabled(False)
        self.btn_mirror.setStyleSheet("background-color: #1b5e20; padding: 15px; font-weight: bold;")
        self.btn_mirror.clicked.connect(self.core.start_mirror)
        
        layout.addWidget(self.btn_mirror)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_status(self):
        devices = self.core.get_devices()
        if devices:
            self.status_label.setText(f"✅ تم اكتشاف جهاز: {devices[0]}")
            self.btn_mirror.setEnabled(True)
        else:
            self.status_label.setText("❌ لا يوجد جهاز (تأكد من تفعيل USB Debugging)")
            self.btn_mirror.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AndroidMirrorGUI()
    window.show()
    sys.exit(app.exec())
