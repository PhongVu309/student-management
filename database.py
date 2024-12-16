import pyodbc

# Chuỗi kết nối cơ sở dữ liệu
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=PHONG-VU\\SQLEXPRESS;'  # Dấu gạch chéo ngược phải được thoát trong chuỗi
    'DATABASE=master;'
    'UID=sa;'
    'PWD=223003'
)

# Sử dụng autocommit để tránh vấn đề với giao dịch
connection = pyodbc.connect(connection_string, autocommit=True)
cursor = connection.cursor()

# Kiểm tra xem cơ sở dữ liệu có tồn tại hay không
cursor.execute("SELECT COUNT(*) FROM sys.databases WHERE name = 'QuanLySinhVien'")
db_exists = cursor.fetchone()[0]

# Tạo cơ sở dữ liệu nếu chưa tồn tại
if not db_exists:
    cursor.execute('CREATE DATABASE QuanLySinhVien')

# Đóng kết nối sau khi tạo cơ sở dữ liệu
connection.close()

# Kết nối lại, lần này chỉ định cơ sở dữ liệu QuanLySinhVien
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=PHONG-VU\\SQLEXPRESS;'  # Dấu gạch chéo ngược phải được thoát trong chuỗi
    'DATABASE=QuanLySinhVien;'
    'UID=sa;'
    'PWD=223003'
)

# Thiết lập lại autocommit cho các thao tác tiếp theo
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Tạo các bảng
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'SinhVien') AND type in (N'U'))
    CREATE TABLE SinhVien (
        MaSV NVARCHAR(50) PRIMARY KEY,
        HoTen NVARCHAR(50),
        NgaySinh DATE,
        GioiTinh NVARCHAR(10),
        DiaChi NVARCHAR(100)
    )
''')
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'LopHoc') AND type in (N'U'))
    CREATE TABLE LopHoc (
        MaLop INT,
        MaSV NVARCHAR(50),
        TenLop NVARCHAR(50),
        Khoa NVARCHAR(50),
        PRIMARY KEY (MaSV, MaLop),
        FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
    )
''')
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'MonHoc') AND type in (N'U'))
    CREATE TABLE MonHoc (
        MaMon NVARCHAR(10) PRIMARY KEY,
        TenMon NVARCHAR(50),
        SoTinChi INT
    )
''')
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'DangKy') AND type in (N'U'))
    CREATE TABLE DangKy (
        MaSV NVARCHAR(50),
        MaMon NVARCHAR(10),
        NgayDangKy DATE,
        PRIMARY KEY (MaSV, MaMon),
        FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV),
        FOREIGN KEY (MaMon) REFERENCES MonHoc(MaMon)
    )
''')
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Diem') AND type in (N'U'))
    CREATE TABLE Diem (
        MaSV NVARCHAR(50),
        MaMon NVARCHAR(10),
        Diem FLOAT,
        PRIMARY KEY (MaSV, MaMon),
        FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV),
        FOREIGN KEY (MaMon) REFERENCES MonHoc(MaMon)
    )
''')
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'Login') AND type in (N'U'))
    CREATE TABLE Login (
        TenTK NVARCHAR(50),
        Password INT
    )
''')
connection.commit()

# Chèn dữ liệu mẫu
cursor.execute('''
    INSERT INTO SinhVien (MaSV, HoTen, NgaySinh, GioiTinh, DiaChi)
    VALUES 
        (N'SV001', N'Nguyễn Văn A', '2000-01-01', N'Nam', N'Hà Nội'),
        (N'SV002', N'Trần Thị B', '2001-02-02', N'Nữ', N'TP. Hồ Chí Minh'),
        (N'SV003', N'Phạm Thị C', '1999-03-03', N'Nữ', N'Đà Nẵng'),
        (N'SV004', N'Lê Văn D', '1998-04-04', N'Nam', N'Hải Phòng'),
        (N'SV005', N'Trần Văn E', '2002-05-05', N'Nam', N'Thái Bình'),
        (N'SV006', N'Nguyễn Thị F', '2003-06-06', N'Nữ', N'Hà Nam'),
        (N'SV007', N'Lê Thị G', '2000-07-07', N'Nữ', N'Bắc Giang'),
        (N'SV008', N'Hoàng Văn H', '2001-08-08', N'Nam', N'Thái Nguyên'),
        (N'SV009', N'Vũ Văn I', '1999-09-09', N'Nam', N'Hải Dương'),
        (N'SV010', N'Đỗ Thị K', '2002-10-10', N'Nữ', N'Nam Định'),
        (N'SV011', N'Mai Văn L', '2001-11-11', N'Nam', N'Hà Tĩnh'),
        (N'SV012', N'Nguyễn Thị M', '2000-12-12', N'Nữ', N'Bắc Ninh')
''')

