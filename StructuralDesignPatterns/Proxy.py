"""
IDoor (Subject): Giao diện chung đảm bảo SecurityProxy có thể thay thế cho RealDoor một cách minh bạch.
RealDoor (Real Subject): Chỉ làm một việc đơn giản là mở và đóng. Nó không quan tâm đến bảo mật.
SecurityProxy (Proxy): "Người gác cổng". Nó có cùng các phương thức open và close, nhưng bên trong phương thức open, nó thêm một lớp kiểm tra an ninh. Nó chỉ gọi _real_door.open() nếu điều kiện xác thực được thỏa mãn.
Client: Client không cần biết về RealDoor. Nó chỉ cần biết về SecurityProxy và cách tương tác với nó. Sự phức tạp của việc xác thực đã được che giấu khỏi client.
"""

from abc import ABC, abstractmethod

# --- 1. The Subject Interface (Giao diện chung) ---
# Cả cửa thật và proxy bảo vệ đều phải tuân thủ giao diện này.
class IDoor(ABC):
    @abstractmethod
    def open(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

# --- 2. The Real Subject (Đối tượng thật) ---
# Đây là đối tượng thực hiện công việc cốt lõi.
class RealDoor(IDoor):
    def open(self):
        print("Cửa thật đã mở.")

    def close(self):
        print("Cửa thật đã đóng.")

# --- 3. The Proxy (Người đại diện/ủy quyền) ---
# Lớp này có cùng giao diện với RealDoor và chứa một tham chiếu đến nó.
# Nó sẽ thêm vào logic bảo vệ.
class SecurityProxy(IDoor):
    def __init__(self, door: RealDoor):
        self._real_door = door
        self._password = "SECRET_PASSWORD"

    def _authenticate(self, password: str) -> bool:
        """Kiểm tra mật khẩu trước khi cho phép hành động."""
        return password == self._password

    def open(self, password: str):
        """
        Client gọi phương thức open này, nhưng nó bị chặn lại bởi logic xác thực.
        """
        if self._authenticate(password):
            print("Proxy: Mật khẩu chính xác. Cho phép mở cửa.")
            # Chỉ khi xác thực thành công, nó mới ủy quyền cho cửa thật.
            self._real_door.open()
        else:
            print("Proxy: Sai mật khẩu! Truy cập bị từ chối.")

    def close(self):
        # Việc đóng cửa có thể không cần bảo vệ, nên chỉ cần ủy quyền trực tiếp.
        print("Proxy: Yêu cầu đóng cửa được thực hiện.")
        self._real_door.close()


# --- 4. The Client Code ---
if __name__ == "__main__":
    # Tạo đối tượng thật
    real_door = RealDoor()
    
    # Tạo proxy và "bọc" đối tượng thật vào trong
    security_door = SecurityProxy(real_door)

    # Client tương tác với proxy, không phải với cửa thật.
    
    print("--- Thử mở cửa với mật khẩu sai ---")
    # Lưu ý: Client gọi open() trên proxy.
    security_door.open("WRONG_PASSWORD") # Lời gọi đến cửa thật sẽ bị chặn.

    print("\n--- Thử mở cửa với mật khẩu đúng ---")
    security_door.open("SECRET_PASSWORD") # Lời gọi sẽ được ủy quyền cho cửa thật.
    
    print("\n--- Đóng cửa ---")
    security_door.close()