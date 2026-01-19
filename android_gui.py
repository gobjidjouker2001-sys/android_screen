import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QPushButton, QLabel, QHBoxLayout, QFrame)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer

# استيراد المحرك (تأكد من وجود android_core.py في نفس المجلد)
try:
    from android_core import AndroidEngine, install_logic
except ImportError:
    print("[!] خطأ: لم يتم العثور على ملف android_core.py بجانب هذا الملف!")
    sys.exit()

class AndroidApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # تنفيذ التثبيت التلقائي للأدوات الجانبية فور تشغيل الواجهة
        install_logic()
        
        self.engine = AndroidEngine()
        self.init_ui()

        # موقت لتحديث حالة الاتصال تلقائياً
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(2000)

    def init_ui(self):
        self.setWindowTitle("Kali Android Mirror - Auto Setup")
        self.setFixedSize(550, 350)
        self.setStyleSheet("background-color: #121212; color: #ffffff;")

        central_widget = QWidget()
        layout = QVBoxLayout()

        # الهيدر واللوجو
        header = QHBoxLayout()
        self.logo = QLabel()
        if os.path.exists("logo.png"):
            self.logo.setPixmap(QPixmap("logo.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))
        
        title_label = QLabel("نظام عرض شاشة الأندرويد")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.addWidget(self.logo)
        header.addWidget(title_label)
        header.addStretch()
        layout.addLayout(header)

        # منطقة الحالة
        self.status_box = QLabel("جاري فحص اتصال USB...")
        self.status_box.setStyleSheet("background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #333;")
        self.status_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_box)

        # الأزرار
        self.btn_run = QPushButton("▶ ابدأ عرض الشاشة الآن")
        self.btn_run.setEnabled(False)
        self.btn_run.setStyleSheet("""
            QPushButton { background-color: #2e7d32; padding: 15px; border-radius: 5px; font-weight: bold; }
            QPushButton:disabled { background-color: #424242; color: #888; }
        """)
        self.btn_run.clicked.connect(self.engine.start_mirror)
        layout.addWidget(self.btn_run)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_status(self):
        devices = self.engine.get_devices()
        if devices:
            self.status_box.setText(f"✅ تم اكتشاف الجهاز: {devices[0]}\nالأدوات الثانوية جاهزة للعمل.")
            self.status_box.setStyleSheet("background-color: #1b5e20; padding: 20px; border-radius: 10px;")
            self.btn_run.setEnabled(True)
        else:
            self.status_box.setText("❌ لا يوجد جهاز متصل\nتأكد من تفعيل USB Debugging في الهاتف")
            self.status_box.setStyleSheet("background-color: #c62828; padding: 20px; border-radius: 10px;")
            self.btn_run.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AndroidApp()
    window.show()
    sys.exit(app.exec())
