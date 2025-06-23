import sys
import sqlite3
import csv
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QAction, QMessageBox, QFileDialog, QInputDialog
from PyQt5.QtCore import QDate
from ui_utama import Ui_MainWindow as UiUtama
from ui_add import Ui_MainWindow as UiAdd

DB_NAME = "patients.db"

class AddWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, patient_id=None):
        super().__init__(parent)
        self.ui = UiAdd()
        self.ui.setupUi(self)

        self.patient_id = patient_id
        self.parent = parent
        self.setWindowTitle("Tambah Data")

        self.ui.comboBox.addItems(["Laki-laki", "Perempuan"])
        self.ui.pushButton.clicked.connect(self.save_data)
        self.ui.pushButton.setStyleSheet("background-color: #3498db; color: white;")

        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.setDate(QDate.currentDate())

        if self.patient_id:
            self.load_existing_data()

    def load_existing_data(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id=?", (self.patient_id,))
        data = cursor.fetchone()
        conn.close()

        if data:
            self.ui.lineEdit_2.setText(data[1])
            self.ui.lineEdit_4.setText(str(data[2]))
            self.ui.comboBox.setCurrentText(data[3])
            try:
                date_parts = list(map(int, data[4].split("-")))
                self.ui.dateEdit.setDate(QDate(date_parts[0], date_parts[1], date_parts[2]))
            except Exception:
                self.ui.dateEdit.setDate(QDate.currentDate())
            self.ui.lineEdit.setText(data[5])
            self.ui.lineEdit_5.setText(data[6])

    def save_data(self):
        nama = self.ui.lineEdit_2.text()
        umur = self.ui.lineEdit_4.text()
        gender = self.ui.comboBox.currentText()
        tanggal = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        gejala = self.ui.lineEdit.text()
        pengobatan = self.ui.lineEdit_5.text()

        if not all([nama, umur, gender, tanggal, gejala, pengobatan]):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi sebelum menyimpan data.")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if self.patient_id is not None:
            cursor.execute("""
                UPDATE patients
                SET nama_lengkap=?, umur=?, jenis_kelamin=?, tanggal_kunjungan=?, gejala=?, pengobatan=?
                WHERE id=?
            """, (nama, umur, gender, tanggal, gejala, pengobatan, self.patient_id))
        else:
            cursor.execute("""
                INSERT INTO patients (nama_lengkap, umur, jenis_kelamin, tanggal_kunjungan, gejala, pengobatan)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nama, umur, gender, tanggal, gejala, pengobatan))
        conn.commit()
        conn.close()

        self.parent.load_data()
        self.close()


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UiUtama()
        self.ui.setupUi(self)
        self.setWindowTitle("Health Record System")

        self.setup_database()
        self.load_data()

        self.ui.pushButton.clicked.connect(self.open_add_window)
        self.ui.pushButton.setStyleSheet("background-color: #3498db; color: white;")

        self.ui.pushButton_2.clicked.connect(self.delete_row)
        self.ui.pushButton_2.setStyleSheet("background-color: #e74c3c; color: white;")

        self.ui.lineEdit.textChanged.connect(self.search_data)
        self.ui.tableWidget.cellDoubleClicked.connect(self.edit_row)

        self.ui.pushButton_export.clicked.connect(self.export_csv)
        self.ui.pushButton_export.setStyleSheet("background-color: #2ecc71; color: white;")

        self.createMenuBar()
        self.statusBar().showMessage("Safira Dwirizqia - F1D022096")

    def setup_database(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_lengkap TEXT,
                umur INTEGER,
                jenis_kelamin TEXT,
                tanggal_kunjungan TEXT,
                gejala TEXT,
                pengobatan TEXT
            )
        """)
        conn.commit()
        conn.close()

    def load_data(self):
        self.ui.tableWidget.setRowCount(0)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        for row_data in cursor.fetchall():
            row_pos = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_pos)
            for col, data in enumerate(row_data):
                self.ui.tableWidget.setItem(row_pos, col, QtWidgets.QTableWidgetItem(str(data)))
        conn.close()

    def open_add_window(self):
        self.add_win = AddWindow(self)
        self.add_win.show()

    def edit_row(self, row, column):
        if column == 0:
            return
        patient_id = int(self.ui.tableWidget.item(row, 0).text())
        field_name = self.ui.tableWidget.horizontalHeaderItem(column).text()
        current_value = self.ui.tableWidget.item(row, column).text()
        new_value, ok = QInputDialog.getText(self, f"Edit {field_name}", f"{field_name}:", text=current_value)
        if ok and new_value != current_value:
            column_mapping = {
                "Nama Lengkap": "nama_lengkap",
                "Umur": "umur",
                "Jenis Kelamin": "jenis_kelamin",
                "Tanggal Kunjungan": "tanggal_kunjungan",
                "Gejala": "gejala",
                "Pengobatan": "pengobatan"
            }
            db_field = column_mapping.get(field_name)
            if db_field:
                conn = sqlite3.connect(DB_NAME)
                cursor = conn.cursor()
                cursor.execute(f"UPDATE patients SET {db_field}=? WHERE id=?", (new_value, patient_id))
                conn.commit()
                conn.close()
                self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem(new_value))
                QMessageBox.information(self, "Sukses", f"Data berhasil diubah untuk {field_name}.")

    def delete_row(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus.")
            return
        patient_id = int(self.ui.tableWidget.item(row, 0).text())
        reply = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus data ini?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
            conn.commit()
            conn.close()
            self.load_data()

    def search_data(self, text):
        text = text.lower()
        for row in range(self.ui.tableWidget.rowCount()):
            nama_item = self.ui.tableWidget.item(row, 1)
            match = text in nama_item.text().lower() if nama_item else False
            self.ui.tableWidget.setRowHidden(row, not match)

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save CSV", "health_records.csv", "CSV Files (*.csv)"
        )
        if filename:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients")
            data = cursor.fetchall()
            conn.close()
            with open(filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nama Lengkap", "Umur", "Jenis Kelamin", "Tanggal Kunjungan", "Gejala", "Pengobatan"])
                for row in data:
                    writer.writerow(row)
            QMessageBox.information(self, "Sukses", "Data berhasil diekspor ke CSV.")

    def show_about(self):
        QMessageBox.information(self, "Tentang Aplikasi",
            "Health Record System\n\n"
            "Aplikasi ini digunakan untuk mencatat dan mengelola data pasien "
            "secara sederhana. Fitur-fitur meliputi pencatatan data kunjungan, "
            "edit data langsung di tabel, pencarian pasien, serta ekspor data ke format CSV.\n\n"
            "Dikembangkan menggunakan PyQt5 dan SQLite.")

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(QAction("Simpan", self, triggered=self.saveData))
        fileMenu.addAction(QAction("Keluar", self, triggered=self.close))
        editMenu = menubar.addMenu("Edit")
        editMenu.addAction(QAction("Cari Pasien", self, triggered=self.focusCariPasien))
        editMenu.addAction(QAction("Hapus Data", self, triggered=self.delete_row))
        helpMenu = menubar.addMenu("Bantuan")
        helpMenu.addAction(QAction("Tentang Aplikasi", self, triggered=self.show_about))

    def saveData(self):
        QMessageBox.information(self, "Simpan", "Data sudah tersimpan di database secara otomatis.")

    def focusCariPasien(self):
        self.ui.lineEdit.setFocus()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