cursor.execute('''
    INSERT INTO LopHoc (MaSV, MaLop, TenLop, Khoa)
    VALUES 
        (N'SV001', 1, N'Lớp 1', N'Khoa Công Nghệ Thông Tin'),
        (N'SV002', 2, N'Lớp 2', N'Khoa Kinh Tế'),
        (N'SV003', 3, N'Lớp 3', N'Khoa Công Nghệ Sinh Học'),
        (N'SV004', 4, N'Lớp 4', N'Khoa Điện Tử Viễn Thông'),
        (N'SV005', 5, N'Lớp 5', N'Khoa Kỹ Thuật Máy Tính'),
        (N'SV006', 6, N'Lớp 6', N'Khoa Quản Trị Kinh Doanh'),
        (N'SV007', 7, N'Lớp 7', N'Khoa Ngoại Ngữ'),
        (N'SV008', 8, N'Lớp 8', N'Khoa Khoa Học Xã Hội'),
        (N'SV009', 9, N'Lớp 9', N'Khoa Điện Tử'),
        (N'SV010', 10, N'Lớp 10', N'Khoa Vật Lý'),
        (N'SV011', 11, N'Lớp 11', N'Khoa Hóa Học'),
        (N'SV012', 12, N'Lớp 12', N'Khoa Sinh Học')
''')

cursor.execute('''
    INSERT INTO MonHoc (MaMon, TenMon, SoTinChi)
    VALUES 
        (N'MH001', N'Tin học cơ sở', 3),
        (N'MH002', N'Toán cao cấp', 4),
        (N'MH003', N'Lập trình Python', 3),
        (N'MH004', N'Cấu trúc dữ liệu và giải thuật', 4),
        (N'MH005', N'Hệ điều hành', 3),
        (N'MH006', N'Mạng máy tính', 3),
        (N'MH007', N'Tiếng Anh chuyên ngành', 2),
        (N'MH008', N'Tâm lý học đại cương', 2),
        (N'MH009', N'Toán rời rạc', 3),
        (N'MH010', N'Kinh tế học cơ bản', 3),
        (N'MH011', N'Chính trị học', 2),
        (N'MH012', N'Luật học căn bản', 2)
''')

cursor.execute('''
    INSERT INTO DangKy (MaSV, MaMon, NgayDangKy)
    VALUES 
        (N'SV001', N'MH001', '2024-06-01'),
        (N'SV002', N'MH002', '2024-06-01'),
        (N'SV003', N'MH003', '2024-06-01'),
        (N'SV004', N'MH004', '2024-06-01'),
        (N'SV005', N'MH005', '2024-06-01'),
        (N'SV006', N'MH006', '2024-06-01'),
        (N'SV007', N'MH007', '2024-06-01'),
        (N'SV008', N'MH008', '2024-06-01'),
        (N'SV009', N'MH009', '2024-06-01'),
        (N'SV010', N'MH010', '2024-06-01'),
        (N'SV011', N'MH011', '2024-06-01'),
        (N'SV012', N'MH012', '2024-06-01')
''')

