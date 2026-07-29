[![Quyên góp](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=DB9N3QDZLR822)

# Trình đọc thanh tiến trình – tiện ích bổ sung NVDA
(C) 2025, Imam Kahraman

Giấy phép: Giấy phép Công cộng GNU v3 (GPL-3.0) (xem tệp GIẤY PHÉP: https://www.gnu.org/licenses/gpl-3.0.txt)

Tiện ích bổ sung NVDA này cho phép bạn đọc các thanh tiến trình trong nhiều ứng dụng khác nhau và thông báo tiến trình hiện tại bằng giọng nói.  
Thanh tiến trình được nhận dạng thông qua nhiều giao diện để đảm bảo khả năng tương thích rộng rãi với các công nghệ phần mềm khác nhau.  
Ngoài ra, tiện ích bổ sung này còn cung cấp **một cửa sổ tự động làm mới** của riêng nó với hộp văn bản nhiều dòng, chỉ đọc, tự động cập nhật tiến trình.

[Nhấp vào đây để tải xuống phiên bản hiện tại](https://davidacm.github.io/getlatest/gh/vbprofi/Progress-Reader-NVDA-Addon/)

---

## Mục lục

1. Cài đặt tiện ích bổ sung
2. Sử dụng tiện ích bổ sung
3. Lưu ý về chức năng
4. Lịch sử phiên bản
5. Giấy phép & Tuyên bố từ chối trách nhiệm

---

## 1) Cài đặt tiện ích bổ sung

### Cài đặt qua Cửa hàng tiện ích NVDA
1. Mở NVDA và điều hướng đến Công cụ > Cửa hàng tiện ích bổ sung.
2. Tìm kiếm "Trình đọc thanh tiến trình" và chọn nó.
3. Nhấp vào "Cài đặt" và làm theo hướng dẫn.
4. Khởi động lại NVDA để kích hoạt tiện ích bổ sung.

### Cài đặt thủ công (tệp .nvda-addon)
#### Nếu tiện ích bổ sung không có sẵn trong cửa hàng tiện ích bổ sung:
1. Tải xuống tệp `.nvda-addon`. [Nhấp vào đây để tải xuống phiên bản hiện tại](https://davidacm.github.io/getlatest/gh/vbprofi/Progress-Reader-NVDA-Addon/)
2. Mở NVDA và điều hướng đến Công cụ > Cửa hàng tiện ích bổ sung.
3. Nhấp vào "Cài đặt từ nguồn bên ngoài..." và chọn tệp `.nvda-addon`.
4. Xác nhận cài đặt và khởi động lại NVDA để kích hoạt tiện ích bổ sung.

---

## 2) Cách sử dụng tiện ích bổ sung

1. **Chuyển sang ứng dụng có thanh tiến trình hoạt động (ví dụ: truyền tệp, thanh tải, cài đặt phần mềm).**
2. **Nhấn NVDA + Shift + R để mở cửa sổ Tự động làm mới.**  
   - Khi cửa sổ mở ra, các thanh tiến trình được phát hiện sẽ tự động được theo dõi.  
   - Cửa sổ hiển thị liên tục tiến trình trong hộp văn bản nhiều dòng, chỉ đọc.  
   - Tiêu điểm tự động chuyển đến dòng đầu tiên sau mỗi lần cập nhật.  
   - Nhấn NVDA + Shift + R lần nữa để đóng cửa sổ.
3. **Nhấn NVDA + Shift + U để thay đổi khoảng thời gian làm mới (tính bằng giây).**

---

## 3) Lưu ý về chức năng

- Nếu có nhiều thanh tiến trình trong cửa sổ đang hoạt động, tất cả các thanh tiến trình được phát hiện sẽ được theo dõi và hiển thị trong một cửa sổ tự động làm mới.
- Nếu không tìm thấy thanh tiến trình, NVDA sẽ thông báo "Không tìm thấy thanh tiến trình".
- Nếu không thể xác định được giá trị tiến trình hoặc giá trị tối đa thì tiện ích bổ sung sẽ giả định giá trị mặc định là 0–100%.
- Một số ứng dụng sử dụng các thành phần UI độc quyền không thể được nhận dạng theo mặc định.
- Tất cả các tổ hợp phím đều có thể được cấu hình thông qua thao tác nhập của NVDA và người dùng có thể tùy chỉnh.

---

## 4) Lịch sử phiên bản

### v0.3.0
- Cửa sổ đầu ra hiện sử dụng hộp văn bản nhiều dòng, chỉ đọc.
- Tự động lấy nét vào hộp văn bản khi mở, con trỏ nhảy về dòng đầu tiên khi cập nhật.
- Hộp thoại cài đặt đã thay đổi: Nhập khoảng thời gian tính bằng giây (nội bộ vẫn là mili giây).
- Nút đặt lại trong hộp thoại cài đặt sẽ đặt lại khoảng thời gian về giá trị mặc định.
- Nút "Quyên góp" mới trong hộp thoại cài đặt sẽ mở trang PayPal trong trình duyệt tiêu chuẩn.
- Các thanh tiến trình được phát hiện sẽ tự động được theo dõi khi cửa sổ tự động làm mới được mở.
- Tất cả các chuỗi giao diện người dùng được chuẩn bị để dịch.
- Cử chỉ được đăng ký qua @script-decorator để người dùng có thể tùy chỉnh chúng trong hộp thoại cử chỉ nhập của NVDA.

### v0.2.5
- Đã cập nhật cho NVDA 2025.3.2.
- Đã thêm ngôn ngữ mới tiếng Ukraina (uk UA).

### v0.2.4
- Đã cập nhật cho NVDA 2025.2.

### v0.2.3
- Đã cập nhật cho NVDA 2025.1.2.
- Đã thêm ngôn ngữ mới Tiếng Trung giản thể (zh CN).

### v0.2.2
- Đã cập nhật cho NVDA 2025.1.1.

### v0.2.1
- Đã cập nhật cho NVDA 2024.4.2.

### v0.2.0
- Đã thêm dòng bình luận cho người dịch.
- Dọn dẹp mã: Đã xóa phương thức gỡ lỗi vì nó không còn cần thiết nữa.
- Đã thêm dòng bình luận mô tả tệp tiện ích bổ sung bao gồm cả phiên bản tệp.

### v0.1.7
- Sửa lỗi: Phát hiện chính xác các thanh tiến trình - ngăn hiển thị sai "tiến trình 0%".
- Cải thiện các tệp ngôn ngữ.

### v0.1.6
- Các thanh tiến trình được phát hiện sẽ được hiển thị trong cửa sổ đầu ra.
- Tổ hợp phím có thể được thay đổi thông qua hộp thoại cài đặt: Tiện ích bổ sung được hiển thị theo danh mục riêng.

### v0.1.5
- Chuyển thụt lề trong mã sang tab.
- Đã thêm bản dịch tiếng Anh.
- Đã sửa lỗi trong tệp README.

### v0.1.4
- Đã sửa lỗi: Phát hiện các thành phần UI trong hộp thoại sao chép và di chuyển của Windows.

### v0.1.3
- Tổ hợp phím được đổi thành NVDA + SHIFT + U.
- Cập nhật phím tắt trong tệp README.
- Mã đã được làm sạch.
- Sử dụng GPL-3.0.

### v0.1.2
- Tệp README được cải thiện và thêm hướng dẫn sử dụng.
- Hỗ trợ mở rộng cho các công nghệ UI khác nhau:
  - Điều khiển Windows gốc (thanh tiến trình cổ điển)
  - WPF/WinForms (công nghệ Microsoft .NET)
  - wxPython/wxWidgets (ví dụ: `wx.Gauge`)
  - Các ứng dụng Java (với các API hỗ trợ tiếp cận phù hợp)
  - Thanh tiến trình dựa trên web (tùy thuộc vào trình duyệt và hỗ trợ ARIA)

### v0.1.0
- Phiên bản đầu tiên có chức năng cơ bản để nhận dạng và đọc thanh tiến trình.

---

## 5) Giấy phép & Tuyên bố từ chối trách nhiệm  

Tiện ích bổ sung này được phát hành theo Giấy phép Công cộng GNU v3 (GPL-3.0). Xem tệp GIẤY PHÉP để biết thêm thông tin. Tệp này có sẵn ở đây: https://www.gnu.org/licenses/gpl-3.0.txt

### Điều khoản cấp phép:
- Tiện ích bổ sung này là phần mềm mã nguồn mở và có thể được sử dụng, sửa đổi và phân phối theo các điều khoản của giấy phép GPL-3.0.  
- Mọi sửa đổi phải được xuất bản theo cùng một giấy phép (GPL-3.0).

### Tuyên bố từ chối trách nhiệm:
Tiện ích bổ sung này được cung cấp mà không có bất kỳ sự đảm bảo nào. Tác giả không chịu trách nhiệm về bất kỳ thiệt hại hoặc mất dữ liệu nào có thể xảy ra do việc sử dụng tiện ích bổ sung này.

(C) 2025, Imam Kahraman

Giấy phép: Giấy phép Công cộng GNU v3 (GPL-3.0) (xem tệp GIẤY PHÉP: https://www.gnu.org/licenses/gpl-3.0.txt)

[Quyên góp qua PayPal](https://www.paypal.com/donate/?hosted_button_id=DB9N3QDZLR822)