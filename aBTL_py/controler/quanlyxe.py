import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from aBTL_py.view.database import Database
from datetime import datetime


class QuanLyXe(QMainWindow):
    def __init__(self, role=None):
        super().__init__()
        self.role = role
        ui_path = os.path.abspath("../ui/QuanLyXe.ui")
        loadUi(ui_path, self)
        self.btnThoat.clicked.connect(self.thoat)
        self.btnThem.clicked.connect(self.them)

        self.btnSua.clicked.connect(self.sua)
        self.tblQuanLyXe.cellClicked.connect(self.hienThiThongTin)
        self.btnXoa.clicked.connect(self.xoa)
        self.btntimkiem.clicked.connect(self.tim_kiem)
        self.load_data()



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
        self.txtMaPhuongTien.clear()
        self.txtTenChuXe.clear()
        self.txtBienSoXe.clear()
        self.cmbLoaiXe.setCurrentIndex(0)

    def hienThiThongTin(self,row):
        self.txtMaPhuongTien.setText(self.tblQuanLyXe.item(row, 0).text())
        self.txtTenChuXe.setText(self.tblQuanLyXe.item(row, 1).text())
        self.txtBienSoXe.setText(self.tblQuanLyXe.item(row, 2).text())

        loai_xe = self.tblQuanLyXe.item(row, 3).text()
        index = self.cmbLoaiXe.findText(loai_xe)
        if index >= 0:
            self.cmbLoaiXe.setCurrentIndex(index)



    def load_data(self):
        db = Database()
        query = "SELECT * FROM phuongtien"
        rows = db.ket_noi(query)
        if rows:
            self.tblQuanLyXe.setRowCount(len(rows))
            self.tblQuanLyXe.setColumnCount(4)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblQuanLyXe.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            print("❌ Không có dữ liệu hoặc lỗi khi truy vấn.")
        db.dong_ket_noi()

    def them(self):
        idxe = self.txtMaPhuongTien.text().strip()
        ho_ten = self.txtTenChuXe.text().strip()
        bien_so_xe = self.txtBienSoXe.text().strip()
        loai_xe = self.cmbLoaiXe.currentText().strip()

        if not all([idxe, ho_ten, bien_so_xe, loai_xe]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return

        db = Database()
        query = """
            INSERT INTO phuongtien (MaPhuongTien, TenChuXe, BienSo, LoaiXe)
            VALUES (%s, %s, %s, %s)
        """
        values = (idxe, ho_ten, bien_so_xe, loai_xe)

        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", " Thêm thông tin xe và chủ xe thành công!")
            self.load_data()
            self.lam_moi()
        else:
            print("lỗi thêm thông tin , tìm thông tin mà fix")
        db.dong_ket_noi()

    def sua(self):
        idxe = self.txtMaPhuongTien.text().strip()
        ho_ten = self.txtTenChuXe.text().strip()
        bien_so_xe = self.txtBienSoXe.text().strip()
        loai_xe = self.cmbLoaiXe.currentText().strip()

        if not all([idxe, ho_ten, bien_so_xe, loai_xe]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return

        db = Database()
        query = """
            UPDATE phuongtien 
            SET TenChuXe = %s, BienSo = %s, LoaiXe = %s 
            WHERE MaPhuongTien = %s
        """
        values = (ho_ten, bien_so_xe, loai_xe, idxe)

        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Sửa phương tiện thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Không thể sửa phương tiện.")
        db.dong_ket_noi()

    def xoa(self):
        selected_row = self.tblQuanLyXe.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một phương tiện để xóa!")
            return

        idpt_item = self.tblQuanLyXe.item(selected_row, 0)
        if not idpt_item:
            QMessageBox.warning(self, "Thông báo", "Không tìm thấy mã phương tiện!")
            return

        idpt = idpt_item.text()

        if QMessageBox.question(
                self,
                "Xác nhận",
                f"Bạn có chắc muốn xóa phương tiện có mã {idpt} không?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        db = Database()
        query = "DELETE FROM phuongtien WHERE MaPhuongTien = %s"
        values = (idpt,)

        result = db.ket_noi(query, values)
        db.dong_ket_noi()

        if result:
            self.load_data()
            self.lam_moi()
            self.tblQuanLyXe.removeRow(selected_row)
            QMessageBox.information(self, "Thành công", "Xóa phương tiện suýt không thành công!")
        else:
            QMessageBox.critical(self, "Lỗi", "Xóa phương tiện thất bại!")

    def load_data1(self, keyword=""):
        db = Database()
        query = "SELECT * FROM phuongtien"
        values = None

        if keyword:
            query += " WHERE MaPhuongTien LIKE %s OR TenChuXe LIKE %s OR BienSo LIKE %s OR LoaiXe LIKE %s"
            values = (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")

        rows = db.ket_noi(query, values) if values else db.ket_noi(query)

        if rows:
            self.tblQuanLyXe.setRowCount(len(rows))
            self.tblQuanLyXe.setColumnCount(4)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblQuanLyXe.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            self.tblQuanLyXe.setRowCount(0)
        db.dong_ket_noi()

    def tim_kiem(self):
        keyword = self.txttukhoa.text().strip()
        self.load_data1(keyword)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuanLyXe()
    window.show()
    sys.exit(app.exec())
