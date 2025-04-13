import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from aBTL_py.view.login import DangNhap


class TrangChu(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.abspath("../ui/TrangChu.ui")
        loadUi(ui_path, self)
        self.btnDangXuat.clicked.connect(self.dang_xuat)
        self.btnQuanLyNhanVien.clicked.connect(self.mo_quan_li_nhan_vien)
        self.btnQuanLyXe.clicked.connect(self.mo_quan_li_xe)
        self.btnQuanLyVe.clicked.connect(self.mo_quan_ly_gia_ve)
        self.btnDangKiVe.clicked.connect(self.mo_dang_ky_ve)
        self.btnGiaHanVe.clicked.connect(self.mo_gia_han_ve)
        self.btnQuanLyVe.clicked.connect(self.mo_quan_ly_gia_ve)
        self.btnQuanLyVaoRa.clicked.connect(self.mo_quan_ly_vao_ra)
        self.btnBaoCaoDoanhThu.clicked.connect(self.mo_bao_cao_doanh_thu)

    def mo_quan_li_nhan_vien(self):
        from aBTL_py.controler.quanlynhanvien import QuanLyNhanVien
        self.quanly_nv = QuanLyNhanVien()
        self.quanly_nv.show()
        self.close()

    def mo_quan_li_xe(self):
        from aBTL_py.controler.quanlyxe import QuanLyXe
        self.quanly_xe = QuanLyXe(role='Admin')
        self.hide()
        self.quanly_xe.show()
    def mo_quan_ly_gia_ve(self):
        from aBTL_py.controler.quanlygiave import QuanLyGiaVe
        self.quanly_giave  = QuanLyGiaVe(role= "Admin")
        self.hide()
        self.quanly_giave.show()
    def mo_dang_ky_ve(self):
        from aBTL_py.controler.dangkyve import DangKyVe
        self.dangky_ve = DangKyVe(role="Admin")
        self.hide()
        self.dangky_ve.show()
    def mo_gia_han_ve(self):
        from aBTL_py.controler.giahanve import GiaHanVe
        self.giahan_ve = GiaHanVe(role ="Admin")
        self.hide()
        self.giahan_ve.show()
    def mo_quan_ly_vao_ra(self):
        from aBTL_py.controler.quanlyvaora import QuanLyVaoRa
        self.quanly_vaora = QuanLyVaoRa(role= 'Admin')
        self.hide()
        self.quanly_vaora.show()
    def dang_xuat(self):
        self.dang_nhap = DangNhap()
        self.dang_nhap.show()
        self.close()
    def mo_bao_cao_doanh_thu(self):
        from aBTL_py.controler.baocaodoanhthu import BaoCaoDoanhThu
        self.baocao_doanhthu = BaoCaoDoanhThu(role= 'Admin')
        self.hide()
        self.baocao_doanhthu.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrangChu()
    window.show()
    sys.exit(app.exec())
