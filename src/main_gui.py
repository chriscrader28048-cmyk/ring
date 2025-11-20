"""
Giao diện GUI cho phần mềm quản lý phát âm thanh
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys

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
        self.root.title("Quản Lý Phát Âm Thanh")
        self.root.geometry("900x600")

        # Khởi tạo audio player và scheduler
        self.player = AudioPlayer()
        self.scheduler = ScheduleManager()
        self.scheduler.set_playback_callback(self.auto_play_callback)

        # Tạo giao diện
        self.create_widgets()

        # Bắt đầu scheduler
        self.scheduler.start()

        # Tải danh sách lịch
        self.refresh_schedule_list()

    def create_widgets(self):
        """Tạo các widget cho giao diện"""

        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # === PHẦN PHÁT THỦ CÔNG ===
        manual_frame = ttk.LabelFrame(main_frame, text="Phát Thủ Công", padding="10")
        manual_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        manual_frame.columnconfigure(1, weight=1)

        # Chọn file
        ttk.Label(manual_frame, text="File âm thanh:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_entry = ttk.Entry(manual_frame)
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(manual_frame, text="Chọn File", command=self.browse_file).grid(row=0, column=2, pady=5)

        # Nút điều khiển
        control_frame = ttk.Frame(manual_frame)
        control_frame.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(control_frame, text="▶ Phát", command=self.play_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⏸ Tạm dừng", command=self.pause_audio).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⏹ Dừng", command=self.stop_audio).pack(side=tk.LEFT, padx=5)

        # Âm lượng
        volume_frame = ttk.Frame(manual_frame)
        volume_frame.grid(row=2, column=0, columnspan=3, pady=5)
        ttk.Label(volume_frame, text="Âm lượng:").pack(side=tk.LEFT, padx=5)
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.on_volume_change, length=200)
        self.volume_scale.set(100)
        self.volume_scale.pack(side=tk.LEFT, padx=5)
        self.volume_label = ttk.Label(volume_frame, text="100%")
        self.volume_label.pack(side=tk.LEFT, padx=5)

        # === PHẦN QUẢN LÝ LỊCH ===
        schedule_frame = ttk.LabelFrame(main_frame, text="Quản Lý Lịch Trình", padding="10")
        schedule_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        schedule_frame.columnconfigure(1, weight=1)

        # Tên lịch
        ttk.Label(schedule_frame, text="Tên lịch:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.schedule_name_entry = ttk.Entry(schedule_frame)
        self.schedule_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # File âm thanh
        ttk.Label(schedule_frame, text="File âm thanh:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.schedule_file_entry = ttk.Entry(schedule_frame)
        self.schedule_file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(schedule_frame, text="Chọn", command=self.browse_schedule_file).grid(row=1, column=2, pady=5)

        # Thời gian
        ttk.Label(schedule_frame, text="Thời gian (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=5)
        time_frame = ttk.Frame(schedule_frame)
        time_frame.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        self.hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, width=5, format="%02.0f")
        self.hour_spinbox.set("08")
        self.hour_spinbox.pack(side=tk.LEFT)

        ttk.Label(time_frame, text=":").pack(side=tk.LEFT, padx=2)

        self.minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, width=5, format="%02.0f")
        self.minute_spinbox.set("00")
        self.minute_spinbox.pack(side=tk.LEFT)

        # Lặp lại hàng ngày
        self.repeat_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(schedule_frame, text="Lặp lại hàng ngày",
                       variable=self.repeat_var).grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Nút thêm lịch
        ttk.Button(schedule_frame, text="➕ Thêm Lịch", command=self.add_schedule).grid(row=4, column=1, pady=10)

        # === DANH SÁCH LỊCH ===
        list_frame = ttk.LabelFrame(main_frame, text="Danh Sách Lịch Trình", padding="10")
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Treeview
        columns = ('Tên', 'Thời gian', 'File', 'Lặp lại', 'Trạng thái')
        self.schedule_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=10)

        # Định nghĩa cột
        self.schedule_tree.column('#0', width=0, stretch=tk.NO)
        self.schedule_tree.column('Tên', width=150)
        self.schedule_tree.column('Thời gian', width=100)
        self.schedule_tree.column('File', width=300)
        self.schedule_tree.column('Lặp lại', width=80)
        self.schedule_tree.column('Trạng thái', width=100)

        # Định nghĩa tiêu đề
        self.schedule_tree.heading('Tên', text='Tên')
        self.schedule_tree.heading('Thời gian', text='Thời gian')
        self.schedule_tree.heading('File', text='File')
        self.schedule_tree.heading('Lặp lại', text='Lặp lại')
        self.schedule_tree.heading('Trạng thái', text='Trạng thái')

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscroll=scrollbar.set)

        self.schedule_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Nút quản lý
        button_frame = ttk.Frame(list_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="🔄 Làm mới", command=self.refresh_schedule_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Xóa", command=self.delete_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏯️ Bật/Tắt", command=self.toggle_schedule).pack(side=tk.LEFT, padx=5)

    def browse_file(self):
        """Chọn file âm thanh để phát thủ công"""
        filename = filedialog.askopenfilename(
            title="Chọn file âm thanh",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.ogg *.flac"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
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
                ("Audio files", "*.mp3 *.wav *.ogg *.flac"),
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
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
            messagebox.showinfo("Thông báo", f"Đang phát: {os.path.basename(file_path)}")

    def pause_audio(self):
        """Tạm dừng phát"""
        self.player.pause()

    def stop_audio(self):
        """Dừng phát"""
        self.player.stop()

    def on_volume_change(self, value):
        """Callback khi thay đổi âm lượng"""
        volume = float(value) / 100.0
        self.player.set_volume(volume)
        self.volume_label.config(text=f"{int(float(value))}%")

    def add_schedule(self):
        """Thêm lịch mới"""
        name = self.schedule_name_entry.get()
        audio_file = self.schedule_file_entry.get()
        hour = self.hour_spinbox.get()
        minute = self.minute_spinbox.get()
        repeat = self.repeat_var.get()

        if not name or not audio_file:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not os.path.exists(audio_file):
            messagebox.showerror("Lỗi", "File âm thanh không tồn tại!")
            return

        schedule_time = f"{int(hour):02d}:{int(minute):02d}"

        self.scheduler.add_schedule(name, audio_file, schedule_time, True, repeat)
        messagebox.showinfo("Thành công", f"Đã thêm lịch: {name} lúc {schedule_time}")

        # Xóa form
        self.schedule_name_entry.delete(0, tk.END)
        self.schedule_file_entry.delete(0, tk.END)

        # Làm mới danh sách
        self.refresh_schedule_list()

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
                os.path.basename(schedule.audio_file),
                "Có" if schedule.repeat_daily else "Không",
                "Bật" if schedule.enabled else "Tắt"
            ))

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
                messagebox.showinfo("Thành công", f"Đã {status_text} lịch!")
                break

    def auto_play_callback(self, audio_file, schedule_name):
        """Callback khi scheduler tự động phát"""
        self.player.play(audio_file)
        # Hiển thị thông báo
        self.show_notification(f"Đang phát theo lịch: {schedule_name}")

    def show_notification(self, message):
        """Hiển thị thông báo"""
        messagebox.showinfo("Thông báo lịch", message)

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
