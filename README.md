# Phần Mềm Quản Lý Phát Âm Thanh

Phần mềm quản lý và phát âm thanh tự động theo lịch trình được hẹn trước.

## Tính năng

- ✅ Phát file âm thanh (MP3, WAV, OGG, FLAC)
- ✅ Hẹn lịch phát âm thanh theo giờ
- ✅ Lặp lại hàng ngày
- ✅ Quản lý nhiều lịch trình
- ✅ Điều chỉnh âm lượng
- ✅ Giao diện đồ họa đơn giản, dễ sử dụng

## Cài đặt

### Yêu cầu
- Python 3.7 trở lên
- Hệ điều hành: Windows, Linux, macOS

### Các bước cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd ring
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy phần mềm

```bash
python src/main_gui.py
```

### Hướng dẫn sử dụng

#### 1. Phát âm thanh thủ công

- Nhấn nút **"Chọn File"** để chọn file âm thanh
- Nhấn **"▶ Phát"** để phát file
- Sử dụng **"⏸ Tạm dừng"** và **"⏹ Dừng"** để điều khiển
- Kéo thanh âm lượng để điều chỉnh

#### 2. Thêm lịch phát tự động

- Nhập **tên lịch** (ví dụ: "Chuông báo thức")
- Chọn **file âm thanh** muốn phát
- Chọn **thời gian** phát (giờ và phút)
- Đánh dấu **"Lặp lại hàng ngày"** nếu muốn phát mỗi ngày
- Nhấn **"➕ Thêm Lịch"**

#### 3. Quản lý lịch trình

- Xem danh sách các lịch đã tạo trong bảng
- Chọn một lịch và nhấn **"🗑️ Xóa"** để xóa
- Chọn một lịch và nhấn **"⏯️ Bật/Tắt"** để tạm thời vô hiệu hóa
- Nhấn **"🔄 Làm mới"** để cập nhật danh sách

## Cấu trúc dự án

```
ring/
├── src/
│   ├── __init__.py          # Module init
│   ├── audio_player.py      # Module phát âm thanh
│   ├── scheduler.py         # Module quản lý lịch trình
│   └── main_gui.py          # Giao diện chính
├── schedules/
│   └── schedules.json       # File lưu lịch trình (tự động tạo)
├── data/                    # Thư mục lưu file âm thanh (tùy chọn)
├── requirements.txt         # Danh sách thư viện
└── README.md               # File này
```

## Các module chính

### audio_player.py
Module xử lý phát âm thanh sử dụng pygame:
- `AudioPlayer`: Class quản lý phát/dừng/tạm dừng âm thanh
- Hỗ trợ điều chỉnh âm lượng
- Kiểm tra trạng thái phát

### scheduler.py
Module quản lý lịch trình:
- `AudioSchedule`: Class đại diện cho một lịch phát
- `ScheduleManager`: Class quản lý danh sách lịch
- Tự động lưu/tải lịch từ file JSON
- Chạy background thread để kiểm tra và thực thi lịch

### main_gui.py
Giao diện đồ họa sử dụng Tkinter:
- Phần phát thủ công với điều khiển đầy đủ
- Form thêm lịch trình mới
- Bảng hiển thị và quản lý lịch

## Ví dụ sử dụng

### Tạo lịch báo thức buổi sáng
1. Chọn file nhạc báo thức (ví dụ: alarm.mp3)
2. Đặt tên: "Báo thức buổi sáng"
3. Đặt thời gian: 07:00
4. Bật "Lặp lại hàng ngày"
5. Nhấn "Thêm Lịch"

### Tạo lịch phát nhạc giải lao
1. Chọn file nhạc (ví dụ: break_music.mp3)
2. Đặt tên: "Giải lao"
3. Đặt thời gian: 10:00
4. Bật "Lặp lại hàng ngày"
5. Nhấn "Thêm Lịch"

## Lưu ý

- File âm thanh cần tồn tại tại đường dẫn đã chọn
- Lịch trình được lưu tự động vào file `schedules/schedules.json`
- Phần mềm cần chạy liên tục để lịch tự động hoạt động
- Âm lượng mặc định là 100%
- Hỗ trợ định dạng: MP3, WAV, OGG, FLAC

## Xử lý lỗi thường gặp

### "File không tồn tại"
- Kiểm tra đường dẫn file âm thanh
- Đảm bảo file chưa bị di chuyển hoặc xóa

### "Lỗi khi phát âm thanh"
- Kiểm tra định dạng file có được hỗ trợ
- Thử với file âm thanh khác
- Đảm bảo pygame đã được cài đặt đúng

### Lịch không tự động phát
- Kiểm tra lịch đã được bật (cột "Trạng thái" = "Bật")
- Kiểm tra thời gian đã đặt đúng chưa
- Đảm bảo phần mềm đang chạy

## Phát triển thêm

Các tính năng có thể mở rộng:
- [ ] Thêm lịch phát theo ngày trong tuần
- [ ] Fade in/out khi phát
- [ ] Playlist support
- [ ] Giao diện tùy chỉnh theme
- [ ] Xuất/nhập lịch trình
- [ ] System tray integration

## License

MIT License

## Tác giả

Audio Scheduler Team
