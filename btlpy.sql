-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 13, 2025 at 08:30 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `btlpy`
--

-- --------------------------------------------------------

--
-- Table structure for table `giave`
--

CREATE TABLE `giave` (
  `MaGiaVe` varchar(10) NOT NULL,
  `LoaiVe` enum('Luot','Thang','Nam') NOT NULL,
  `LoaiXe` enum('OTo','XeMay','XeDap') NOT NULL,
  `Gia` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `giave`
--

INSERT INTO `giave` (`MaGiaVe`, `LoaiVe`, `LoaiXe`, `Gia`) VALUES
('OTOLUOT', 'Luot', 'OTo', 5000.00),
('OTONAM', 'Nam', 'OTo', 1600000.00),
('OTOTHANG', 'Thang', 'OTo', 140000.00),
('XEDAP', 'Luot', 'OTo', 1000.00),
('XEDAPN', 'Nam', 'XeDap', 300000.00),
('XEDAPT', 'Thang', 'XeDap', 30000.00),
('XEMAYL', 'Luot', 'XeMay', 2000.00),
('XEMAYN', 'Nam', 'XeMay', 620000.00),
('XEMAYT', 'Thang', 'XeMay', 50000.00);

-- --------------------------------------------------------

--
-- Table structure for table `lichsugiahan`
--

CREATE TABLE `lichsugiahan` (
  `MaGiaHan` varchar(10) NOT NULL,
  `MaVe` varchar(10) DEFAULT NULL,
  `NgayGiaHan` date DEFAULT NULL,
  `SoTien` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lichsugiahan`
--

INSERT INTO `lichsugiahan` (`MaGiaHan`, `MaVe`, `NgayGiaHan`, `SoTien`) VALUES
('mv001', 'mv002', '2025-02-25', 280000.00);

-- --------------------------------------------------------

--
-- Table structure for table `lichsuvaora`
--

CREATE TABLE `lichsuvaora` (
  `MaLichSu` varchar(10) NOT NULL,
  `MaPhuongTien` varchar(10) DEFAULT NULL,
  `ThoiGianVao` datetime DEFAULT NULL,
  `ThoiGianRa` datetime DEFAULT NULL,
  `Phi` decimal(10,2) DEFAULT NULL,
  `LoaiVeSuDung` enum('Luot','Thang','Nam') DEFAULT 'Luot'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lichsuvaora`
--

INSERT INTO `lichsuvaora` (`MaLichSu`, `MaPhuongTien`, `ThoiGianVao`, `ThoiGianRa`, `Phi`, `LoaiVeSuDung`) VALUES
('1', 'OTO001', '2025-02-25 18:20:30', '2025-02-25 11:20:30', 0.00, 'Thang'),
('10', 'OTO001', '2025-03-18 06:45:00', '2025-03-18 09:15:00', 5000.00, 'Luot'),
('11', 'VR002', '2025-03-05 14:30:00', '2025-03-05 16:45:00', 5000.00, 'Luot'),
('111', 'VR005', '2025-03-18 16:57:52', '2025-03-18 16:59:41', 2000.00, 'Luot'),
('1111', 'OTO002', '2025-03-19 07:41:56', '2025-03-19 07:43:11', 0.00, 'Thang'),
('1112', 'VR006', '2025-03-19 07:42:12', '2025-03-19 07:43:02', 5000.00, 'Luot'),
('12', 'VR003', '2025-03-17 08:00:00', '2025-03-17 12:00:00', 5000.00, 'Luot'),
('13', 'VR001', '2025-03-11 15:00:00', '2025-03-11 17:30:00', 2000.00, 'Luot'),
('14', 'OTO002', '2025-03-16 09:30:00', '2025-03-16 14:00:00', 5000.00, 'Luot'),
('15', 'XM001', '2025-03-02 07:15:00', '2025-03-02 10:30:00', 2000.00, 'Luot'),
('16', 'VR004', '2025-03-21 12:00:00', '2025-03-21 13:00:00', 2000.00, 'Luot'),
('2', 'VR001', '2025-02-25 18:21:11', '2025-02-25 11:21:12', 2000.00, 'Luot'),
('3', 'VR004', '2025-02-25 18:49:50', '2025-02-25 18:50:25', 2000.00, 'Luot'),
('4', 'OTO001', '2025-02-25 18:53:14', '2025-02-25 18:53:42', 0.00, 'Thang'),
('5', 'XM001', '2025-03-01 08:30:00', '2025-03-01 12:45:00', 2000.00, 'Luot'),
('6', 'VR001', '2025-03-10 09:15:00', '2025-03-10 14:20:00', 2000.00, 'Luot'),
('7', 'OTO002', '2025-03-15 07:00:00', '2025-03-15 17:30:00', 5000.00, 'Luot'),
('8', 'VR004', '2025-03-18 10:00:00', '2025-03-18 11:00:00', 2000.00, 'Luot'),
('9', 'XM002', '2025-03-17 13:00:00', '2025-03-17 18:00:00', 5000.00, 'Luot');

-- --------------------------------------------------------

--
-- Table structure for table `nhanvien`
--

CREATE TABLE `nhanvien` (
  `MaNhanVien` varchar(10) NOT NULL,
  `HoTen` varchar(100) DEFAULT NULL,
  `TenDangNhap` varchar(50) DEFAULT NULL,
  `MatKhau` varchar(255) DEFAULT NULL,
  `VaiTro` enum('Admin','NhanVien') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nhanvien`
--

INSERT INTO `nhanvien` (`MaNhanVien`, `HoTen`, `TenDangNhap`, `MatKhau`, `VaiTro`) VALUES
('NV001', 'Phạm Đại Dương', '1', '1', 'Admin'),
('NV002', 'Phạm Đại DươngNV', '2', '2', 'NhanVien'),
('NV003', 'Lương Trọng Duy NV', 'duy', '1', 'NhanVien'),
('NV004', 'Bùi Khánh Hùng', 'hung', '1', 'Admin');

-- --------------------------------------------------------

--
-- Table structure for table `phuongtien`
--

CREATE TABLE `phuongtien` (
  `MaPhuongTien` varchar(10) NOT NULL,
  `TenChuXe` varchar(100) DEFAULT NULL,
  `BienSo` varchar(20) DEFAULT NULL,
  `LoaiXe` enum('OTo','XeMay','XeDap') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `phuongtien`
--

INSERT INTO `phuongtien` (`MaPhuongTien`, `TenChuXe`, `BienSo`, `LoaiXe`) VALUES
('OTO001', 'Phạm Đại Dương', '19B22657', 'OTo'),
('OTO002', 'Phạm Đại Dương 2', '19B22222', 'OTo'),
('VR001', 'Khách vãng lai', '22B819321', 'XeMay'),
('VR002', 'Khách vãng lai', '35H88122', 'OTo'),
('VR003', 'Khách vãng lai', 'EWQ', 'OTo'),
('VR004', 'Khách vãng lai', '66B88121', 'XeMay'),
('VR005', 'Khách vãng lai', '111111', 'XeMay'),
('VR006', 'Khách vãng lai', '34D4249294', 'OTo'),
('XM001', 'Phạm Đại Dương', '19B122657', 'XeMay'),
('XM002', 'Khách vãng lai', '3G3333', 'OTo');

-- --------------------------------------------------------

--
-- Table structure for table `vethangnam`
--

CREATE TABLE `vethangnam` (
  `MaVe` varchar(10) NOT NULL,
  `MaPhuongTien` varchar(10) DEFAULT NULL,
  `LoaiVe` varchar(11) NOT NULL,
  `Gia` decimal(10,2) DEFAULT NULL,
  `NgayBatDau` date DEFAULT NULL,
  `NgayHetHan` date DEFAULT NULL,
  `TrangThai` enum('HoatDong','HetHan') DEFAULT 'HoatDong'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vethangnam`
--

INSERT INTO `vethangnam` (`MaVe`, `MaPhuongTien`, `LoaiVe`, `Gia`, `NgayBatDau`, `NgayHetHan`, `TrangThai`) VALUES
('mv001', 'OTO002', 'Nam', 1600000.00, '2025-02-25', '2026-02-25', 'HoatDong'),
('mv002', 'OTO001', 'Thang', 140000.00, '2025-01-24', '2025-03-27', 'HoatDong'),
('mv003', 'XM001', 'Thang', 50000.00, '2025-03-01', '2025-04-01', 'HoatDong'),
('mv004', 'VR001', 'Nam', 620000.00, '2025-03-10', '2026-03-10', 'HoatDong'),
('mv005', 'OTO002', 'Thang', 140000.00, '2025-03-15', '2025-04-15', 'HoatDong'),
('mv006', 'VR004', 'Thang', 50000.00, '2025-02-20', '2025-03-27', 'HoatDong'),
('mv007', 'XM002', 'Nam', 1600000.00, '2025-01-01', '2026-01-01', 'HoatDong'),
('mv008', 'OTO001', 'Nam', 1600000.00, '2025-03-18', '2026-03-18', 'HoatDong'),
('mv009', 'VR002', 'Thang', 140000.00, '2025-03-05', '2025-04-05', 'HoatDong'),
('mv010', 'VR003', 'Nam', 1600000.00, '2025-02-15', '2026-02-15', 'HoatDong');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `giave`
--
ALTER TABLE `giave`
  ADD PRIMARY KEY (`MaGiaVe`);

--
-- Indexes for table `lichsugiahan`
--
ALTER TABLE `lichsugiahan`
  ADD PRIMARY KEY (`MaGiaHan`),
  ADD KEY `MaVe` (`MaVe`);

--
-- Indexes for table `lichsuvaora`
--
ALTER TABLE `lichsuvaora`
  ADD PRIMARY KEY (`MaLichSu`),
  ADD KEY `MaPhuongTien` (`MaPhuongTien`);

--
-- Indexes for table `nhanvien`
--
ALTER TABLE `nhanvien`
  ADD PRIMARY KEY (`MaNhanVien`),
  ADD UNIQUE KEY `TenDangNhap` (`TenDangNhap`);

--
-- Indexes for table `phuongtien`
--
ALTER TABLE `phuongtien`
  ADD PRIMARY KEY (`MaPhuongTien`),
  ADD UNIQUE KEY `BienSo` (`BienSo`);

--
-- Indexes for table `vethangnam`
--
ALTER TABLE `vethangnam`
  ADD PRIMARY KEY (`MaVe`),
  ADD KEY `MaPhuongTien` (`MaPhuongTien`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `lichsugiahan`
--
ALTER TABLE `lichsugiahan`
  ADD CONSTRAINT `lichsugiahan_ibfk_1` FOREIGN KEY (`MaVe`) REFERENCES `vethangnam` (`MaVe`);

--
-- Constraints for table `lichsuvaora`
--
ALTER TABLE `lichsuvaora`
  ADD CONSTRAINT `lichsuvaora_ibfk_1` FOREIGN KEY (`MaPhuongTien`) REFERENCES `phuongtien` (`MaPhuongTien`);

--
-- Constraints for table `vethangnam`
--
ALTER TABLE `vethangnam`
  ADD CONSTRAINT `vethangnam_ibfk_1` FOREIGN KEY (`MaPhuongTien`) REFERENCES `phuongtien` (`MaPhuongTien`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
