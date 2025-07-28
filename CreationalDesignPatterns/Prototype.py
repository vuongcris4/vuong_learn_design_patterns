import copy
import time

# --- 1. The Concrete Prototype (Lớp mẫu cụ thể) ---
# Lớp này sẽ chứa logic tạo đối tượng "đắt đỏ" và phương thức clone().
class GameObject:
    def __init__(self, name: str, properties: list):
        # Giả lập một quá trình khởi tạo tốn thời gian (ví dụ: tải file)
        print(f"Đang tải các tài nguyên đắt đỏ cho '{name}'...")
        time.sleep(3)  # Dừng 3 giây để giả lập
        
        self.name = name
        self.properties = properties
        print(f"Đã tạo xong '{name}'.")

    def clone(self):
        """
        Phương thức nhân bản. Sử dụng deepcopy để tạo một bản sao độc lập.
        """
        print(f"Đang nhân bản (cloning) '{self.name}'...")
        return copy.deepcopy(self)

    def __str__(self):
        # Hiển thị cả id của object để chứng minh chúng là các đối tượng khác nhau
        return f"GameObject [Name: {self.name}, Properties: {self.properties}, ID: {id(self)}]"

# --- 2. The Prototype Registry (Bộ đăng ký các mẫu - Tùy chọn nhưng rất hữu ích) ---
# Một nơi để lưu trữ các đối tượng mẫu đã được tạo sẵn.
class PrototypeRegistry:
    def __init__(self):
        self._prototypes = {}

    def add_prototype(self, name: str, prototype: GameObject):
        self._prototypes[name] = prototype
        print(f"Đã thêm mẫu '{name}' vào bộ đăng ký.")

    def get_clone(self, name: str) -> GameObject:
        prototype = self._prototypes.get(name)
        if not prototype:
            raise ValueError(f"Mẫu với tên '{name}' không tồn tại!")
        return prototype.clone()

# --- 3. Client Code ---
if __name__ == "__main__":
    
    print("--- CÁCH 1: TẠO TỪ ĐẦU (TỐN KÉM) ---")
    start_time = time.time()
    player1_from_scratch = GameObject("Player", ["Health: 100", "Mana: 50"])
    player2_from_scratch = GameObject("Player", ["Health: 100", "Mana: 50"])
    end_time = time.time()
    print(f"==> Thời gian tạo từ đầu: {end_time - start_time:.2f} giây.\n")
    
    print("\n" + "="*50 + "\n")

    print("--- CÁCH 2: SỬ DỤNG PROTOTYPE PATTERN (NHANH CHÓNG) ---")
    registry = PrototypeRegistry()
    
    # Bước 1: Chỉ tạo đối tượng mẫu MỘT LẦN DUY NHẤT (tốn 3 giây)
    start_time = time.time()
    player_prototype = GameObject("Player", ["Health: 100", "Mana: 50"])
    registry.add_prototype("player", player_prototype)
    end_time_prototype = time.time()
    print(f"Thời gian tạo mẫu gốc: {end_time_prototype - start_time:.2f} giây.\n")
    
    # Bước 2: Nhân bản các đối tượng mới từ mẫu (gần như tức thì)
    start_time_cloning = time.time()
    player_clone_1 = registry.get_clone("player")
    player_clone_2 = registry.get_clone("player")
    end_time_cloning = time.time()
    print(f"==> Thời gian để nhân bản 2 đối tượng: {end_time_cloning - start_time_cloning:.4f} giây.\n")
    
    # Bước 3: Chứng minh các bản sao là độc lập
    print("--- KIỂM TRA TÍNH ĐỘC LẬP ---")
    # Thay đổi một bản sao
    player_clone_1.properties.append("Effect: Shielded")
    
    print(f"Mẫu gốc      : {player_prototype}")
    print(f"Bản sao 1 (đã sửa): {player_clone_1}")
    print(f"Bản sao 2     : {player_clone_2}")
    
    # Kết quả sẽ cho thấy:
    # 1. ID của 3 đối tượng là khác nhau.
    # 2. Chỉ có `properties` của Bản sao 1 bị thay đổi.