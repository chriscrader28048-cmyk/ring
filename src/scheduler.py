"""
Module quản lý lịch trình phát âm thanh
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import threading
import time as time_module


class AudioSchedule:
    """Lớp đại diện cho một lịch phát âm thanh"""

    def __init__(self, schedule_id: str, name: str, audio_file: str,
                 schedule_time: str, enabled: bool = True, repeat_daily: bool = False,
                 days_of_week: List[int] = None):
        """
        Khởi tạo lịch phát

        Args:
            schedule_id: ID của lịch
            name: Tên mô tả lịch
            audio_file: Đường dẫn file âm thanh
            schedule_time: Thời gian phát (định dạng HH:MM)
            enabled: Có kích hoạt hay không
            repeat_daily: Có lặp lại hàng ngày không
            days_of_week: Danh sách các ngày trong tuần (0=T2, 1=T3, ..., 6=CN)
        """
        self.schedule_id = schedule_id
        self.name = name
        self.audio_file = audio_file
        self.schedule_time = schedule_time
        self.enabled = enabled
        self.repeat_daily = repeat_daily
        # Mặc định tất cả các ngày nếu không chỉ định
        self.days_of_week = days_of_week if days_of_week is not None else [0, 1, 2, 3, 4, 5, 6]

    def to_dict(self) -> Dict:
        """Chuyển đổi sang dictionary"""
        return {
            'schedule_id': self.schedule_id,
            'name': self.name,
            'audio_file': self.audio_file,
            'schedule_time': self.schedule_time,
            'enabled': self.enabled,
            'repeat_daily': self.repeat_daily,
            'days_of_week': self.days_of_week
        }

    @staticmethod
    def from_dict(data: Dict) -> 'AudioSchedule':
        """Tạo AudioSchedule từ dictionary"""
        return AudioSchedule(
            schedule_id=data['schedule_id'],
            name=data['name'],
            audio_file=data['audio_file'],
            schedule_time=data['schedule_time'],
            enabled=data.get('enabled', True),
            repeat_daily=data.get('repeat_daily', False),
            days_of_week=data.get('days_of_week', [0, 1, 2, 3, 4, 5, 6])
        )

    def get_days_display(self) -> str:
        """Lấy chuỗi hiển thị các ngày"""
        day_names = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        if len(self.days_of_week) == 7:
            return 'Hàng ngày'
        return ', '.join([day_names[d] for d in sorted(self.days_of_week)])


class ScheduleManager:
    """Lớp quản lý các lịch phát âm thanh"""

    def __init__(self, schedule_file: str = 'schedules/schedules.json'):
        """
        Khởi tạo quản lý lịch

        Args:
            schedule_file: Đường dẫn file lưu lịch trình
        """
        self.schedule_file = schedule_file
        self.schedules: List[AudioSchedule] = []
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.callback = None
        self.load_schedules()

    def load_schedules(self):
        """Tải danh sách lịch từ file"""
        if os.path.exists(self.schedule_file):
            try:
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.schedules = [AudioSchedule.from_dict(s) for s in data]
                print(f"Đã tải {len(self.schedules)} lịch trình")
            except Exception as e:
                print(f"Lỗi khi tải lịch trình: {e}")
                self.schedules = []
        else:
            print("Chưa có file lịch trình, tạo mới")
            self.schedules = []

    def save_schedules(self):
        """Lưu danh sách lịch vào file"""
        try:
            os.makedirs(os.path.dirname(self.schedule_file), exist_ok=True)
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                data = [s.to_dict() for s in self.schedules]
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Đã lưu {len(self.schedules)} lịch trình")
        except Exception as e:
            print(f"Lỗi khi lưu lịch trình: {e}")

    def add_schedule(self, name: str, audio_file: str, schedule_time: str,
                     enabled: bool = True, repeat_daily: bool = False,
                     days_of_week: List[int] = None) -> AudioSchedule:
        """
        Thêm lịch mới

        Args:
            name: Tên lịch
            audio_file: File âm thanh
            schedule_time: Thời gian (HH:MM)
            enabled: Kích hoạt
            repeat_daily: Lặp hàng ngày
            days_of_week: Các ngày trong tuần

        Returns:
            AudioSchedule đã tạo
        """
        schedule_id = f"schedule_{len(self.schedules) + 1}_{int(time_module.time())}"
        schedule = AudioSchedule(schedule_id, name, audio_file, schedule_time,
                                 enabled, repeat_daily, days_of_week)
        self.schedules.append(schedule)
        self.save_schedules()
        print(f"Đã thêm lịch: {name} - {schedule_time}")
        return schedule

    def remove_schedule(self, schedule_id: str) -> bool:
        """
        Xóa lịch

        Args:
            schedule_id: ID của lịch cần xóa

        Returns:
            True nếu xóa thành công
        """
        for i, schedule in enumerate(self.schedules):
            if schedule.schedule_id == schedule_id:
                del self.schedules[i]
                self.save_schedules()
                print(f"Đã xóa lịch: {schedule_id}")
                return True
        return False

    def update_schedule(self, schedule_id: str, **kwargs) -> bool:
        """
        Cập nhật lịch

        Args:
            schedule_id: ID của lịch
            **kwargs: Các thuộc tính cần cập nhật

        Returns:
            True nếu cập nhật thành công
        """
        for schedule in self.schedules:
            if schedule.schedule_id == schedule_id:
                for key, value in kwargs.items():
                    if hasattr(schedule, key):
                        setattr(schedule, key, value)
                self.save_schedules()
                print(f"Đã cập nhật lịch: {schedule_id}")
                return True
        return False

    def get_schedules(self) -> List[AudioSchedule]:
        """Lấy danh sách tất cả lịch"""
        return self.schedules

    def set_playback_callback(self, callback):
        """
        Đặt callback khi đến giờ phát

        Args:
            callback: Hàm callback nhận (audio_file, schedule_name)
        """
        self.callback = callback

    def _check_schedules(self):
        """Kiểm tra và thực thi lịch (chạy trong thread)"""
        last_minute = None

        while self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            # Chuyển đổi weekday: Python dùng 0=Monday, ta dùng 0=T2
            current_day = now.weekday()  # 0=Monday=T2

            # Chỉ kiểm tra mỗi phút một lần
            if current_time != last_minute:
                last_minute = current_time

                for schedule in self.schedules:
                    if (schedule.enabled and
                        schedule.schedule_time == current_time and
                        current_day in schedule.days_of_week):
                        print(f"\n⏰ Đến giờ phát: {schedule.name} ({current_time})")
                        if self.callback:
                            self.callback(schedule.audio_file, schedule.name)

            time_module.sleep(1)  # Kiểm tra mỗi giây

    def start(self):
        """Bắt đầu theo dõi lịch"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._check_schedules, daemon=True)
            self.thread.start()
            print("Đã bắt đầu theo dõi lịch trình")

    def stop(self):
        """Dừng theo dõi lịch"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("Đã dừng theo dõi lịch trình")
