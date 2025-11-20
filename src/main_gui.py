"""
Giao diện GUI cho phần mềm quản lý phát âm thanh theo lịch
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
from datetime import datetime

# Thêm thư mục src vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio_player import AudioPlayer
from scheduler import ScheduleManager


class AudioSchedulerGUI:
    """Giao diện chính của ứng dụng"""

    def __init__(self, root):
        """
        Khởi tạo giao diện

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Quản Lý Phát Âm Thanh Theo Lịch")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)

        # Maximize cửa sổ khi khởi động
        self.root.state('zoomed')

        # Cấu hình style
        self.setup_style()

        # Khởi tạo audio player và scheduler
        self.player = AudioPlayer()
        self.scheduler = ScheduleManager()
        self.scheduler.set_playback_callback(self.auto_play_callback)

        # Biến cho checkbox ngày
        self.day_vars = []

        # Tạo giao diện
        self.create_widgets()

        # Bắt đầu scheduler
        self.scheduler.start()

        # Tải danh sách lịch
        self.refresh_schedule_list()

        # Cập nhật đồng hồ
        self.update_clock()

    def setup_style(self):
        """Cấu hình style cho giao diện"""
        style = ttk.Style()
        style.theme_use('clam')

        # Cấu hình màu sắc
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 11, 'bold'))
        style.configure('Clock.TLabel', font=('Segoe UI', 28, 'bold'), foreground='#2196F3')
        style.configure('Date.TLabel', font=('Segoe UI', 12), foreground='#333')
        style.configure('Status.TLabel', font=('Segoe UI', 9), foreground='#666')

        # Nút chính
        style.configure('Primary.TButton', font=('Segoe UI', 10))
        style.configure('Success.TButton', font=('Segoe UI', 10))
        style.configure('Danger.TButton', font=('Segoe UI', 10))

    def create_widgets(self):
        """Tạo các widget cho giao diện"""

        # Frame chính
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # === HEADER VỚI ĐỒNG HỒ VÀ NGÀY THÁNG ===
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)

        ttk.Label(header_frame, text="Quản Lý Phát Âm Thanh Theo Lịch",
                  style='Title.TLabel').grid(row=0, column=0, sticky=tk.W)

        # Khung thời gian và ngày tháng
        datetime_frame = ttk.LabelFrame(header_frame, text="", padding="10")
        datetime_frame.grid(row=0, column=2, sticky=tk.E)

        self.clock_label = ttk.Label(datetime_frame, text="00:00:00", style='Clock.TLabel')
        self.clock_label.pack()

        self.date_label = ttk.Label(datetime_frame, text="", style='Date.TLabel')
        self.date_label.pack()

        # === PHẦN PHÁT THỦ CÔNG ===
        manual_frame = ttk.LabelFrame(main_frame, text="  Phát Thủ Công  ", padding="15")
        manual_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        manual_frame.columnconfigure(1, weight=1)

        # Chọn file
        ttk.Label(manual_frame, text="File âm thanh:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=8)
        self.file_entry = ttk.Entry(manual_frame, font=('Segoe UI', 10))
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=8)
        ttk.Button(manual_frame, text="Chọn File", command=self.browse_file,
                   style='Primary.TButton').grid(row=0, column=2, pady=8)

        # Nút điều khiển và âm lượng
        control_frame = ttk.Frame(manual_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(control_frame, text="  Phát  ", command=self.play_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="  Tạm dừng  ", command=self.pause_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="  Dừng  ", command=self.stop_audio).pack(side=tk.LEFT, padx=5)

        # Âm lượng
        ttk.Separator(control_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=15, fill=tk.Y)
        ttk.Label(control_frame, text="Âm lượng:").pack(side=tk.LEFT, padx=5)
        self.volume_scale = ttk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.on_volume_change, length=150)
        self.volume_scale.set(100)
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        self.volume_label = ttk.Label(control_frame, text="100%", width=5)
        self.volume_label.pack(side=tk.LEFT)

        # === PHẦN THÊM LỊCH MỚI ===
        schedule_frame = ttk.LabelFrame(main_frame, text="  Thêm Lịch Mới  ", padding="15")
        schedule_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        schedule_frame.columnconfigure(1, weight=1)

        # Tên lịch
        ttk.Label(schedule_frame, text="Tên lịch:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=8)
        self.schedule_name_entry = ttk.Entry(schedule_frame, font=('Segoe UI', 10))
        self.schedule_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10, pady=8)

        # File âm thanh
        ttk.Label(schedule_frame, text="File âm thanh:", style='Header.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=8)
        self.schedule_file_entry = ttk.Entry(schedule_frame, font=('Segoe UI', 10))
        self.schedule_file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=8)
        ttk.Button(schedule_frame, text="Chọn", command=self.browse_schedule_file).grid(
            row=1, column=2, pady=8)

        # Thời gian
        ttk.Label(schedule_frame, text="Thời gian:", style='Header.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=8)
        time_frame = ttk.Frame(schedule_frame)
        time_frame.grid(row=2, column=1, sticky=tk.W, padx=10, pady=8)

        self.hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=5, format="%02.0f",
                                        font=('Segoe UI', 11))
        self.hour_spinbox.set("08")
        self.hour_spinbox.pack(side=tk.LEFT)

        ttk.Label(time_frame, text=" : ", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)

        self.minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=5, format="%02.0f",
                                          font=('Segoe UI', 11))
        self.minute_spinbox.set("00")
        self.minute_spinbox.pack(side=tk.LEFT)

        # Chọn ngày trong tuần
        ttk.Label(schedule_frame, text="Các ngày phát:", style='Header.TLabel').grid(
            row=3, column=0, sticky=tk.W, pady=8)

        days_frame = ttk.Frame(schedule_frame)
        days_frame.grid(row=3, column=1, sticky=tk.W, padx=10, pady=8)

        day_names = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']
        self.day_vars = []

        for i, day in enumerate(day_names):
            var = tk.BooleanVar(value=True)
            self.day_vars.append(var)
            cb = ttk.Checkbutton(days_frame, text=day, variable=var)
            cb.pack(side=tk.LEFT, padx=5)

        # Nút chọn nhanh
        quick_frame = ttk.Frame(schedule_frame)
        quick_frame.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)

        ttk.Button(quick_frame, text="Tất cả", command=self.select_all_days).pack(side=tk.LEFT, padx=3)
        ttk.Button(quick_frame, text="Ngày thường", command=self.select_weekdays).pack(side=tk.LEFT, padx=3)
        ttk.Button(quick_frame, text="Cuối tuần", command=self.select_weekend).pack(side=tk.LEFT, padx=3)
        ttk.Button(quick_frame, text="Bỏ chọn", command=self.deselect_all_days).pack(side=tk.LEFT, padx=3)

        # Nút thêm lịch
        add_btn_frame = ttk.Frame(schedule_frame)
        add_btn_frame.grid(row=5, column=0, columnspan=3, pady=15)
        ttk.Button(add_btn_frame, text="  Thêm Lịch  ", command=self.add_schedule,
                   style='Success.TButton').pack()

        # === DANH SÁCH LỊCH ===
        list_frame = ttk.LabelFrame(main_frame, text="  Danh Sách Lịch Trình  ", padding="15")
        list_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Treeview
        columns = ('Tên', 'Thời gian', 'Các ngày', 'File', 'Trạng thái')
        self.schedule_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)

        # Định nghĩa cột
        self.schedule_tree.column('Tên', width=150, minwidth=100)
        self.schedule_tree.column('Thời gian', width=80, minwidth=60)
        self.schedule_tree.column('Các ngày', width=150, minwidth=100)
        self.schedule_tree.column('File', width=250, minwidth=150)
        self.schedule_tree.column('Trạng thái', width=80, minwidth=60)

        # Định nghĩa tiêu đề
        for col in columns:
            self.schedule_tree.heading(col, text=col, anchor=tk.W)

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.schedule_tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.schedule_tree.xview)
        self.schedule_tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        self.schedule_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Nút quản lý
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="  Làm mới  ", command=self.refresh_schedule_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="  Xóa  ", command=self.delete_schedule,
                   style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="  Bật/Tắt  ", command=self.toggle_schedule).pack(side=tk.LEFT, padx=5)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        self.status_label = ttk.Label(status_frame,
                                      text="Sẵn sàng - Ứng dụng đang chạy và theo dõi lịch trình",
                                      style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT)

    def update_clock(self):
        """Cập nhật đồng hồ và ngày tháng"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        self.clock_label.config(text=time_str)

        # Tên các ngày và tháng bằng tiếng Việt
        day_names = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']
        day_name = day_names[now.weekday()]
        date_str = f"{day_name}, {now.day:02d}/{now.month:02d}/{now.year}"
        self.date_label.config(text=date_str)

        self.root.after(1000, self.update_clock)

    def select_all_days(self):
        """Chọn tất cả các ngày"""
        for var in self.day_vars:
            var.set(True)

    def deselect_all_days(self):
        """Bỏ chọn tất cả các ngày"""
        for var in self.day_vars:
            var.set(False)

    def select_weekdays(self):
        """Chọn ngày thường (T2-T6)"""
        for i, var in enumerate(self.day_vars):
            var.set(i < 5)

    def select_weekend(self):
        """Chọn cuối tuần (T7, CN)"""
        for i, var in enumerate(self.day_vars):
            var.set(i >= 5)

    def browse_file(self):
        """Chọn file âm thanh để phát thủ công"""
        filename = filedialog.askopenfilename(
            title="Chọn file âm thanh",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg *.flac *.mid *.midi"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("MIDI files", "*.mid *.midi"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)

    def browse_schedule_file(self):
        """Chọn file âm thanh cho lịch"""
        filename = filedialog.askopenfilename(
            title="Chọn file âm thanh",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg *.flac *.mid *.midi"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("MIDI files", "*.mid *.midi"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.schedule_file_entry.delete(0, tk.END)
            self.schedule_file_entry.insert(0, filename)

    def play_audio(self):
        """Phát file âm thanh"""
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file âm thanh!")
            return

        if self.player.play(file_path):
            self.status_label.config(text=f"Đang phát: {os.path.basename(file_path)}")

    def pause_audio(self):
        """Tạm dừng phát"""
        self.player.pause()
        self.status_label.config(text="Đã tạm dừng phát")

    def stop_audio(self):
        """Dừng phát"""
        self.player.stop()
        self.status_label.config(text="Đã dừng phát")

    def on_volume_change(self, value):
        """Callback khi thay đổi âm lượng"""
        volume = float(value) / 100.0
        self.player.set_volume(volume)
        self.volume_label.config(text=f"{int(float(value))}%")

    def add_schedule(self):
        """Thêm lịch mới"""
        name = self.schedule_name_entry.get().strip()
        audio_file = self.schedule_file_entry.get().strip()
        hour = self.hour_spinbox.get()
        minute = self.minute_spinbox.get()

        if not name or not audio_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tên lịch và chọn file âm thanh!")
            return

        if not os.path.exists(audio_file):
            messagebox.showerror("Lỗi", "File âm thanh không tồn tại!")
            return

        # Lấy các ngày đã chọn
        days_of_week = [i for i, var in enumerate(self.day_vars) if var.get()]

        if not days_of_week:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một ngày trong tuần!")
            return

        schedule_time = f"{int(hour):02d}:{int(minute):02d}"

        self.scheduler.add_schedule(name, audio_file, schedule_time, True, True, days_of_week)

        # Hiển thị các ngày đã chọn
        day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        days_str = ', '.join([day_names[d] for d in days_of_week])

        messagebox.showinfo("Thành công", f"Đã thêm lịch: {name}\nThời gian: {schedule_time}\nCác ngày: {days_str}")

        # Xóa form
        self.schedule_name_entry.delete(0, tk.END)
        self.schedule_file_entry.delete(0, tk.END)

        # Làm mới danh sách
        self.refresh_schedule_list()

        self.status_label.config(text=f"Đã thêm lịch mới: {name}")

    def refresh_schedule_list(self):
        """Làm mới danh sách lịch"""
        # Xóa danh sách cũ
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        # Thêm lịch mới
        for schedule in self.scheduler.get_schedules():
            self.schedule_tree.insert('', tk.END, iid=schedule.schedule_id, values=(
                schedule.name,
                schedule.schedule_time,
                schedule.get_days_display(),
                os.path.basename(schedule.audio_file),
                "Bật" if schedule.enabled else "Tắt"
            ))

        count = len(self.scheduler.get_schedules())
        self.status_label.config(text=f"Đã tải {count} lịch trình")

    def delete_schedule(self):
        """Xóa lịch đã chọn"""
        selection = self.schedule_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch cần xóa!")
            return

        schedule_id = selection[0]
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa lịch này?"):
            self.scheduler.remove_schedule(schedule_id)
            self.refresh_schedule_list()
            messagebox.showinfo("Thành công", "Đã xóa lịch!")

    def toggle_schedule(self):
        """Bật/tắt lịch đã chọn"""
        selection = self.schedule_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch!")
            return

        schedule_id = selection[0]
        for schedule in self.scheduler.get_schedules():
            if schedule.schedule_id == schedule_id:
                new_status = not schedule.enabled
                self.scheduler.update_schedule(schedule_id, enabled=new_status)
                self.refresh_schedule_list()
                status_text = "bật" if new_status else "tắt"
                self.status_label.config(text=f"Đã {status_text} lịch: {schedule.name}")
                break

    def auto_play_callback(self, audio_file, schedule_name):
        """Callback khi scheduler tự động phát"""
        self.player.play(audio_file)
        # Cập nhật status
        self.status_label.config(text=f"Đang phát theo lịch: {schedule_name}")
        # Hiển thị thông báo
        self.show_notification(f"Đang phát theo lịch: {schedule_name}")

    def show_notification(self, message):
        """Hiển thị thông báo"""
        # Tạo cửa sổ thông báo nhỏ
        notification = tk.Toplevel(self.root)
        notification.title("Thông báo")
        notification.geometry("350x100")
        notification.resizable(False, False)

        # Đặt vị trí góc phải dưới màn hình
        screen_width = notification.winfo_screenwidth()
        screen_height = notification.winfo_screenheight()
        x = screen_width - 370
        y = screen_height - 150
        notification.geometry(f"+{x}+{y}")

        ttk.Label(notification, text=message, font=('Segoe UI', 11),
                  wraplength=330).pack(pady=20, padx=10)

        # Tự động đóng sau 5 giây
        notification.after(5000, notification.destroy)

    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        self.scheduler.stop()
        self.player.stop()
        self.root.destroy()


def main():
    """Hàm chính"""
    root = tk.Tk()
    app = AudioSchedulerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
