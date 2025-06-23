from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #d0e9ff;")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1920, 1030))
        self.tabWidget.setObjectName("tabWidget")

        self.tab_pasien = QtWidgets.QWidget()
        self.tab_pasien.setObjectName("tab_pasien")

        self.label = QtWidgets.QLabel(self.tab_pasien)
        self.label.setGeometry(QtCore.QRect(200, 50, 1500, 120))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.tableWidget = QtWidgets.QTableWidget(self.tab_pasien)
        self.tableWidget.setGeometry(QtCore.QRect(60, 300, 1800, 600))
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setStyleSheet("background-color: white; gridline-color: gray;")
        self.tableWidget.setShowGrid(True)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        for i in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

        self.tableWidget.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(120)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.widget = QtWidgets.QWidget(self.tab_pasien)
        self.widget.setGeometry(QtCore.QRect(60, 200, 1800, 60))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumHeight(40)
        font_lineedit = QtGui.QFont()
        font_lineedit.setPointSize(14)
        self.lineEdit.setFont(font_lineedit)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit.setStyleSheet("background-color: white;")

        self.pushButton = QtWidgets.QPushButton(self.widget)
        icon_add = QtGui.QIcon()
        icon_add.addPixmap(QtGui.QPixmap("icons/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon_add)
        self.pushButton.setIconSize(QtCore.QSize(36, 36))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumHeight(50)
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.tab_pasien)
        self.pushButton_2.setGeometry(QtCore.QRect(1710, 930, 150, 50))
        icon_del = QtGui.QIcon()
        icon_del.addPixmap(QtGui.QPixmap("icons/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon_del)
        self.pushButton_2.setIconSize(QtCore.QSize(36, 36))
        self.pushButton_2.setObjectName("pushButton_2")

        self.tabWidget.addTab(self.tab_pasien, "Data Pasien")

        self.tab_export = QtWidgets.QWidget()
        self.tab_export.setObjectName("tab_export")

        self.pushButton_export = QtWidgets.QPushButton(self.tab_export)
        self.pushButton_export.setGeometry(QtCore.QRect(850, 400, 250, 60))
        icon_exp = QtGui.QIcon()
        icon_exp.addPixmap(QtGui.QPixmap("icons/export.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_export.setIcon(icon_exp)
        self.pushButton_export.setObjectName("pushButton_export")
        font_export = QtGui.QFont()
        font_export.setPointSize(8)
        self.pushButton_export.setFont(font_export)
        self.pushButton_export.setStyleSheet("background-color: #2ecc71; color: white;")

        self.tabWidget.addTab(self.tab_export, "Ekspor Data")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 22))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Health Record System"))
        headers = ["ID", "Nama Lengkap", "Umur", "Jenis Kelamin", "Tanggal Kunjungan", "Gejala", "Pengobatan"]
        for i, text in enumerate(headers):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", text))
        self.label.setText(_translate("MainWindow", "Health Record System"))
        self.pushButton_2.setText(_translate("MainWindow", " Delete"))
        self.lineEdit.setPlaceholderText("cari pasien...")
        self.pushButton.setText(_translate("MainWindow", " Add"))
        self.pushButton_export.setText(_translate("MainWindow", "Ekspor Data ke CSV"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
