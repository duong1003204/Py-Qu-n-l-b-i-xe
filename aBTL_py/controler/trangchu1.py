import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi

class TrangChu1(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.abspath("../ui/TrangChu1.ui")
        loadUi(ui_path, self)


        self.btnQuanLyXe.clicked.connect(self.mo_quan_li_xe)
        self.btnDangKiVe.clicked.connect(self.mo_dang_ky_ve)
        self.btnGiaHanVe.clicked.connect(self.mo_gia_han_ve)
        self.btnQuanLyVe.clicked.connect(self.mo_quan_ly_gia_ve)
        self.btnQuanLyVaoRa.clicked.connect(self.mo_quan_ly_vao_ra)

        self.btnDangXuat.clicked.connect(self.dang_xuat)


    def dang_xuat(self):
        from aBTL_py.view.login import DangNhap
        self.dang_nhap = DangNhap()
        self.dang_nhap.show()
        self.close()

    def mo_quan_li_xe(self,role):
        from aBTL_py.controler.quanlyxe import QuanLyXe
        self.quanly_xe = QuanLyXe(role='NhanVien')
        self.hide()
        self.quanly_xe.show()

    def mo_quan_ly_gia_ve(self):
        from aBTL_py.controler.quanlygiave import QuanLyGiaVe
        self.quanly_giave  = QuanLyGiaVe(role= "NhanVien")
        self.hide()
        self.quanly_giave.show()
    def mo_dang_ky_ve(self):
        from aBTL_py.controler.dangkyve import DangKyVe
        self.dangky_ve = DangKyVe(role="NhanVien")
        self.hide()
        self.dangky_ve.show()
    def mo_quan_ly_vao_ra(self):
        from aBTL_py.controler.quanlyvaora import QuanLyVaoRa
        self.quanly_vaora = QuanLyVaoRa(role= 'NhanVien')
        self.hide()
        self.quanly_vaora.show()
    def mo_gia_han_ve(self):
        from aBTL_py.controler.giahanve import GiaHanVe
        self.giahan_ve = GiaHanVe(role ="NhanVien")
        self.hide()
        self.giahan_ve.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrangChu1()
    window.show()
    sys.exit(app.exec())
