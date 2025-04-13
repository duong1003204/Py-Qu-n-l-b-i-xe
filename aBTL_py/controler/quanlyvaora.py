import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDateTime
from aBTL_py.view.database import Database
from datetime import datetime, timedelta


class QuanLyVaoRa(QMainWindow):
    def __init__(self, role=None):
        super().__init__()
        self.role = role
        ui_path = os.path.abspath("../ui/QuanLyVaoRa.ui")
        loadUi(ui_path, self)
        self.load_data()
        self.tai_du_lieu_gia_ve()  # Tải dữ liệu giá vé vào cmbLoaiVe
        self.btnXeVao.clicked.connect(self.xe_vao)
        self.btnXeRa.clicked.connect(self.xe_ra)
        self.btnLamMoi.clicked.connect(self.lam_moi)
        self.btnThoat.clicked.connect(self.thoat)
        self.dtThoiGianVao.setDateTime(QDateTime.currentDateTime())  # Sử dụng QDateTimeEdit
        self.dtThoiGianRa.setDateTime(QDateTime.currentDateTime())   # Sử dụng QDateTimeEdit
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
        """Tải dữ liệu giá vé từ bảng giave (vé lượt) và đổ MaGiaVe vào cmbLoaiVe."""
        db = Database()
        query = "SELECT MaGiaVe, LoaiXe, Gia FROM giave WHERE LoaiVe = 'Luot'"
        rows = db.ket_noi(query)
        self.gia_ve_dict = {}  # Lưu trữ ánh xạ MaGiaVe -> (LoaiXe, Gia)
        if rows:
            self.cmbLoaiVe.clear()
            for row in rows:
                ma_gia_ve, loai_xe, gia = row
                self.cmbLoaiVe.addItem(str(ma_gia_ve))
                self.gia_ve_dict[str(ma_gia_ve)] = (str(loai_xe), str(gia))
        else:
            print("Không có dữ liệu vé lượt trong bảng giave hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def cap_nhat_gia_ve(self, ma_gia_ve):
        """Cập nhật thông báo phí (không hiển thị trong txtMaVaoRa nữa)."""
        if ma_gia_ve and ma_gia_ve in self.gia_ve_dict:
            _, gia = self.gia_ve_dict[ma_gia_ve]
            QMessageBox.information(self, "Thông báo", f"Phí = {gia} (Vé lượt) - Nhập MaLichSu vào txtMaVaoRa để tiếp tục.")
        else:
            QMessageBox.warning(self, "Thông báo", "MaGiaVe không hợp lệ!")

    def load_data(self):
        db = Database()
        query = """
            SELECT lr.MaLichSu, p.BienSo, lr.ThoiGianVao, lr.ThoiGianRa, lr.Phi, lr.LoaiVeSuDung
            FROM lichsuvaora lr
            LEFT JOIN phuongtien p ON lr.MaPhuongTien = p.MaPhuongTien
        """
        rows = db.ket_noi(query)
        if rows:
            self.tblLichSuVaoRa.setRowCount(len(rows))
            self.tblLichSuVaoRa.setColumnCount(6)
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    if isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")
                    self.tblLichSuVaoRa.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            print("Không có dữ liệu trong bảng lichsuvaora hoặc lỗi truy vấn.")
        db.dong_ket_noi()

    def xe_vao(self):
        bien_so = self.txtBienSo.text().strip()
        ma_lich_su = self.txtMaVaoRa.text().strip()  # Sử dụng MaLichSu từ txtMaVaoRa
        thoi_gian_vao = self.dtThoiGianVao.dateTime().toString("yyyy-MM-dd HH:mm:ss")  # Lấy thời gian từ QDateTimeEdit

        if not all([bien_so, ma_lich_su, thoi_gian_vao]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin (Biển số, MaLichSu)!")
            return

        db = Database()
        # Kiểm tra hoặc tạo MaPhuongTien nếu biển số không tồn tại
        query_phuong_tien = "SELECT MaPhuongTien, LoaiXe FROM phuongtien WHERE BienSo = %s"
        result_phuong_tien = db.ket_noi(query_phuong_tien, (bien_so,))

        if result_phuong_tien:
            ma_phuong_tien, loai_xe = result_phuong_tien[0]
        else:
            # Nếu không tồn tại, tạo MaPhuongTien với định dạng VR000 tăng dần
            query_max = "SELECT MAX(MaPhuongTien) FROM phuongtien WHERE MaPhuongTien LIKE 'VR%'"
            result_max = db.ket_noi(query_max)
            if result_max and result_max[0][0]:
                # Tăng số cuối cùng của MaPhuongTien (giả định định dạng 'VRxxx')
                number = int(result_max[0][0].replace('VR', '')) + 1
                ma_phuong_tien = f"VR{number:03d}"  # Định dạng lại (ví dụ: 'VR001', 'VR002', v.v.)
            else:
                ma_phuong_tien = "VR001"  # Mặc định nếu không có dữ liệu
            # Thêm phương tiện mới vào phuongtien (giả định LoaiXe từ MaGiaVe)
            ma_gia_ve = self.cmbLoaiVe.currentText()
            if not ma_gia_ve or ma_gia_ve not in self.gia_ve_dict:
                QMessageBox.warning(self, "Thông báo", "Vui lòng chọn MaGiaVe hợp lệ!")
                db.dong_ket_noi()
                return
            loai_xe, _ = self.gia_ve_dict[ma_gia_ve]
            query_insert = "INSERT INTO phuongtien (MaPhuongTien, TenChuXe, BienSo, LoaiXe) VALUES (%s, %s, %s, %s)"
            db.ket_noi(query_insert, (ma_phuong_tien, "Khách vãng lai", bien_so, loai_xe))

        # Kiểm tra vé tháng/năm để xác định phí và loại vé
        query_ve_thang_nam = """
            SELECT v.MaVe, v.LoaiVe, v.Gia, v.NgayHetHan, v.TrangThai 
            FROM vethangnam v 
            WHERE v.MaPhuongTien = %s AND v.TrangThai = 'HoatDong'
        """
        result_ve_thang_nam = db.ket_noi(query_ve_thang_nam, (ma_phuong_tien,))

        if result_ve_thang_nam:
            ma_ve, loai_ve, gia, ngay_het_han, trang_thai = result_ve_thang_nam[0]
            ngay_het_han = datetime.strptime(str(ngay_het_han), "%Y-%m-%d").date()
            if ngay_het_han >= datetime.now().date():
                phi = 0  # Đặt phí = 0 nếu có vé tháng/năm hợp lệ
                loai_ve = 'Thang'
            else:
                # Nếu vé tháng/năm hết hạn, sử dụng vé lượt
                ma_gia_ve = self.cmbLoaiVe.currentText()
                if not ma_gia_ve or ma_gia_ve not in self.gia_ve_dict:
                    QMessageBox.warning(self, "Thông báo", "MaGiaVe không hợp lệ, vui lòng kiểm tra lại!")
                    db.dong_ket_noi()
                    return
                _, gia = self.gia_ve_dict[ma_gia_ve]
                phi = float(gia)
                loai_ve = 'Luot'
        else:
            # Không có vé tháng/năm, sử dụng vé lượt
            ma_gia_ve = self.cmbLoaiVe.currentText()
            if not ma_gia_ve or ma_gia_ve not in self.gia_ve_dict:
                QMessageBox.warning(self, "Thông báo", "MaGiaVe không hợp lệ, vui lòng kiểm tra lại!")
                db.dong_ket_noi()
                return
            _, gia = self.gia_ve_dict[ma_gia_ve]
            phi = float(gia)
            loai_ve = 'Luot'

        # Kiểm tra MaLichSu đã tồn tại chưa
        query_check_ma = "SELECT MaLichSu FROM lichsuvaora WHERE MaLichSu = %s"
        result_check_ma = db.ket_noi(query_check_ma, (ma_lich_su,))
        if result_check_ma:
            QMessageBox.warning(self, "Thông báo", "MaLichSu đã tồn tại, vui lòng nhập mã khác!")
            db.dong_ket_noi()
            return

        query = """
            INSERT INTO lichsuvaora (MaLichSu, MaPhuongTien, ThoiGianVao, ThoiGianRa, Phi, LoaiVeSuDung)
            VALUES (%s, %s, %s, NULL, %s, %s)
        """
        values = (ma_lich_su, ma_phuong_tien, thoi_gian_vao, phi, loai_ve)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Xe vào thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi ghi thông tin xe vào. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def xe_ra(self):
        # Lấy dòng được chọn trong bảng
        selected_items = self.tblLichSuVaoRa.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một bản ghi trong bảng để ghi thời gian ra!")
            return

        row = self.tblLichSuVaoRa.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một bản ghi hợp lệ!")
            return

        ma_lich_su = self.tblLichSuVaoRa.item(row, 0).text() if self.tblLichSuVaoRa.item(row, 0) else ""
        thoi_gian_ra = self.dtThoiGianRa.dateTime().toString("yyyy-MM-dd HH:mm:ss")  # Lấy thời gian từ QDateTimeEdit

        if not all([ma_lich_su, thoi_gian_ra]):
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập thời gian ra!")
            return

        db = Database()
        query = """
            UPDATE lichsuvaora 
            SET ThoiGianRa = %s 
            WHERE MaLichSu = %s AND ThoiGianRa IS NULL
        """
        values = (thoi_gian_ra, ma_lich_su)
        result = db.ket_noi(query, values)
        if result:
            QMessageBox.information(self, "Thành công", "Xe ra thành công!")
            self.load_data()
            self.lam_moi()
        else:
            QMessageBox.critical(self, "Lỗi", "Lỗi khi ghi thông tin xe ra. Vui lòng kiểm tra lại!")
        db.dong_ket_noi()

    def lam_moi(self):
        self.txtBienSo.clear()
        self.txtMaVaoRa.clear()
        self.cmbLoaiVe.setCurrentIndex(0)
        self.dtThoiGianVao.setDateTime(QDateTime.currentDateTime())  # Sử dụng QDateTimeEdit
        self.dtThoiGianRa.setDateTime(QDateTime.currentDateTime())   # Sử dụng QDateTimeEdit

    def tim_kiem(self):
        tu_khoa = self.txtTuKhoa.text().strip()
        if not tu_khoa:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập từ khóa tìm kiếm!")
            return

        db = Database()
        query = '''
            SELECT lr.MaLichSu, p.MaPhuongTien, p.BienSo, p.TenChuXe, lr.ThoiGianVao, lr.ThoiGianRa, lr.Phi, lr.LoaiVeSuDung
            FROM lichsuvaora lr
            LEFT JOIN phuongtien p ON lr.MaPhuongTien = p.MaPhuongTien
            WHERE p.TenChuXe LIKE %s OR p.MaPhuongTien LIKE %s OR lr.MaLichSu LIKE %s
        '''
        values = (f"%{tu_khoa}%", f"%{tu_khoa}%", f"%{tu_khoa}%")
        rows = db.ket_noi(query, values)
        if rows:
            self.tblLichSuVaoRa.setRowCount(len(rows))
            self.tblLichSuVaoRa.setColumnCount(8)
            self.tblLichSuVaoRa.setHorizontalHeaderLabels(
                ['MaLichSu', 'MaPhuongTien', 'BienSo', 'TenChuXe', 'ThoiGianVao', 'ThoiGianRa', 'Phi', 'LoaiVeSuDung'])
            for row_idx, row_data in enumerate(rows):
                for col_idx, value in enumerate(row_data):
                    if isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")
                    self.tblLichSuVaoRa.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            QMessageBox.warning(self, "Thông báo", "Không tìm thấy kết quả phù hợp!")
        db.dong_ket_noi()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuanLyVaoRa()
    window.show()
    sys.exit(app.exec())