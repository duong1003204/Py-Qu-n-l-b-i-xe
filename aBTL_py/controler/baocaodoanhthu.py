import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import QDate
from aBTL_py.view.database import Database

class BaoCaoDoanhThu(QMainWindow):
    def __init__(self,role = None):
        super().__init__()
        self.role = role
        ui_path = os.path.abspath("../ui/BaoCaoDoanhThu.ui")
        loadUi(ui_path, self)
        self.db = Database()
        self.btnThoat.clicked.connect(self.thoat)

        self.btnDailyRevenue.clicked.connect(self.thong_ke_ngay)
        self.btnMonthlyRevenue.clicked.connect(self.thong_ke_thang)
        self.btnYearlyRevenue.clicked.connect(self.thong_ke_nam)
        self.btnMonthlyTicketRevenue.clicked.connect(self.thong_ke_ve_thang)

        self.dateEditFrom.setDate(QDate.currentDate())
        self.dateEditTo.setDate(QDate.currentDate())
        self.dateTimeEditYearMonth.setDate(QDate.currentDate())
        self.spinBoxYear.setDate(QDate.currentDate())
        self.spinBoxYearMonthlyTicket.setDate(QDate.currentDate())

    def thong_ke_ngay(self):
        from_date = self.dateEditFrom.date().toString("yyyy-MM-dd")
        to_date = self.dateEditTo.date().toString("yyyy-MM-dd")

        query = """
            SELECT ThoiGianRa, SUM(Phi) as TongPhi
            FROM lichsuvaora
            WHERE DATE(ThoiGianRa) BETWEEN %s AND %s
            GROUP BY DATE(ThoiGianRa)
        """
        result = self.db.ket_noi(query, (from_date, to_date))

        if result:
            self.tableDailyRevenue.setRowCount(len(result))
            self.tableDailyRevenue.setColumnCount(2)
            self.tableDailyRevenue.setHorizontalHeaderLabels(["Ngày", "Doanh thu"])

            total_revenue = 0
            for row_idx, row_data in enumerate(result):
                ngay = row_data[0].strftime("%Y-%m-%d")
                doanh_thu = float(row_data[1])
                total_revenue += doanh_thu

                self.tableDailyRevenue.setItem(row_idx, 0, QTableWidgetItem(ngay))
                self.tableDailyRevenue.setItem(row_idx, 1, QTableWidgetItem(f"{doanh_thu:,.0f} VNĐ"))

            self.lblTotalDailyRevenue.setText(f"Tổng doanh thu: {total_revenue:,.0f} VNĐ")
        else:
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu doanh thu trong khoảng thời gian này.")
            self.tableDailyRevenue.setRowCount(0)
            self.lblTotalDailyRevenue.setText("Tổng doanh thu: 0 VNĐ")

    def thong_ke_thang(self):
        month = self.comboBoxMonth.currentIndex() + 1  # Tháng từ 1-12
        year = self.dateTimeEditYearMonth.date().year()

        query = """
            SELECT DATE(ThoiGianRa), SUM(Phi) as TongPhi
            FROM lichsuvaora
            WHERE MONTH(ThoiGianRa) = %s AND YEAR(ThoiGianRa) = %s
            GROUP BY DATE(ThoiGianRa)
        """
        result = self.db.ket_noi(query, (month, year))

        if result:
            self.tableMonthlyRevenue.setRowCount(len(result))
            self.tableMonthlyRevenue.setColumnCount(2)
            self.tableMonthlyRevenue.setHorizontalHeaderLabels(["Ngày", "Doanh thu"])

            total_revenue = 0
            for row_idx, row_data in enumerate(result):
                ngay = row_data[0].strftime("%Y-%m-%d")
                doanh_thu = float(row_data[1])
                total_revenue += doanh_thu

                self.tableMonthlyRevenue.setItem(row_idx, 0, QTableWidgetItem(ngay))
                self.tableMonthlyRevenue.setItem(row_idx, 1, QTableWidgetItem(f"{doanh_thu:,.0f} VNĐ"))

            self.lblTotalMonthlyRevenue.setText(f"Tổng doanh thu: {total_revenue:,.0f} VNĐ")
        else:
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu doanh thu trong tháng này.")
            self.tableMonthlyRevenue.setRowCount(0)
            self.lblTotalMonthlyRevenue.setText("Tổng doanh thu: 0 VNĐ")

    def thong_ke_nam(self):
        year = self.spinBoxYear.date().year()

        query = """
            SELECT MONTH(ThoiGianRa), SUM(Phi) as TongPhi
            FROM lichsuvaora
            WHERE YEAR(ThoiGianRa) = %s
            GROUP BY MONTH(ThoiGianRa)
        """
        result = self.db.ket_noi(query, (year,))

        if result:
            self.tableYearlyRevenue.setRowCount(len(result))
            self.tableYearlyRevenue.setColumnCount(2)
            self.tableYearlyRevenue.setHorizontalHeaderLabels(["Tháng", "Doanh thu"])

            total_revenue = 0
            for row_idx, row_data in enumerate(result):
                thang = f"Tháng {row_data[0]}"
                doanh_thu = float(row_data[1])
                total_revenue += doanh_thu

                self.tableYearlyRevenue.setItem(row_idx, 0, QTableWidgetItem(thang))
                self.tableYearlyRevenue.setItem(row_idx, 1, QTableWidgetItem(f"{doanh_thu:,.0f} VNĐ"))

            self.lblTotalYearlyRevenue.setText(f"Tổng doanh thu: {total_revenue:,.0f} VNĐ")
        else:
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu doanh thu trong năm này.")
            self.tableYearlyRevenue.setRowCount(0)
            self.lblTotalYearlyRevenue.setText("Tổng doanh thu: 0 VNĐ")

    def thong_ke_ve_thang(self):
        year = self.spinBoxYearMonthlyTicket.date().year()
        month = self.comboBoxMonthMonthlyTicket.currentIndex() + 1

        query = """
            SELECT MaVe, Gia, NgayBatDau, NgayHetHan
            FROM vethangnam
            WHERE LoaiVe = 'Thang' AND YEAR(NgayBatDau) = %s AND MONTH(NgayBatDau) = %s
        """
        result = self.db.ket_noi(query, (year, month))

        if result:
            self.tableMonthlyTicketRevenue.setRowCount(len(result))
            self.tableMonthlyTicketRevenue.setColumnCount(4)
            self.tableMonthlyTicketRevenue.setHorizontalHeaderLabels(["Mã vé", "Giá", "Ngày bắt đầu", "Ngày hết hạn"])

            total_revenue = 0
            for row_idx, row_data in enumerate(result):
                ma_ve = row_data[0]
                gia = float(row_data[1])
                ngay_bat_dau = row_data[2].strftime("%Y-%m-%d")
                ngay_het_han = row_data[3].strftime("%Y-%m-%d")
                total_revenue += gia

                self.tableMonthlyTicketRevenue.setItem(row_idx, 0, QTableWidgetItem(ma_ve))
                self.tableMonthlyTicketRevenue.setItem(row_idx, 1, QTableWidgetItem(f"{gia:,.0f} VNĐ"))
                self.tableMonthlyTicketRevenue.setItem(row_idx, 2, QTableWidgetItem(ngay_bat_dau))
                self.tableMonthlyTicketRevenue.setItem(row_idx, 3, QTableWidgetItem(ngay_het_han))

            self.lblTotalMonthlyTicketRevenue.setText(f"Tổng doanh thu vé tháng: {total_revenue:,.0f} VNĐ")
        else:
            QMessageBox.warning(self, "Thông báo", "Không có dữ liệu vé tháng trong khoảng thời gian này.")
            self.tableMonthlyTicketRevenue.setRowCount(0)
            self.lblTotalMonthlyTicketRevenue.setText("Tổng doanh thu vé tháng: 0 VNĐ")

    def closeEvent(self, event):
        self.db.dong_ket_noi()
        event.accept()
    def thoat(self):
        from aBTL_py.controler.trangchu import TrangChu
        self.trang_chu = TrangChu()
        self.trang_chu.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaoCaoDoanhThu()
    window.show()
    sys.exit(app.exec())