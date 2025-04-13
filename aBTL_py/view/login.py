import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from database import Database

class DangNhap(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.abspath("../ui/DangNhap.ui")
        loadUi(ui_path, self)

        self.btnDangNhap.clicked.connect(self.dang_nhap)
        self.db = Database()

    def dang_nhap(self):
        ten_dn = self.txtTenDangNhap.text().strip()
        mat_khau = self.txtMatKhau.text().strip()

        if not ten_dn or not mat_khau:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            query = "SELECT HoTen, VaiTro FROM nhanvien WHERE TenDangNhap = %s AND MatKhau = %s"
            user = self.db.ket_noi(query, (ten_dn, mat_khau))

            if user:
                ho_ten, vai_tro = user[0]
                QMessageBox.information(self, "Thành công", f"Chào {ho_ten} !")

                if vai_tro == "Admin":
                    from aBTL_py.controler.trangchu import TrangChu

                    self.trang_chu = TrangChu()
                else:
                    from aBTL_py.controler.trangchu1 import TrangChu1

                    self.trang_chu = TrangChu1()

                self.trang_chu.show()
                self.close()
            else:
                QMessageBox.critical(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DangNhap()
    window.show()
    sys.exit(app.exec())
