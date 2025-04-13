import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate
from aBTL_py.view.database import Database
from datetime import datetime


class DangKyVe(QMainWindow):
    def __init__(self, role=None):
        super().__init__()
        self.role = role
        ui_path = os.path.abspath("../ui/DangKyVe.ui")
        loadUi(ui_path, self)
        self.tai_du_lieu_gia_ve()
        self.tai_du_lieu_phuong_tien()
        self.load_data()
        self.cmbLoaiVe.currentTextChanged.connect(self.cap_nhat_gia_ve)
        self.tblVeThangNam.itemSelectionChanged.connect(self.hienThiThongTin)
        self.btnDangKy.clicked.connect(self.dang_ky)
        self.btnSua.clicked.connect(self.sua)
        self.btnXoa.clicked.connect(self.xoa)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnThoat.clicked.connect(self.thoat)
        self.dtNgayBatDau.setDate(QDate.currentDate())
        self.dtNgayHetHan.setDate(QDate.currentDate())
        self.btntimkiem.clicked.connect(self.tim_kiem)


    def thoat(self):
        if self.role == 'Admin':
            from aBTL_py.controler.trangchu import TrangChu
            self.trang_chu = TrangChu()
            self.trang_chu.show()
        elif self.role == 'NhanVien':
            from aBTL_py.controler.trangchu1 import TrangChu1
            self.trang_chu1 = TrangChu1()
            self.trang_chu1.show()
        self.close()

    def tai_du_lieu_gia_ve(self):
        db = Database()
        query = "SELECT MaGiaVe, Gia FROM giave WHERE LoaiVe IN ('Thang', 'Nam')"
        rows = db.ket_noi(query)
        self.gia_ve_dict = {}
        if rows:
            self.cmbLoaiVe.clear()
            for row in rows:
                ma_gia_ve, gia = row
                self.cmbLoaiVe.addItem(str(ma_gia_ve))
                self.gia_ve_dict[str(ma_gia_ve)] = str(gia)
            if self.cmbLoaiVe.count() > 0:
                self.txtGiaVe.setText(self.gia_ve_dict[self.cmbLoaiVe.currentText()])
        else:
            print("Không có dữ liệu trong bảng giave hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def cap_nhat_gia_ve(self, ma_gia_ve):
        if ma_gia_ve and ma_gia_ve in self.gia_ve_dict:
            self.txtGiaVe.setText(self.gia_ve_dict[ma_gia_ve])
        else:
            self.txtGiaVe.clear()

    def tai_du_lieu_phuong_tien(self):
        db = Database()
        query = "SELECT MaPhuongTien, BienSo, TenChuXe FROM phuongtien"
        rows = db.ket_noi(query)
        self.phuong_tien_dict = {}
        if rows:
            self.cmbMaPhuongTien.clear()
            for row in rows:
                ma_phuong_tien, bien_so, ten_chu_xe = row
                display_text = f"{ma_phuong_tien} - {bien_so} - {ten_chu_xe}"
                self.cmbMaPhuongTien.addItem(display_text)
                self.phuong_tien_dict[display_text] = {
                    'MaPhuongTien': str(ma_phuong_tien),
                    'BienSo': bien_so,
                    'TenChuXe': ten_chu_xe
                }
        else:
            print("Không có dữ liệu trong bảng phuongtien hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def load_data(self):
        db = Database()
        query = """
            SELECT v.MaVe, p.MaPhuongTien, p.BienSo, p.TenChuXe, v.LoaiVe, v.Gia, v.NgayBatDau, v.NgayHetHan, v.TrangThai
            FROM vethangnam v
            LEFT JOIN phuongtien p ON v.MaPhuongTien = p.MaPhuongTien
        """
        rows = db.ket_noi(query)
        if rows:
            self.tblVeThangNam.setRowCount(len(rows))
            self.tblVeThangNam.setColumnCount(9)
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.tblVeThangNam.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            print("Không có dữ liệu trong bảng vethangnam hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def hienThiThongTin(self):
        selected_items = self.tblVeThangNam.selectedItems()
        if not selected_items:
            return

        row = self.tblVeThangNam.currentRow()
        if row < 0:
            return
        ma_ve = self.tblVeThangNam.item(row, 0).text() if self.tblVeThangNam.item(row, 0) else ""
        ma_phuong_tien = self.tblVeThangNam.item(row, 1).text() if self.tblVeThangNam.item(row, 1) else ""
        bien_so = self.tblVeThangNam.item(row, 2).text() if self.tblVeThangNam.item(row, 2) else ""
        ten_chu_xe = self.tblVeThangNam.item(row, 3).text() if self.tblVeThangNam.item(row, 3) else ""
        loai_ve = self.tblVeThangNam.item(row, 4).text() if self.tblVeThangNam.item(row, 4) else ""
        gia_ve = self.tblVeThangNam.item(row, 5).text() if self.tblVeThangNam.item(row, 5) else ""
        ngay_bat_dau = self.tblVeThangNam.item(row, 6).text() if self.tblVeThangNam.item(row, 6) else ""
        ngay_het_han = self.tblVeThangNam.item(row, 7).text() if self.tblVeThangNam.item(row, 7) else ""
        trang_thai = self.tblVeThangNam.item(row, 8).text() if self.tblVeThangNam.item(row, 8) else ""

        self.txtMaVe.setText(ma_ve)
        display_text = f"{ma_phuong_tien} - {bien_so} - {ten_chu_xe}"
        self.cmbMaPhuongTien.setCurrentText(display_text)
        db = Database()
        query = "SELECT MaGiaVe FROM giave WHERE LoaiVe = %s AND Gia = %s"
        result = db.ket_noi(query, (loai_ve, gia_ve))
        if result:
            self.cmbLoaiVe.setCurrentText(str(result[0][0]))
        db.dong_ket_noi()
        self.txtGiaVe.setText(gia_ve)
        self.dtNgayBatDau.setDate(QDate.fromString(ngay_bat_dau, "yyyy-MM-dd"))
        self.dtNgayHetHan.setDate(QDate.fromString(ngay_het_han, "yyyy-MM-dd"))

    def dang_ky(self):
        ma_ve = self.txtMaVe.text().strip()
        selected_phuong_tien = self.cmbMaPhuongTien.currentText().strip()
        ma_gia_ve = self.cmbLoaiVe.currentText().strip()
        gia_ve = self.txtGiaVe.text().strip()
        ngay_bat_dau = self.dtNgayBatDau.date().toString("yyyy-MM-dd")
        ngay_het_han = self.dtNgayHetHan.date().toString("yyyy-MM-dd")

        if not all([ma_ve, selected_phuong_tien, ma_gia_ve, gia_ve, ngay_bat_dau, ngay_het_han]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return

        ma_phuong_tien = self.phuong_tien_dict[selected_phuong_tien]['MaPhuongTien']
        db = Database()
        query = "SELECT LoaiVe FROM giave WHERE MaGiaVe = %s"
        result = db.ket_noi(query, (ma_gia_ve,))
        loai_ve = result[0][0] if result else None
        if not loai_ve:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy loại vé tương ứng!")
            db.dong_ket_noi()
            return
        query = """
            INSERT INTO vethangnam (MaVe, MaPhuongTien, LoaiVe, Gia, NgayBatDau, NgayHetHan, TrangThai)
            VALUES (%s, %s, %s, %s, %s, %s, 'HoatDong')
        """
        values = (ma_ve, ma_phuong_tien, loai_ve, gia_ve, ngay_bat_dau, ngay_het_han)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Đăng ký vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi đăng ký vé. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def sua(self):
        ma_ve = self.txtMaVe.text().strip()
        selected_phuong_tien = self.cmbMaPhuongTien.currentText().strip()
        ma_gia_ve = self.cmbLoaiVe.currentText().strip()
        gia_ve = self.txtGiaVe.text().strip()
        ngay_bat_dau = self.dtNgayBatDau.date().toString("yyyy-MM-dd")
        ngay_het_han = self.dtNgayHetHan.date().toString("yyyy-MM-dd")

        if not all([ma_ve, selected_phuong_tien, ma_gia_ve, gia_ve, ngay_bat_dau, ngay_het_han]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin để sửa!")
            return

        ma_phuong_tien = self.phuong_tien_dict[selected_phuong_tien]['MaPhuongTien']
        db = Database()
        query = "SELECT LoaiVe FROM giave WHERE MaGiaVe = %s"
        result = db.ket_noi(query, (ma_gia_ve,))
        loai_ve = result[0][0] if result else None
        if not loai_ve:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy loại vé tương ứng!")
            db.dong_ket_noi()
            return

        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn sửa thông tin vé này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return
        query = """
            UPDATE vethangnam 
            SET MaPhuongTien = %s, LoaiVe = %s, Gia = %s, NgayBatDau = %s, NgayHetHan = %s, TrangThai = TrangThai
            WHERE MaVe = %s
        """
        values = (ma_phuong_tien, loai_ve, gia_ve, ngay_bat_dau, ngay_het_han, ma_ve)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Sửa thông tin vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi sửa thông tin. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def xoa(self):
        ma_ve = self.txtMaVe.text().strip()
        if not ma_ve:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mã vé hoặc chọn vé cần xóa!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa vé này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        db = Database()
        query = "DELETE FROM vethangnam WHERE MaVe = %s"
        values = (ma_ve,)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Xóa vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi xóa vé. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def lam_moi(self):
        self.txtMaVe.clear()
        self.cmbMaPhuongTien.setCurrentIndex(0)
        self.cmbLoaiVe.setCurrentIndex(0)
        if self.cmbLoaiVe.currentText():
            self.txtGiaVe.setText(self.gia_ve_dict[self.cmbLoaiVe.currentText()])
        self.dtNgayBatDau.setDate(QDate.currentDate())
        self.dtNgayHetHan.setDate(QDate.currentDate())

    def load_data1(self, keyword=""):
        db = Database()
        query = """
            SELECT v.MaVe, p.MaPhuongTien, p.BienSo, p.TenChuXe, v.LoaiVe, v.Gia, v.NgayBatDau, v.NgayHetHan, v.TrangThai
            FROM vethangnam v
            LEFT JOIN phuongtien p ON v.MaPhuongTien = p.MaPhuongTien
        """
        values = None

        if keyword:
            query += " WHERE LOWER(v.MaVe) LIKE %s OR LOWER(p.MaPhuongTien) LIKE %s OR LOWER(p.BienSo) LIKE %s OR LOWER(p.TenChuXe) LIKE %s OR LOWER(v.LoaiVe) LIKE %s"
            values = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")

        rows = db.ket_noi(query, values) if values else db.ket_noi(query)

        if rows:
            self.tblVeThangNam.setRowCount(len(rows))
            self.tblVeThangNam.setColumnCount(9)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblVeThangNam.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            self.tblVeThangNam.setRowCount(0)
        db.dong_ket_noi()

    def tim_kiem(self):
        keyword = self.txttukhoa.text().strip().lower()
        self.load_data1(keyword)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DangKyVe()
    window.show()
    sys.exit(app.exec())