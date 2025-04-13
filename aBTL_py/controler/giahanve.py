import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate
from aBTL_py.view.database import Database
from datetime import datetime, timedelta


class GiaHanVe(QMainWindow):
    def __init__(self, role=None):
        super().__init__()
        self.role = role
        ui_path = os.path.abspath("../ui/GiaHanVe.ui")
        loadUi(ui_path, self)
        self.tai_du_lieu_gia_ve()
        self.tai_du_lieu_phuong_tien()
        self.load_data()
        self.cmbLoaiVe.currentTextChanged.connect(self.cap_nhat_gia_ve)
        self.tblLichSuGiaHan.itemSelectionChanged.connect(self.hienThiThongTin)
        self.btnGiaHan.clicked.connect(self.gia_han)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.dtNgayGiaHan.setDate(QDate.currentDate())
        self.btnThoat.clicked.connect(self.thoat)
        self.btnTimKiem.clicked.connect(self.tim_kiem)


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
        query = """
            SELECT p.MaPhuongTien, p.BienSo, p.TenChuXe 
            FROM phuongtien p 
            JOIN vethangnam v ON p.MaPhuongTien = v.MaPhuongTien 
            WHERE v.TrangThai = 'HetHan'
        """
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
            print("Không có phương tiện nào có trạng thái 'HetHan' hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def load_data(self):
        db = Database()
        query = """
            SELECT gh.MaGiaHan, p.MaPhuongTien, p.BienSo, p.TenChuXe, v.LoaiVe, gh.SoTien, gh.NgayGiaHan
            FROM lichsugiahan gh
            LEFT JOIN vethangnam v ON gh.MaVe = v.MaVe
            LEFT JOIN phuongtien p ON v.MaPhuongTien = p.MaPhuongTien
        """
        rows = db.ket_noi(query)
        if rows:
            self.tblLichSuGiaHan.setRowCount(len(rows))
            self.tblLichSuGiaHan.setColumnCount(7)
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    self.tblLichSuGiaHan.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            print("Không có dữ liệu trong bảng lichsugiahan hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def hienThiThongTin(self):
        selected_items = self.tblLichSuGiaHan.selectedItems()
        if not selected_items:
            return

        row = self.tblLichSuGiaHan.currentRow()
        if row < 0:
            return

        ma_gia_han = self.tblLichSuGiaHan.item(row, 0).text() if self.tblLichSuGiaHan.item(row, 0) else ""
        ma_phuong_tien = self.tblLichSuGiaHan.item(row, 1).text() if self.tblLichSuGiaHan.item(row, 1) else ""
        bien_so = self.tblLichSuGiaHan.item(row, 2).text() if self.tblLichSuGiaHan.item(row, 2) else ""
        ten_chu_xe = self.tblLichSuGiaHan.item(row, 3).text() if self.tblLichSuGiaHan.item(row, 3) else ""
        loai_ve = self.tblLichSuGiaHan.item(row, 4).text() if self.tblLichSuGiaHan.item(row, 4) else ""
        so_tien = self.tblLichSuGiaHan.item(row, 5).text() if self.tblLichSuGiaHan.item(row, 5) else ""
        ngay_gia_han = self.tblLichSuGiaHan.item(row, 6).text() if self.tblLichSuGiaHan.item(row, 6) else ""

        self.txtMaGiaHan.setText(ma_gia_han)
        display_text = f"{ma_phuong_tien} - {bien_so} - {ten_chu_xe}"
        self.cmbMaPhuongTien.setCurrentText(display_text)
        db = Database()
        query = "SELECT MaGiaVe FROM giave WHERE LoaiVe = %s AND Gia = %s"
        result = db.ket_noi(query, (loai_ve, so_tien))
        if result:
            self.cmbLoaiVe.setCurrentText(str(result[0][0]))
        db.dong_ket_noi()
        self.txtGiaVe.setText(so_tien)
        self.dtNgayGiaHan.setDate(QDate.fromString(ngay_gia_han, "yyyy-MM-dd"))

    def gia_han(self):
        ma_gia_han = self.txtMaGiaHan.text().strip()
        selected_phuong_tien = self.cmbMaPhuongTien.currentText().strip()
        ma_gia_ve = self.cmbLoaiVe.currentText().strip()
        so_tien_moi = self.txtGiaVe.text().strip()
        ngay_gia_han = self.dtNgayGiaHan.date().toString("yyyy-MM-dd")

        if not all([ma_gia_han, selected_phuong_tien, ma_gia_ve, so_tien_moi, ngay_gia_han]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return

        ma_phuong_tien = self.phuong_tien_dict[selected_phuong_tien]['MaPhuongTien']
        db = Database()
        query = "SELECT MaVe, Gia, NgayHetHan FROM vethangnam WHERE MaPhuongTien = %s AND LoaiVe IN ('Thang', 'Nam')"
        result = db.ket_noi(query, (ma_phuong_tien,))
        ma_ve = result[0][0] if result else None
        gia_cu = result[0][1] if result else 0.0
        ngay_het_han_cu = result[0][2] if result else None

        if not ma_ve:
            QMessageBox.warning(self, "Thông báo", "Không tìm thấy vé tháng/năm cho phương tiện này!")
            db.dong_ket_noi()
            return

        query = "SELECT LoaiVe FROM giave WHERE MaGiaVe = %s"
        result = db.ket_noi(query, (ma_gia_ve,))
        loai_ve = result[0][0] if result else None
        if not loai_ve:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy loại vé tương ứng!")
            db.dong_ket_noi()
            return

        try:
            so_tien_tong = float(gia_cu) + float(so_tien_moi)
        except ValueError:
            QMessageBox.critical(self, "Lỗi", "Số tiền không hợp lệ!")
            db.dong_ket_noi()
            return

        if loai_ve == 'Thang':
            ngay_het_han_moi = datetime.strptime(ngay_gia_han, "%Y-%m-%d").date() + timedelta(days=30)
        elif loai_ve == 'Nam':
            ngay_het_han_moi = datetime.strptime(ngay_gia_han, "%Y-%m-%d").date() + timedelta(days=365)
        else:
            ngay_het_han_moi = ngay_gia_han
        query_update_vethangnam = """
            UPDATE vethangnam 
            SET TrangThai = 'HoatDong', NgayHetHan = %s 
            WHERE MaVe = %s
        """
        db.ket_noi(query_update_vethangnam, (ngay_het_han_moi, ma_ve))

        query = """
            INSERT INTO lichsugiahan (MaGiaHan, MaVe, NgayGiaHan, SoTien)
            VALUES (%s, %s, %s, %s)
        """
        values = (ma_gia_han, ma_ve, ngay_gia_han, so_tien_tong)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Gia hạn vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi gia hạn vé. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def lam_moi(self):
        self.txtMaGiaHan.clear()
        self.cmbMaPhuongTien.setCurrentIndex(0)
        self.cmbLoaiVe.setCurrentIndex(0)
        if self.cmbLoaiVe.currentText():
            self.txtGiaVe.setText(self.gia_ve_dict[self.cmbLoaiVe.currentText()])
        self.dtNgayGiaHan.setDate(QDate.currentDate())

    def load_data1(self, keyword=""):
        db = Database()
        query = """
            SELECT gh.MaGiaHan, p.MaPhuongTien, p.BienSo, p.TenChuXe, v.LoaiVe, gh.SoTien, gh.NgayGiaHan
            FROM lichsugiahan gh
            LEFT JOIN vethangnam v ON gh.MaVe = v.MaVe
            LEFT JOIN phuongtien p ON v.MaPhuongTien = p.MaPhuongTien
        """
        values = None

        if keyword:
            query += " WHERE LOWER(gh.MaGiaHan) LIKE %s OR LOWER(p.MaPhuongTien) LIKE %s OR LOWER(p.BienSo) LIKE %s OR LOWER(p.TenChuXe) LIKE %s OR LOWER(v.LoaiVe) LIKE %s"
            values = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")

        rows = db.ket_noi(query, values) if values else db.ket_noi(query)

        if rows:
            self.tblLichSuGiaHan.setRowCount(len(rows))
            self.tblLichSuGiaHan.setColumnCount(7)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblLichSuGiaHan.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            self.tblLichSuGiaHan.setRowCount(0)
        db.dong_ket_noi()

    def tim_kiem(self):
        keyword = self.txtTuKhoa.text().strip().lower()
        self.load_data1(keyword)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GiaHanVe()
    window.show()
    sys.exit(app.exec())