"""
Module quản lý phát âm thanh
"""
import pygame
import os
import threading
import time
from typing import Optional


class AudioPlayer:
    """Lớp quản lý phát âm thanh"""

    def __init__(self):
        """Khởi tạo audio player"""
        pygame.mixer.init()
        self.current_file: Optional[str] = None
        self.is_playing = False
        self.playback_thread: Optional[threading.Thread] = None
        self.stop_flag = False

    def load_audio(self, file_path: str) -> bool:
        """
        Tải file âm thanh

        Args:
            file_path: Đường dẫn đến file âm thanh

        Returns:
            True nếu tải thành công, False nếu thất bại
        """
        try:
            if not os.path.exists(file_path):
                print(f"Lỗi: File không tồn tại: {file_path}")
                return False

            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            print(f"Đã tải file: {file_path}")
            return True
        except Exception as e:
            print(f"Lỗi khi tải file: {e}")
            return False

    def play(self, file_path: Optional[str] = None, loops: int = 0) -> bool:
        """
        Phát âm thanh

        Args:
            file_path: Đường dẫn file (nếu None sẽ phát file đã tải)
            loops: Số lần lặp lại (0 = phát 1 lần, -1 = lặp vô hạn)

        Returns:
            True nếu phát thành công, False nếu thất bại
        """
        try:
            if file_path:
                if not self.load_audio(file_path):
                    return False

            if self.current_file is None:
                print("Lỗi: Chưa có file nào được tải")
                return False

            pygame.mixer.music.play(loops=loops)
            self.is_playing = True
            print(f"Đang phát: {self.current_file}")
            return True
        except Exception as e:
            print(f"Lỗi khi phát âm thanh: {e}")
            return False

    def play_with_duration(self, file_path: str, duration_seconds: int) -> bool:
        """
        Phát âm thanh với thời lượng cố định
        - Nếu file ngắn hơn duration: lặp lại cho đủ
        - Nếu file dài hơn duration: chỉ phát phần đầu

        Args:
            file_path: Đường dẫn file âm thanh
            duration_seconds: Thời lượng phát (giây)

        Returns:
            True nếu phát thành công
        """
        try:
            # Dừng phát hiện tại nếu có
            self.stop()
            self.stop_flag = False

            if not os.path.exists(file_path):
                print(f"Lỗi: File không tồn tại: {file_path}")
                return False

            # Tải và phát trong thread riêng
            def play_thread():
                try:
                    pygame.mixer.music.load(file_path)
                    self.current_file = file_path

                    # Phát với loop vô hạn
                    pygame.mixer.music.play(loops=-1)
                    self.is_playing = True
                    print(f"Đang phát: {os.path.basename(file_path)} ({duration_seconds}s)")

                    # Đợi đủ thời gian hoặc bị dừng
                    start_time = time.time()
                    while time.time() - start_time < duration_seconds:
                        if self.stop_flag:
                            break
                        time.sleep(0.1)

                    # Dừng phát
                    pygame.mixer.music.stop()
                    self.is_playing = False
                    print(f"Đã phát xong {duration_seconds} giây")

                except Exception as e:
                    print(f"Lỗi khi phát: {e}")
                    self.is_playing = False

            self.playback_thread = threading.Thread(target=play_thread, daemon=True)
            self.playback_thread.start()
            return True

        except Exception as e:
            print(f"Lỗi khi phát âm thanh: {e}")
            return False

    def stop(self):
        """Dừng phát âm thanh"""
        self.stop_flag = True
        pygame.mixer.music.stop()
        self.is_playing = False
        print("Đã dừng phát")

    def pause(self):
        """Tạm dừng phát âm thanh"""
        pygame.mixer.music.pause()
        self.is_playing = False
        print("Đã tạm dừng")

    def resume(self):
        """Tiếp tục phát âm thanh"""
        pygame.mixer.music.unpause()
        self.is_playing = True
        print("Đã tiếp tục phát")

    def set_volume(self, volume: float):
        """
        Điều chỉnh âm lượng

        Args:
            volume: Âm lượng từ 0.0 đến 1.0
        """
        volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(volume)
        print(f"Đã đặt âm lượng: {volume * 100}%")

    def get_volume(self) -> float:
        """
        Lấy âm lượng hiện tại

        Returns:
            Âm lượng từ 0.0 đến 1.0
        """
        return pygame.mixer.music.get_volume()

    def is_busy(self) -> bool:
        """
        Kiểm tra xem có đang phát không

        Returns:
            True nếu đang phát, False nếu không
        """
        return pygame.mixer.music.get_busy()
