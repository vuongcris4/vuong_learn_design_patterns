from abc import ABC, abstractmethod

# --- 1. The Abstract Class (Lớp cha trừu tượng) ---
# Lớp này chứa "khuôn mẫu" (template method).
class HouseBuilder(ABC):

    # Đây là TEMPLATE METHOD.
    # Nó định nghĩa một bộ khung các bước không thể thay đổi.
    # Nó là một phương thức cụ thể, không phải trừu tượng.
    def build_house(self):
        """Đây là thuật toán khung, với một chuỗi các bước cố định."""
        self.prepare_base()
        self.build_walls()
        self.add_roof()
        self.add_windows() # Đây là một "hook"
        print("=> Ngôi nhà đã được xây xong!")

    # --- Các bước trừu tượng mà lớp con BẮT BUỘC phải triển khai ---
    @abstractmethod
    def prepare_base(self):
        pass

    @abstractmethod
    def build_walls(self):
        pass

    @abstractmethod
    def add_roof(self):
        pass
        
    # --- Một "Hook" - một bước tùy chọn ---
    # Đây là một phương thức cụ thể nhưng trống. Lớp con CÓ THỂ ghi đè nó nếu muốn.
    def add_windows(self):
        print("   (Không có yêu cầu đặc biệt về cửa sổ)")
        pass

# --- 2. Concrete Classes (Các lớp con cụ thể) ---
# Mỗi lớp này sẽ cung cấp cách triển khai riêng cho các bước.

class WoodenHouseBuilder(HouseBuilder):
    def prepare_base(self):
        print("   - Đang chuẩn bị nền móng bằng gỗ và cọc.")

    def build_walls(self):
        print("   - Đang xây tường bằng gỗ.")

    def add_roof(self):
        print("   - Đang lợp mái ngói.")
    
    # Ghi đè "hook" để có hành vi riêng
    def add_windows(self):
        print("   - Đang lắp cửa sổ khung gỗ.")

class BrickHouseBuilder(HouseBuilder):
    def prepare_base(self):
        print("   - Đang chuẩn bị nền móng bằng bê tông cốt thép.")

    def build_walls(self):
        print("   - Đang xây tường bằng gạch đỏ.")

    def add_roof(self):
        print("   - Đang đổ mái bằng và chống thấm.")
    
    # Lớp này không ghi đè hook, nên phiên bản mặc định của cha sẽ được dùng.

# --- 3. The Client Code ---
if __name__ == "__main__":
    print("--- Bắt đầu xây nhà GỖ ---")
    wooden_house_builder = WoodenHouseBuilder()
    # Client chỉ cần gọi một phương thức duy nhất là build_house().
    wooden_house_builder.build_house()

    print("\n" + "="*30 + "\n")

    print("--- Bắt đầu xây nhà GẠCH ---")
    brick_house_builder = BrickHouseBuilder()
    # Client cũng gọi cùng một phương thức...
    brick_house_builder.build_house()
    # ... nhưng kết quả lại khác vì các bước bên trong đã được triển khai khác đi.