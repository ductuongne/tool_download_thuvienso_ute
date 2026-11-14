# UTE Library PDF Extractor (ĐÃ NGỪNG HOẠT ĐỘNG)

> ⚠️ **Lưu ý quan trọng:** Tool hiện **không còn hoạt động** và được public source ở đây **chỉ nhằm mục đích tham khảo kỹ thuật / học thuật**, không nhằm mục đích sử dụng thực tế.

## Giới thiệu

Đây là một script Python nhỏ từng được dùng để tải và giải mã nội dung PDF từ một endpoint nội bộ của hệ thống thư viện số HCMUTE. Endpoint này trước đây trả về nội dung PDF dưới dạng chuỗi Base64 không yêu cầu xác thực.

Script thực hiện các bước:
1. Nhận URL trang xem tài liệu, trích ID tài liệu từ URL.
2. Gọi tới endpoint `loadpdf2` với ID đó.
3. Làm sạch response.
4. Giải mã Base64 thành file PDF.

## Vì sao không còn dùng được

Phía nền tảng đã thay đổi cơ chế trả dữ liệu của endpoint (có thể đã thêm xác thực, mã hóa khác, hoặc chặn truy cập trực tiếp), nên luồng tải → giải mã Base64 như cũ không còn trả về PDF hợp lệ.

## Giá trị tham khảo

Dù không còn hoạt động, code có thể hữu ích để tham khảo về:
- Cách xử lý và làm sạch chuỗi Base64 từ response HTTP.
- Cách dùng `regex` để trích ID từ URL.
- Cách dùng PyMuPDF (`fitz`) để kiểm tra và render PDF.
- Một ví dụ thực tế về lỗ hổng bảo mật dạng "trả dữ liệu nhạy cảm không xác thực" — một lớp lỗi khá phổ biến trong các hệ thống quản lý tài liệu nội bộ.

## Disclaimer

- Tool này **không** dùng để vượt qua các cơ chế bảo vệ bản quyền tài liệu hiện tại.
- Tool được tạo ra **chỉ với mục đích học tập và tìm hiểu về cách hoạt động của hệ thống**, không nhằm mục đích khai thác hay sử dụng trái phép.
- Không khuyến khích và không chịu trách nhiệm cho việc sử dụng sai mục đích.
