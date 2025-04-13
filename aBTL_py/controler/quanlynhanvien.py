import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from aBTL_py.view.database import Database

class QuanLyNhanVien(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.abspath("../ui/QuanLyNhanVien.ui")
        loadUi(ui_path, self)
        self.tblNhanVien.cellClicked.connect(self.hienThiThongTin)

        self.btnThoat.clicked.connect(self.thoat)
        self.btnThem.clicked.connect(self.them)
        self.btnSua.clicked.connect(self.sua)
        self.btnXoa.clicked.connect(self.xoa)
        self.btnTimKiem.clicked.connect(self.tim_kiem)
        self.load_data()

    def lam_moi(self):
        self.txtIDNV.clear()
        self.txtHoTen.clear()
        self.txtTenDangNhap.clear()
        self.txtMatKhau.clear()
        self.cmbVaiTro.setCurrentIndex(0)
    def hienThiThongTin(self,row):
        self.txtIDNV.setText(self.tblNhanVien.item(row, 0).text())
        self.txtHoTen.setText(self.tblNhanVien.item(row, 1).text())
        self.txtTenDangNhap.setText(self.tblNhanVien.item(row, 2).text())
        self.txtMatKhau.setText(self.tblNhanVien.item(row, 3).text())

        vai_tro = self.tblNhanVien.item(row, 4).text()
        index = self.cmbVaiTro.findText(vai_tro)
        if index >= 0:
            self.cmbVaiTro.setCurrentIndex(index)

    def thoat(self):
        from aBTL_py.controler.trangchu import TrangChu
        self.trang_chu = TrangChu()
        self.trang_chu.show()
        self.close()

    def load_data(self):
        db = Database()
        query = "SELECT * FROM nhanvien"
        rows = db.ket_noi(query)
        if rows:
            self.tblNhanVien.setRowCount(len(rows))
            self.tblNhanVien.setColumnCount(5)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblNhanVien.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            print("❌ Không có dữ liệu hoặc lỗi khi truy vấn.")
        db.dong_ket_noi()

    def them(self):
        idnv = self.txtIDNV.text().strip()
        ho_ten = self.txtHoTen.text().strip()
        ten_dang_nhap = self.txtTenDangNhap.text().strip()
        mat_khau = self.txtMatKhau.text().strip()
        vai_tro = self.cmbVaiTro.currentText().strip()

        if not all([idnv, ho_ten, ten_dang_nhap, mat_khau, vai_tro]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return

        db = Database()
        query = """
            INSERT INTO nhanvien (MaNhanVien, HoTen, TenDangNhap, MatKhau, VaiTro)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (idnv, ho_ten, ten_dang_nhap, mat_khau, vai_tro)

        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", " Thêm nhân viên  thành công!")
            self.load_data()
            self.lam_moi()
        else:
            print("lỗi thêm nhân viên , tìm nhân viên mà fix")
        db.dong_ket_noi()
    def sua(self):
        idnv = self.txtIDNV.text().strip()
        ho_ten = self.txtHoTen.text().strip()
        ten_dang_nhap = self.txtTenDangNhap.text().strip()
        mat_khau = self.txtMatKhau.text().strip()
        vai_tro = self.cmbVaiTro.currentText().strip()
        if not all([idnv, ho_ten, ten_dang_nhap, mat_khau, vai_tro]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đủ thông tin!")
            return

        db = Database()
        query = """
            UPDATE nhanvien SET HoTen = %s, TenDangNhap = %s, MatKhau = %s, VaiTro = %s WHERE MaNhanVien = %s
        """

        values = (ho_ten, ten_dang_nhap, mat_khau, vai_tro, idnv)

        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", " Sửa nhân viên  thành công!")
            self.load_data()
            self.lam_moi()
        else:
            print("lỗi sửa nhân viên , tìm nhân viên mà fix")
        db.dong_ket_noi()

    def xoa(self):
        selected_row = self.tblNhanVien.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một nhân viên để xóa!")
            return

        idnv_item = self.tblNhanVien.item(selected_row, 0)
        if not idnv_item:
            QMessageBox.warning(self, "Thông báo", "Không tìm thấy mã nhân viên!")
            return

        idnv = idnv_item.text()

        if QMessageBox.question(
                self,
                "Xác nhận",
                f"Bạn có chắc muốn xóa nhân viên có mã {idnv} không?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        db = Database()
        query = "DELETE FROM nhanvien WHERE MaNhanVien = %s"
        values = (idnv,)

        result = db.ket_noi(query, values)
        db.dong_ket_noi()

        if result:
            self.load_data()
            self.lam_moi()
            self.tblNhanVien.removeRow(selected_row)
            QMessageBox.information(self, "Thành công", "Xóa nhân viên suýt không thành công!")
        else:
            QMessageBox.critical(self, "Lỗi", "Xóa nhân viên thất bại!")

    def tim_kiem(self):
        tu_khoa = self.txtTuKhoa.text().strip()

        if not tu_khoa:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        db = Database()
        query = """
            SELECT * FROM nhanvien 
            WHERE MaNhanVien LIKE %s 
            OR HoTen LIKE %s 
            OR TenDangNhap LIKE %s 
            OR VaiTro LIKE %s
        """
        values = (f"%{tu_khoa}%", f"%{tu_khoa}%", f"%{tu_khoa}%", f"%{tu_khoa}%")

        rows = db.ket_noi(query, values)
        db.dong_ket_noi()

        if rows:
            self.tblNhanVien.setRowCount(len(rows))
            self.tblNhanVien.setColumnCount(5)
            for row_index, row_data in enumerate(rows):
                for col_index, value in enumerate(row_data):
                    self.tblNhanVien.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        else:
            QMessageBox.information(self, "Thông báo", "Không tìm thấy kết quả phù hợp.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuanLyNhanVien()
    window.show()
    sys.exit(app.exec())
