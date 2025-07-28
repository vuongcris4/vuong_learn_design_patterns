# --- 1. The Complex Subsystem (Hệ thống con phức tạp) ---
# Đây là các lớp riêng lẻ mà client không muốn tương tác trực tiếp.
class Amplifier:
    def on(self): print("Âm ly đã bật")
    def off(self): print("Âm ly đã tắt")
    def set_dvd(self): print("Âm ly đã chuyển sang chế độ DVD")
    def set_volume(self, level: int): print(f"Âm ly đã đặt âm lượng ở mức {level}")

class DvdPlayer:
    def on(self): print("Đầu DVD đã bật")
    def off(self): print("Đầu DVD đã tắt")
    def play(self, movie: str): print(f"Đầu DVD đang phát phim '{movie}'")
    def stop(self): print("Đầu DVD đã dừng phát")

class Projector:
    def on(self): print("Máy chiếu đã bật")
    def off(self): print("Máy chiếu đã tắt")
    def wide_screen_mode(self): print("Máy chiếu đã chuyển sang chế độ màn ảnh rộng")

# --- 2. The Facade (Lớp "bộ mặt") ---
# Lớp này cung cấp một giao diện đơn giản để điều khiển toàn bộ hệ thống con.
class HomeTheaterFacade:
    def __init__(self, amp: Amplifier, dvd: DvdPlayer, projector: Projector):
        # Facade chứa các tham chiếu đến các thành phần của hệ thống con.
        self._amplifier = amp
        self._dvd_player = dvd
        self._projector = projector

    def watch_movie(self, movie: str):
        """Phương thức đơn giản cho một hành động phức tạp."""
        print("Chuẩn bị xem phim...")
        self._projector.on()
        self._projector.wide_screen_mode()
        self._amplifier.on()
        self._amplifier.set_dvd()
        self._amplifier.set_volume(5)
        self._dvd_player.on()
        self._dvd_player.play(movie)

    def end_movie(self):
        """Một phương thức đơn giản khác."""
        print("\nKết thúc xem phim, tắt các thiết bị...")
        self._dvd_player.stop()
        self._dvd_player.off()
        self._amplifier.off()
        self._projector.off()

# --- 3. The Client Code (Người dùng) ---
# Client chỉ cần biết đến Facade.
if __name__ == "__main__":
    # Khởi tạo các thành phần của hệ thống con
    amp = Amplifier()
    dvd = DvdPlayer()
    projector = Projector()

    # Khởi tạo Facade, "tiêm" các thành phần vào
    home_theater = HomeTheaterFacade(amp, dvd, projector)
    
    # Client chỉ cần gọi một phương thức duy nhất để thực hiện một chuỗi hành động phức tạp
    home_theater.watch_movie("Inception")
    
    # Và một phương thức duy nhất khác để kết thúc
    home_theater.end_movie()