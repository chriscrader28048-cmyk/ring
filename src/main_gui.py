"""
Giao diện GUI hiện đại cho phần mềm quản lý phát âm thanh theo lịch
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
from datetime import datetime

# Thêm thư mục src vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio_player import AudioPlayer
from scheduler import ScheduleManager


class ModernStyle:
    """Định nghĩa màu sắc và style hiện đại"""
    # Màu chính
    PRIMARY = '#2196F3'
    PRIMARY_DARK = '#1976D2'
    PRIMARY_LIGHT = '#BBDEFB'

    # Màu phụ
    ACCENT = '#FF4081'
    SUCCESS = '#4CAF50'
    WARNING = '#FF9800'
    DANGER = '#F44336'

    # Màu nền
    BG_MAIN = '#F5F5F5'
    BG_CARD = '#FFFFFF'
    BG_HEADER = '#1976D2'

    # Màu chữ
    TEXT_PRIMARY = '#212121'
    TEXT_SECONDARY = '#757575'
    TEXT_WHITE = '#FFFFFF'

    # Border
    BORDER = '#E0E0E0'


class AudioSchedulerGUI:
    """Giao diện chính của ứng dụng"""

    def __init__(self, root):
        self.root = root
        self.root.title("Hệ thống hẹn giờ phát âm thanh của LG Chem")
        self.root.geometry("1100x750")
        self.root.minsize(1000, 700)

        # Màu nền chính
        self.root.configure(bg=ModernStyle.BG_MAIN)

        # Maximize cửa sổ khi khởi động
        try:
            self.root.state('zoomed')
        except:
            pass

        # Cấu hình style
        self.setup_modern_style()

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

    def setup_modern_style(self):
        """Cấu hình style hiện đại"""
        style = ttk.Style()

        # Thử sử dụng theme tốt nhất có sẵn
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')

        # === FRAME STYLES ===
        style.configure('Card.TFrame', background=ModernStyle.BG_CARD)
        style.configure('Main.TFrame', background=ModernStyle.BG_MAIN)

        # === LABEL STYLES ===
        style.configure('Title.TLabel',
                       font=('Segoe UI', 18, 'bold'),
                       background=ModernStyle.BG_HEADER,
                       foreground=ModernStyle.TEXT_WHITE)

        style.configure('Header.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.TEXT_PRIMARY)

        style.configure('Clock.TLabel',
                       font=('Segoe UI', 36, 'bold'),
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.PRIMARY)

        style.configure('Date.TLabel',
                       font=('Segoe UI', 13),
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.TEXT_SECONDARY)

        style.configure('Status.TLabel',
                       font=('Segoe UI', 10),
                       background=ModernStyle.BG_MAIN,
                       foreground=ModernStyle.TEXT_SECONDARY)

        style.configure('Card.TLabel',
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.TEXT_PRIMARY)

        # === BUTTON STYLES ===
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(15, 8))

        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=(20, 10))

        style.configure('Danger.TButton',
                       font=('Segoe UI', 10),
                       padding=(15, 8))

        style.configure('Control.TButton',
                       font=('Segoe UI', 10),
                       padding=(12, 6))

        style.configure('Quick.TButton',
                       font=('Segoe UI', 9),
                       padding=(8, 4))

        # === LABELFRAME STYLES ===
        style.configure('Card.TLabelframe',
                       background=ModernStyle.BG_CARD)
        style.configure('Card.TLabelframe.Label',
                       font=('Segoe UI', 11, 'bold'),
                       background=ModernStyle.BG_CARD,
                       foreground=ModernStyle.PRIMARY)

        # === ENTRY STYLES ===
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 10),
                       padding=8)

        # === CHECKBUTTON STYLES ===
        style.configure('Day.TCheckbutton',
                       font=('Segoe UI', 10),
                       background=ModernStyle.BG_CARD)

        # === TREEVIEW STYLES ===
        style.configure('Treeview',
                       font=('Segoe UI', 10),
                       rowheight=30,
                       background=ModernStyle.BG_CARD,
                       fieldbackground=ModernStyle.BG_CARD)
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=ModernStyle.PRIMARY_LIGHT,
                       foreground=ModernStyle.TEXT_PRIMARY)
        style.map('Treeview',
                 background=[('selected', ModernStyle.PRIMARY_LIGHT)],
                 foreground=[('selected', ModernStyle.TEXT_PRIMARY)])

        # === SCALE STYLES ===
        style.configure('TScale',
                       background=ModernStyle.BG_CARD)

        # === SPINBOX STYLES ===
        style.configure('TSpinbox',
                       font=('Segoe UI', 12))

    def create_widgets(self):
        """Tạo các widget cho giao diện"""

        # Container chính
        container = ttk.Frame(self.root, style='Main.TFrame')
        container.pack(fill=tk.BOTH, expand=True)

        # === HEADER ===
        header_frame = tk.Frame(container, bg=ModernStyle.BG_HEADER, height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        header_content = tk.Frame(header_frame, bg=ModernStyle.BG_HEADER)
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Title và subtitle
        title_frame = tk.Frame(header_content, bg=ModernStyle.BG_HEADER)
        title_frame.pack(side=tk.LEFT)

        title_label = tk.Label(title_frame,
                              text="HỆ THỐNG HẸN GIỜ PHÁT ÂM THANH CỦA LG CHEM",
                              font=('Segoe UI', 14, 'bold'),
                              bg=ModernStyle.BG_HEADER,
                              fg=ModernStyle.TEXT_WHITE)
        title_label.pack(anchor=tk.W)

        subtitle_label = tk.Label(title_frame,
                                 text="Made by Kitts",
                                 font=('Segoe UI', 9, 'italic'),
                                 bg=ModernStyle.BG_HEADER,
                                 fg='#BBDEFB')
        subtitle_label.pack(anchor=tk.W)

        # === MAIN CONTENT ===
        main_frame = ttk.Frame(container, style='Main.TFrame', padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid configuration
        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # === LEFT PANEL ===
        left_panel = ttk.Frame(main_frame, style='Main.TFrame')
        left_panel.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(0, 10))
        left_panel.rowconfigure(1, weight=1)

        # Card: Phát Thủ Công
        manual_card = ttk.LabelFrame(left_panel, text="  Phát Thủ Công  ",
                                    style='Card.TLabelframe', padding=15)
        manual_card.pack(fill=tk.X, pady=(0, 15))

        # File selection
        file_frame = ttk.Frame(manual_card, style='Card.TFrame')
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(file_frame, text="File âm thanh:",
                 style='Header.TLabel').pack(anchor=tk.W)

        file_input_frame = ttk.Frame(file_frame, style='Card.TFrame')
        file_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.file_entry = ttk.Entry(file_input_frame, font=('Segoe UI', 10))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Button(file_input_frame, text="Chọn File",
                  command=self.browse_file,
                  style='Primary.TButton').pack(side=tk.RIGHT)

        # Control buttons
        control_frame = ttk.Frame(manual_card, style='Card.TFrame')
        control_frame.pack(fill=tk.X, pady=10)

        btn_frame = ttk.Frame(control_frame, style='Card.TFrame')
        btn_frame.pack(side=tk.LEFT)

        ttk.Button(btn_frame, text="▶ Phát", command=self.play_audio,
                  style='Control.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="⏸ Tạm dừng", command=self.pause_audio,
                  style='Control.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⏹ Dừng", command=self.stop_audio,
                  style='Control.TButton').pack(side=tk.LEFT, padx=5)

        # Volume
        volume_frame = ttk.Frame(control_frame, style='Card.TFrame')
        volume_frame.pack(side=tk.RIGHT)

        ttk.Label(volume_frame, text="🔊", style='Card.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.volume_label = ttk.Label(volume_frame, text="100%",
                                     style='Card.TLabel', width=5)
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100,
                                     orient=tk.HORIZONTAL,
                                     command=self.on_volume_change, length=120)
        self.volume_scale.set(100)
        self.volume_scale.pack(side=tk.LEFT)
        self.volume_label.pack(side=tk.LEFT, padx=(5, 0))

        # Card: Thêm Lịch Mới
        schedule_card = ttk.LabelFrame(left_panel, text="  Thêm Lịch Mới  ",
                                      style='Card.TLabelframe', padding=15)
        schedule_card.pack(fill=tk.X, pady=(0, 15))

        # Tên lịch
        name_frame = ttk.Frame(schedule_card, style='Card.TFrame')
        name_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(name_frame, text="Tên lịch:", style='Header.TLabel').pack(anchor=tk.W)
        self.schedule_name_entry = ttk.Entry(name_frame, font=('Segoe UI', 10))
        self.schedule_name_entry.pack(fill=tk.X, pady=(5, 0))

        # File âm thanh
        sfile_frame = ttk.Frame(schedule_card, style='Card.TFrame')
        sfile_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(sfile_frame, text="File âm thanh:", style='Header.TLabel').pack(anchor=tk.W)

        sfile_input = ttk.Frame(sfile_frame, style='Card.TFrame')
        sfile_input.pack(fill=tk.X, pady=(5, 0))
        self.schedule_file_entry = ttk.Entry(sfile_input, font=('Segoe UI', 10))
        self.schedule_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(sfile_input, text="Chọn", command=self.browse_schedule_file,
                  style='Control.TButton').pack(side=tk.RIGHT)

        # Thời gian
        time_frame = ttk.Frame(schedule_card, style='Card.TFrame')
        time_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(time_frame, text="Thời gian:", style='Header.TLabel').pack(anchor=tk.W)

        time_input = ttk.Frame(time_frame, style='Card.TFrame')
        time_input.pack(anchor=tk.W, pady=(5, 0))

        self.hour_spinbox = ttk.Spinbox(time_input, from_=0, to=23, width=4,
                                       format="%02.0f", font=('Segoe UI', 14))
        self.hour_spinbox.set("08")
        self.hour_spinbox.pack(side=tk.LEFT)

        tk.Label(time_input, text=" : ", font=('Segoe UI', 14, 'bold'),
                bg=ModernStyle.BG_CARD).pack(side=tk.LEFT)

        self.minute_spinbox = ttk.Spinbox(time_input, from_=0, to=59, width=4,
                                         format="%02.0f", font=('Segoe UI', 14))
        self.minute_spinbox.set("00")
        self.minute_spinbox.pack(side=tk.LEFT)

        # Chọn ngày
        days_frame = ttk.Frame(schedule_card, style='Card.TFrame')
        days_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(days_frame, text="Các ngày phát:", style='Header.TLabel').pack(anchor=tk.W)

        days_check = ttk.Frame(days_frame, style='Card.TFrame')
        days_check.pack(anchor=tk.W, pady=(5, 0))

        day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        self.day_vars = []

        for i, day in enumerate(day_names):
            var = tk.BooleanVar(value=True)
            self.day_vars.append(var)
            cb = ttk.Checkbutton(days_check, text=day, variable=var,
                                style='Day.TCheckbutton')
            cb.pack(side=tk.LEFT, padx=(0, 10))

        # Quick select buttons
        quick_frame = ttk.Frame(schedule_card, style='Card.TFrame')
        quick_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Button(quick_frame, text="Tất cả", command=self.select_all_days,
                  style='Quick.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="Ngày thường", command=self.select_weekdays,
                  style='Quick.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Cuối tuần", command=self.select_weekend,
                  style='Quick.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(quick_frame, text="Bỏ chọn", command=self.deselect_all_days,
                  style='Quick.TButton').pack(side=tk.LEFT, padx=5)

        # Add button
        ttk.Button(schedule_card, text="➕ THÊM LỊCH", command=self.add_schedule,
                  style='Success.TButton').pack(pady=(5, 0))

        # Card: Danh sách lịch
        list_card = ttk.LabelFrame(left_panel, text="  Danh Sách Lịch Trình  ",
                                  style='Card.TLabelframe', padding=15)
        list_card.pack(fill=tk.BOTH, expand=True)

        # Treeview
        columns = ('Tên', 'Thời gian', 'Các ngày', 'File', 'Trạng thái')
        self.schedule_tree = ttk.Treeview(list_card, columns=columns,
                                         show='headings', height=8)

        # Column config
        self.schedule_tree.column('Tên', width=120, minwidth=80)
        self.schedule_tree.column('Thời gian', width=70, minwidth=50)
        self.schedule_tree.column('Các ngày', width=120, minwidth=80)
        self.schedule_tree.column('File', width=150, minwidth=100)
        self.schedule_tree.column('Trạng thái', width=70, minwidth=50)

        for col in columns:
            self.schedule_tree.heading(col, text=col)

        # Scrollbars
        scroll_y = ttk.Scrollbar(list_card, orient=tk.VERTICAL,
                                command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscroll=scroll_y.set)

        self.schedule_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        # List buttons
        list_btn_frame = ttk.Frame(left_panel, style='Main.TFrame')
        list_btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(list_btn_frame, text="🔄 Làm mới",
                  command=self.refresh_schedule_list,
                  style='Control.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(list_btn_frame, text="🗑️ Xóa", command=self.delete_schedule,
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(list_btn_frame, text="⏯️ Bật/Tắt", command=self.toggle_schedule,
                  style='Control.TButton').pack(side=tk.LEFT, padx=5)

        # === RIGHT PANEL - Clock ===
        right_panel = ttk.Frame(main_frame, style='Main.TFrame')
        right_panel.grid(row=0, column=1, sticky='new')

        # Clock card
        clock_card = ttk.LabelFrame(right_panel, text="  Thời Gian  ",
                                   style='Card.TLabelframe', padding=20)
        clock_card.pack(fill=tk.X)

        self.clock_label = ttk.Label(clock_card, text="00:00:00", style='Clock.TLabel')
        self.clock_label.pack(pady=(10, 5))

        self.date_label = ttk.Label(clock_card, text="", style='Date.TLabel')
        self.date_label.pack(pady=(0, 10))

        # Button sync time
        ttk.Button(clock_card, text="🔄 Đồng bộ thời gian",
                  command=self.sync_system_time,
                  style='Control.TButton').pack(pady=(5, 0))

        # === STATUS BAR ===
        status_frame = tk.Frame(container, bg=ModernStyle.BG_MAIN, height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(status_frame,
                                    text="● Sẵn sàng - Ứng dụng đang chạy và theo dõi lịch trình",
                                    font=('Segoe UI', 9),
                                    bg=ModernStyle.BG_MAIN,
                                    fg=ModernStyle.SUCCESS)
        self.status_label.pack(side=tk.LEFT, padx=20, pady=5)

    def update_clock(self):
        """Cập nhật đồng hồ và ngày tháng"""
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        self.clock_label.config(text=time_str)

        day_names = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']
        day_name = day_names[now.weekday()]
        date_str = f"{day_name}, {now.day:02d}/{now.month:02d}/{now.year}"
        self.date_label.config(text=date_str)

        self.root.after(1000, self.update_clock)

    def sync_system_time(self):
        """Đồng bộ thời gian hệ thống từ Windows Time Service"""
        try:
            # Chạy lệnh đồng bộ thời gian Windows
            result = subprocess.run(
                ['w32tm', '/resync', '/nowait'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            if result.returncode == 0:
                self.status_label.config(
                    text="● Đã gửi yêu cầu đồng bộ thời gian",
                    fg=ModernStyle.SUCCESS
                )
                messagebox.showinfo(
                    "Đồng bộ thời gian",
                    "Đã gửi yêu cầu đồng bộ thời gian với máy chủ Windows.\n\n"
                    "Lưu ý: Cần chạy với quyền Administrator để đồng bộ thành công."
                )
            else:
                # Thử cách khác nếu không có quyền admin
                self.status_label.config(
                    text="● Cần quyền Administrator để đồng bộ",
                    fg=ModernStyle.WARNING
                )
                messagebox.showwarning(
                    "Cần quyền Admin",
                    "Để đồng bộ thời gian, vui lòng:\n\n"
                    "1. Chạy ứng dụng với quyền Administrator\n"
                    "2. Hoặc vào Settings > Time & Language > Sync now"
                )
        except Exception as e:
            self.status_label.config(
                text=f"● Lỗi đồng bộ: {str(e)}",
                fg=ModernStyle.DANGER
            )
            messagebox.showerror("Lỗi", f"Không thể đồng bộ thời gian:\n{str(e)}")

    def select_all_days(self):
        for var in self.day_vars:
            var.set(True)

    def deselect_all_days(self):
        for var in self.day_vars:
            var.set(False)

    def select_weekdays(self):
        for i, var in enumerate(self.day_vars):
            var.set(i < 5)

    def select_weekend(self):
        for i, var in enumerate(self.day_vars):
            var.set(i >= 5)

    def browse_file(self):
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
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file âm thanh!")
            return

        if self.player.play(file_path):
            self.status_label.config(text=f"● Đang phát: {os.path.basename(file_path)}",
                                    fg=ModernStyle.PRIMARY)

    def pause_audio(self):
        self.player.pause()
        self.status_label.config(text="● Đã tạm dừng phát", fg=ModernStyle.WARNING)

    def stop_audio(self):
        self.player.stop()
        self.status_label.config(text="● Đã dừng phát", fg=ModernStyle.TEXT_SECONDARY)

    def on_volume_change(self, value):
        volume = float(value) / 100.0
        self.player.set_volume(volume)
        self.volume_label.config(text=f"{int(float(value))}%")

    def add_schedule(self):
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

        days_of_week = [i for i, var in enumerate(self.day_vars) if var.get()]

        if not days_of_week:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một ngày trong tuần!")
            return

        schedule_time = f"{int(hour):02d}:{int(minute):02d}"

        self.scheduler.add_schedule(name, audio_file, schedule_time, True, True, days_of_week)

        day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        days_str = ', '.join([day_names[d] for d in days_of_week])

        messagebox.showinfo("Thành công", f"Đã thêm lịch: {name}\nThời gian: {schedule_time}\nCác ngày: {days_str}")

        self.schedule_name_entry.delete(0, tk.END)
        self.schedule_file_entry.delete(0, tk.END)
        self.refresh_schedule_list()
        self.status_label.config(text=f"● Đã thêm lịch mới: {name}", fg=ModernStyle.SUCCESS)

    def refresh_schedule_list(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)

        for schedule in self.scheduler.get_schedules():
            self.schedule_tree.insert('', tk.END, iid=schedule.schedule_id, values=(
                schedule.name,
                schedule.schedule_time,
                schedule.get_days_display(),
                os.path.basename(schedule.audio_file),
                "✓ Bật" if schedule.enabled else "✗ Tắt"
            ))

        count = len(self.scheduler.get_schedules())
        self.status_label.config(text=f"● Đã tải {count} lịch trình", fg=ModernStyle.SUCCESS)

    def delete_schedule(self):
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
                self.status_label.config(text=f"● Đã {status_text} lịch: {schedule.name}",
                                        fg=ModernStyle.SUCCESS if new_status else ModernStyle.WARNING)
                break

    def auto_play_callback(self, audio_file, schedule_name):
        self.player.play(audio_file)
        self.status_label.config(text=f"● Đang phát theo lịch: {schedule_name}",
                                fg=ModernStyle.PRIMARY)
        self.show_notification(f"Đang phát theo lịch: {schedule_name}")

    def show_notification(self, message):
        notification = tk.Toplevel(self.root)
        notification.title("Thông báo")
        notification.geometry("400x120")
        notification.resizable(False, False)
        notification.configure(bg=ModernStyle.BG_CARD)

        screen_width = notification.winfo_screenwidth()
        screen_height = notification.winfo_screenheight()
        x = screen_width - 420
        y = screen_height - 180
        notification.geometry(f"+{x}+{y}")

        # Header
        header = tk.Frame(notification, bg=ModernStyle.PRIMARY, height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="🔔 Thông báo lịch", font=('Segoe UI', 10, 'bold'),
                bg=ModernStyle.PRIMARY, fg=ModernStyle.TEXT_WHITE).pack(pady=10)

        # Content
        tk.Label(notification, text=message, font=('Segoe UI', 11),
                bg=ModernStyle.BG_CARD, fg=ModernStyle.TEXT_PRIMARY,
                wraplength=380).pack(pady=20, padx=10)

        notification.after(5000, notification.destroy)

    def on_closing(self):
        self.scheduler.stop()
        self.player.stop()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AudioSchedulerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
