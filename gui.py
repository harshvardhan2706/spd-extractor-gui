import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QTextEdit, QSplashScreen
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
import extractor
from pathlib import Path

class ExtractThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            self.progress.emit("Starting extraction...")

            base_folder = QFileDialog.getExistingDirectory(
                None, "Select Destination Folder"
            )
            if not base_folder:
                self.progress.emit("❌ Extraction cancelled (no folder selected).")
                return

            file_name = Path(self.file_path).stem
            output_dir = os.path.join(base_folder, f"{file_name}_extracted")
            os.makedirs(output_dir, exist_ok=True)

            extractor.extract_spd(self.file_path, output_dir)

            self.progress.emit("✅ Extraction completed successfully!")
            self.finished.emit(output_dir)
        except Exception as e:
            self.progress.emit(f"❌ Error: {str(e)}")

class SPDExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roland SPD Extractor")
        self.setGeometry(500, 200, 500, 350)
        self.setWindowIcon(QIcon.fromTheme("folder-music"))

        layout = QVBoxLayout()

        title = QLabel("🎶 Roland SPD File Extractor")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.select_btn = QPushButton("Choose .SPD File")
        self.select_btn.setFont(QFont("Arial", 12))
        self.select_btn.clicked.connect(self.open_file)
        layout.addWidget(self.select_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select SPD File", "", "SPD Files (*.SPD);;All Files (*)")
        if file_path:
            self.thread = ExtractThread(file_path)
            self.thread.progress.connect(self.update_log)
            self.thread.finished.connect(self.show_done)
            self.thread.start()
            self.progress_bar.setValue(50)

    def update_log(self, message):
        self.log_area.append(message)
        if "completed" in message:
            self.progress_bar.setValue(100)

    def show_done(self, folder_path):
        if folder_path:
            QMessageBox.information(self, "Done", f"Files saved in:\n{folder_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Splash Screen with Logo ---
    splash_pix = QPixmap("img/spdlogo.png")  # Splash image path
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    QTimer.singleShot(3000, splash.close)  # 3 sec wait

    # After splash → main window
    window = SPDExtractorApp()
    QTimer.singleShot(3000, window.show)  # show after 3 sec

    sys.exit(app.exec_())