cursor.execute('''
    INSERT INTO Diem (MaSV, MaMon, Diem)
    VALUES 
        (N'SV001', N'MH001', 8.5),
        (N'SV002', N'MH002', 9.0),
        (N'SV003', N'MH003', 7.5),
        (N'SV004', N'MH004', 8.0),
        (N'SV005', N'MH005', 9.5),
        (N'SV006', N'MH006', 8.5),
        (N'SV007', N'MH007', 7.0),
        (N'SV008', N'MH008', 8.8),
        (N'SV009', N'MH009', 9.2),
        (N'SV010', N'MH010', 7.9),
        (N'SV011', N'MH011', 8.7),
        (N'SV012', N'MH012', 9.8)
''')

cursor.execute('''
    INSERT INTO Login (TenTK, Password)
    VALUES (N'admin', 1),
           (N'Phong', 1)
''')
connection.commit()



# import pyodbc
# import sys
# import io

# # Đổi mã hóa đầu ra của bảng điều khiển sang UTF-8
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# # Chuỗi kết nối cơ sở dữ liệu
# connection_string = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     'SERVER=PHONG-VU\\SQLEXPRESS;'  # Dấu gạch chéo ngược phải được thoát trong chuỗi
#     'DATABASE=QuanLySinhVien;'
#     'UID=sa;'
#     'PWD=223003'
# )

# # Kết nối lại cơ sở dữ liệu
# connection = pyodbc.connect(connection_string)
# cursor = connection.cursor()

# # Truy vấn dữ liệu từ bảng SinhVien
# cursor.execute('SELECT * FROM SinhVien')
# sinhvien_data = cursor.fetchall()

# # Truy vấn dữ liệu từ bảng LopHoc
# cursor.execute('SELECT * FROM LopHoc')
# lophoc_data = cursor.fetchall()

# # Truy vấn dữ liệu từ bảng MonHoc
# cursor.execute('SELECT * FROM MonHoc')
# monhoc_data = cursor.fetchall()

# # Truy vấn dữ liệu từ bảng DangKy
# cursor.execute('SELECT * FROM DangKy')
# dangky_data = cursor.fetchall()

# # Truy vấn dữ liệu từ bảng Login
# cursor.execute('SELECT * FROM Login')
# login_data = cursor.fetchall()

# # Đóng kết nối sau khi truy vấn
# connection.close()

# # In kết quả truy vấn
# print("Bảng SinhVien:")
# for row in sinhvien_data:
#     print(row)

# print("\nBảng LopHoc:")
# for row in lophoc_data:
#     print(row)

# print("\nBảng MonHoc:")
# for row in monhoc_data:
#     print(row)

# print("\nBảng DangKy:")
# for row in dangky_data:
#     print(row)

# print("\nBảng Login:")
# for row in login_data:
#     print(row)


# import pyodbc
# import sys
# import io

# # Đổi mã hóa đầu ra của bảng điều khiển sang UTF-8
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# # Chuỗi kết nối cơ sở dữ liệu
# connection_string = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     'SERVER=PHONG-VU\\SQLEXPRESS;'  # Dấu gạch chéo ngược phải được thoát trong chuỗi
#     'DATABASE=QuanLySinhVien;'
#     'UID=sa;'
#     'PWD=223003'
# )

# # Kết nối cơ sở dữ liệu
# connection = pyodbc.connect(connection_string)
# cursor = connection.cursor()

# # Xóa sinh viên theo mã sinh viên
# ma_sv_can_xoa = 1  # Thay đổi mã sinh viên cần xóa tại đây
# cursor.execute('DELETE FROM DangKy WHERE MaSV = ?', ma_sv_can_xoa)  # Xóa trong bảng DangKy trước
# cursor.execute('DELETE FROM SinhVien WHERE MaSV = ?', ma_sv_can_xoa)
# connection.commit()

# # Truy vấn dữ liệu từ bảng SinhVien để kiểm tra kết quả
# cursor.execute('SELECT * FROM SinhVien')
# sinhvien_data = cursor.fetchall()

# # Đóng kết nối sau khi truy vấn
# connection.close()

# # In kết quả truy vấn
# print("Bảng SinhVien sau khi xóa:")
# for row in sinhvien_data:
#     print(row)