# Hướng Dẫn Tải Trực Tiếp Từ Tài Khoản Study4

Study4 (`study4.com`) bảo vệ hệ thống làm bài thi bằng cơ chế tài khoản người dùng (`sessionid`).

### Cách lấy Cookie để cào trực tiếp từ tài khoản của bạn:
1. Mở trình duyệt và đăng nhập vào `https://study4.com`.
2. Mở Developer Tools (bấm F12 hoặc chuột phải -> Inspect).
3. Chuyển sang tab **Application** (hoặc Storage) -> **Cookies** -> `https://study4.com`.
4. Tìm giá trị của `sessionid` và sao chép.
5. Chạy lệnh:
   ```bash
   python3 data_pipeline.py --study4-cookie "<GIA_TRI_SESSION_ID>" --test-id 6846
   ```
