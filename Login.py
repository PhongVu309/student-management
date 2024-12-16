from PyQt6 import QtCore, QtGui, QtWidgets
from Trangchu import Ui_TrangChuWindow as Ui_TrangChuWindow
import pyodbc

class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(373, 264)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 40, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 70, 55, 16))
        self.label_2.setObjectName("label_2")
        self.btnDangNhap = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnDangNhap.setGeometry(QtCore.QRect(130, 120, 93, 28))
        self.btnDangNhap.setObjectName("btnDangNhap")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 120, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.txtTenTK = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txtTenTK.setGeometry(QtCore.QRect(130, 40, 113, 22))
        self.txtTenTK.setObjectName("txtTenTK")
        self.txtMatKhau = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txtMatKhau.setGeometry(QtCore.QRect(130, 70, 113, 22))
        self.txtMatKhau.setObjectName("txtMatKhau")
        self.txtMatKhau.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)  # Ẩn mật khẩu khi nhập
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.btnDangNhap.clicked.connect(self.check_login)
        self.pushButton_2.clicked.connect(QtWidgets.QApplication.instance().quit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Ten TK"))
        self.label_2.setText(_translate("MainWindow", "Mat khau"))
        self.btnDangNhap.setText(_translate("MainWindow", "Dang nhap"))
        self.pushButton_2.setText(_translate("MainWindow", "Thoat"))

    def check_login(self):
        username = self.txtTenTK.text()
        password = self.txtMatKhau.text()

        # Kết nối đến cơ sở dữ liệu
        connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=PHONG-VU\\SQLEXPRESS;'
            'DATABASE=QuanLySinhVien;'
            'UID=sa;'
            'PWD=223003'
        )
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Kiểm tra tài khoản và mật khẩu
        cursor.execute("SELECT * FROM login WHERE TenTK = ? AND Password = ?", (username, password))
        result = cursor.fetchone()

        if result:
            self.open_Trang_Chu_window()
        else:
            QtWidgets.QMessageBox.warning(None, 'Error', 'Sai tên tài khoản hoặc mật khẩu!')

        cursor.close()
        conn.close()

    def open_Trang_Chu_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_TrangChuWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
