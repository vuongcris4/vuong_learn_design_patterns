from abc import ABC, abstractmethod

# --- 1. Product Interface (Sản phẩm trừu tượng) ---
# Định nghĩa các thuộc tính chung mà mọi loại cửa đều phải có.
# Giống như việc mọi cánh cửa đều phải có chiều rộng, chiều cao.
class IDoor(ABC):
    """
    Interface cho các loại cửa.
    Trong Python, chúng ta thường dùng Abstract Base Class (ABC) để tạo interface.
    """
    @abstractmethod
    def get_description(self):
        """Mô tả về cánh cửa."""
        pass

# --- 2. Concrete Products (Sản phẩm cụ thể) ---
# Đây là các loại cửa thực tế mà nhà máy có thể sản xuất.
class WoodenDoor(IDoor):
    """Lớp cửa gỗ cụ thể."""
    def get_description(self):
        return "Tôi là một cánh cửa gỗ."

class GlassDoor(IDoor):
    """Lớp cửa kính cụ thể."""
    def get_description(self):
        return "Tôi là một cánh cửa kính."

# --- 3. The Simple Factory (Nhà máy đơn giản) ---
# Đây là nơi logic tạo đối tượng được tập trung.
# Nó nhận yêu cầu và trả về sản phẩm tương ứng.
class DoorFactory:
    """
    Nhà máy cửa đơn giản.
    Nó có một phương thức tĩnh (staticmethod) để tạo cửa mà không cần tạo
    một thực thể (instance) của nhà máy.
    """
    @staticmethod
    def make_door(door_type: str) -> IDoor:
        """
        Phương thức chính của nhà máy, tạo ra một cánh cửa dựa trên loại được yêu cầu.
        """
        if door_type == 'wooden':
            return WoodenDoor()
        elif door_type == 'glass':
            return GlassDoor()
        else:
            # Nếu yêu cầu một loại cửa mà nhà máy không sản xuất
            raise ValueError(f"Loại cửa '{door_type}' không được hỗ trợ.")

# --- 4. Client Code (Mã của người dùng/client) ---
# Đây là nơi chúng ta sử dụng nhà máy để có được sản phẩm.
if __name__ == "__main__":
    print("Bắt đầu xây nhà, tôi cần một vài cánh cửa.")
    
    # Người xây nhà (client) không cần biết cách làm cửa gỗ hay cửa kính.
    # Họ chỉ cần gọi đến nhà máy và yêu cầu.
    
    # Yêu cầu nhà máy tạo một cửa gỗ
    try:
        cua_go = DoorFactory.make_door('wooden')
        print(f"Nhận được cửa đầu tiên: {cua_go.get_description()}")

        # Yêu cầu nhà máy tạo một cửa kính
        cua_kinh = DoorFactory.make_door('glass')
        print(f"Nhận được cửa thứ hai: {cua_kinh.get_description()}")
        
        # Thử yêu cầu một loại cửa không tồn tại
        print("\nBây giờ thử yêu cầu một loại cửa sắt...")
        cua_sat = DoorFactory.make_door('steel')

    except ValueError as e:
        print(f"Lỗi từ nhà máy: {e}")