import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from aBTL_py.view.database import Database
from datetime import datetime


class QuanLyGiaVe(QMainWindow):
    def __init__(self, role=None):
        super().__init__()
        self.role = role
        ui_path = os.path.abspath("../ui/QuanLyGiaVe.ui")
        loadUi(ui_path, self)
        self.load_data()
        self.btnThem.clicked.connect(self.them)
        self.btnSua.clicked.connect(self.sua)
        self.btnXoa.clicked.connect(self.xoa)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.tblGiaVe.itemSelectionChanged.connect(self.hienThiThongTin)
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

    def lam_moi(self):
        self.txtMaVe.clear()
        self.cmbLoaiVe.setCurrentIndex(0)
        self.cmbLoaiXe.setCurrentIndex(0)
        self.txtGiaVe.clear()

    def load_data(self):
        db = Database()
        query = "SELECT * FROM giave"
        rows = db.ket_noi(query)
        if rows:
            self.tblGiaVe.setRowCount(len(rows))
            self.tblGiaVe.setColumnCount(4)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblGiaVe.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            print("❌ Không có dữ liệu hoặc lỗi khi truy vấn.")
        db.dong_ket_noi()

    def hienThiThongTin(self):
        selected_items = self.tblGiaVe.selectedItems()
        if not selected_items:
            return  # No row selected, do nothing

        row = self.tblGiaVe.currentRow()
        if row < 0:
            return  # Invalid row, do nothing

        ma_gia_ve = self.tblGiaVe.item(row, 0).text() if self.tblGiaVe.item(row, 0) else ""
        loai_ve = self.tblGiaVe.item(row, 1).text() if self.tblGiaVe.item(row, 1) else ""
        loai_xe = self.tblGiaVe.item(row, 2).text() if self.tblGiaVe.item(row, 2) else ""
        gia = self.tblGiaVe.item(row, 3).text() if self.tblGiaVe.item(row, 3) else ""

        self.txtMaVe.setText(ma_gia_ve)
        self.cmbLoaiVe.setCurrentText(loai_ve)
        self.cmbLoaiXe.setCurrentText(loai_xe)
        self.txtGiaVe.setText(gia)

    def them(self):
        idve = self.txtMaVe.text().strip()
        loaive = self.cmbLoaiVe.currentText().strip()
        loaixe = self.cmbLoaiXe.currentText().strip()
        giave = self.txtGiaVe.text().strip()
        if not all([idve, loaive, loaixe, giave]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return
        db = Database()
        query = """
            INSERT INTO giave (MaGiaVe, LoaiVe, LoaiXe, Gia)
            VALUES (%s, %s, %s, %s)
        """
        values = (idve, loaive, loaixe, giave)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Thêm loại vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi thêm thông tin. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def sua(self):
        idve = self.txtMaVe.text().strip()
        loaive = self.cmbLoaiVe.currentText().strip()
        loaixe = self.cmbLoaiXe.currentText().strip()
        giave = self.txtGiaVe.text().strip()

        if not all([idve, loaive, loaixe, giave]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin để sửa!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn sửa thông tin vé này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        db = Database()
        query = """
            UPDATE giave 
            SET LoaiVe = %s, LoaiXe = %s, Gia = %s 
            WHERE MaGiaVe = %s
        """
        values = (loaive, loaixe, giave, idve)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Sửa thông tin vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi sửa thông tin. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def xoa(self):
        idve = self.txtMaVe.text().strip()
        if not idve:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mã vé để xóa!")
            return

        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn xóa vé này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return

        db = Database()
        query = "DELETE FROM giave WHERE MaGiaVe = %s"
        values = (idve,)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Xóa vé thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi xóa vé. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def tim_kiem(self):
        tu_khoa = self.txtTuKhoa.text().strip()

        if not tu_khoa:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa để tìm kiếm!")
            return

        db = Database()
        query = """
            SELECT * FROM giave
            WHERE MaGiaVe LIKE %s OR LoaiVe LIKE %s OR LoaiXe LIKE %s
        """
        keyword = f"%{tu_khoa}%"
        rows = db.ket_noi(query, (keyword, keyword, keyword))

        if rows:
            self.tblGiaVe.setRowCount(len(rows))
            self.tblGiaVe.setColumnCount(4)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblGiaVe.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            QMessageBox.information(self, "Kết quả", "Không tìm thấy kết quả phù hợp.")
        db.dong_ket_noi()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuanLyGiaVe()
    window.show()
    sys.exit(app.exec())