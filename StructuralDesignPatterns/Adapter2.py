from abc import ABC, abstractmethod

# --- Giao diện mục tiêu mà hệ thống cần ---
class ICanonicalShape(ABC):
    @abstractmethod
    def get_vertices(self) -> list[tuple]:
        pass

# --- Các lớp không tương thích (Adaptees) ---
class RectangleA:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class RectangleB:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

class Quad:
    def get_corners(self):
        return [(0, 0), (100, 10), (90, 110), (5, 95)]

# --- MỘT ADAPTER DUY NHẤT, LINH HOẠT ---
class UniversalShapeAdapter(ICanonicalShape):
    def __init__(self, shape_object):
        # Adapter này "bọc" một đối tượng bất kỳ.
        self._shape = shape_object

    def get_vertices(self) -> list[tuple]:
        """
        Đây là nơi phép màu xảy ra. Adapter sẽ kiểm tra xem nó đang
        bọc đối tượng nào để có cách "dịch" phù hợp.
        """
        print(f"Adapter: Đang chuyển đổi cho đối tượng kiểu '{type(self._shape).__name__}'...")
        
        # Kiểm tra xem có phải là RectangleA không?
        if isinstance(self._shape, RectangleA):
            # Logic dịch cho RectangleA
            x, y, w, h = self._shape.x, self._shape.y, self._shape.width, self._shape.height
            return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

        # Kiểm tra xem có phải là RectangleB không?
        elif isinstance(self._shape, RectangleB):
            # Logic dịch cho RectangleB
            x1, y1, x2, y2 = self._shape.x1, self._shape.y1, self._shape.x2, self._shape.y2
            return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

        # Kiểm tra xem có phải là Quad không?
        elif hasattr(self._shape, 'get_corners'):
            # Logic dịch cho Quad
            return self._shape.get_corners()
            
        else:
            raise TypeError("Loại hình học không được hỗ trợ bởi UniversalShapeAdapter")

# --- Client Code ---
def draw_shape(shape: ICanonicalShape):
    vertices = shape.get_vertices()
    print(f"Client: Đã nhận được các đỉnh: {vertices}. Đang vẽ...")

# --- Cách sử dụng ---
if __name__ == "__main__":
    # Tạo ra các đối tượng từ các thư viện khác nhau
    rect_a = RectangleA(x=10, y=20, width=100, height=50)
    rect_b = RectangleB(x1=0, y1=0, x2=200, y2=100)
    quad_c = Quad()

    # Tạo các adapter tương ứng, tất cả đều dùng chung một lớp UniversalShapeAdapter
    adapter_a = UniversalShapeAdapter(rect_a)
    adapter_b = UniversalShapeAdapter(rect_b)
    adapter_c = UniversalShapeAdapter(quad_c)

    # Hệ thống có thể làm việc với tất cả chúng một cách thống nhất
    print("--- Vẽ hình chữ nhật A ---")
    draw_shape(adapter_a)

    print("\n--- Vẽ hình chữ nhật B ---")
    draw_shape(adapter_b)

    print("\n--- Vẽ hình tứ giác C ---")
    draw_shape(adapter_c)