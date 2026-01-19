import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLabel, QHBoxLayout, QFrame)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QTimer
from android_core import AndroidCore, install_android_deps

class AndroidMirrorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        install_android_deps() # تثبيت المتطلبات تلقائياً
        self.core = AndroidCore()
        self.init_ui()
        
        # موقت لفحص الاتصال كل ثانيتين
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)

    def init_ui(self):
        self.setWindowTitle("Kali Android Mirror - Pro")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #121212; color: white;")

        central_widget = QWidget()
        layout = QVBoxLayout()

        # --- اللوجو والعنوان ---
        header = QHBoxLayout()
        self.logo = QLabel()
        pix = QPixmap("logo.png")
        if not pix.isNull():
            self.logo.setPixmap(pix.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        
        self.title = QLabel("Android Screen Mirror")
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50;")
        
        header.addWidget(self.logo)
        header.addWidget(self.title)
        header.addStretch()
        layout.addLayout(header)

        # --- الحالة ---
        self.status_label = QLabel("الحالة: جاري البحث عن أجهزة...")
        self.status_label.setStyleSheet("color: #ff9800; padding: 10px;")
        layout.addWidget(self.status_label)

        # --- الأزرار ---
        self.btn_mirror = QPushButton("▶ بدء عرض الشاشة")
        self.btn_mirror.setEnabled(False)
        self.btn_mirror.setStyleSheet("""
            QPushButton { background-color: #1b5e20; padding: 15px; border-radius: 5px; font-weight: bold; }
            QPushButton:disabled { background-color: #333; color: #777; }
        """)
        self.btn_mirror.clicked.connect(self.core.start_mirror)
        
        self.btn_fix = QPushButton("🔧 إعادة ضبط ADB")
        self.btn_fix.clicked.connect(self.core.kill_adb)

        layout.addWidget(self.btn_mirror)
        layout.addWidget(self.btn_fix)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_status(self):
        devices = self.core.get_devices()
        if devices:
            self.status_label.setText(f"✅ تم اكتشاف جهاز: {devices[0]}")
            self.status_label.setStyleSheet("color: #4CAF50;")
            self.btn_mirror.setEnabled(True)
        else:
            self.status_label.setText("❌ لا يوجد جهاز متصل (فعل تصحيح USB)")
            self.status_label.setStyleSheet("color: #f44336;")
            self.btn_mirror.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AndroidMirrorGUI()
    window.show()
    sys.exit(app.exec())
