"""
Intrinsic State: data chung, không thay đổi, và có thể được chia sẻ giữa nhiều object. (nặng)
Extrinsic State: data riêng, độc nhất, phụ thuộc vào bối cảnh từng đối tượng (nhẹ). Không được lưu trong object Flyweight, được client truyền vào khi gọi phương thức của Flyweight
"""
    
"""
Kiểu TreeFactory để quản lí kho TreeType đúng không, 
TreeType là linh hồn của Tree, Tree chỉ wrap TreeType và thêm toạ độ vô thôi
Vậy khi một trong name: str, color: str, texture: str mà thay đổi thì tạo TreeType mới đúng k
"""

import json

# --- 1. The Flyweight ---
# Đối tượng này chứa Trạng thái Nội tại (Intrinsic State) được chia sẻ.
# kiểu hình ảnh giống nhau giữa các object, tránh clone nặng.
class TreeType:
    def __init__(self, name: str, color: str, texture: str):
        """
        Lưu trữ trạng thái chung cho một loại cây.
        Đây là phần "nặng", tốn bộ nhớ.
        """
        print(f"[[ Tạo mới TreeType cho loại '{name}' - Đây là phần tốn kém! ]]")
        self._name = name
        self._color = color
        self._texture = texture

    def draw(self, x: int, y: int):
        """
        Phương thức này nhận Trạng thái Bên ngoài (Extrinsic State) để vẽ.
        """
        print(f"Đang vẽ cây loại '{self._name}' tại ({x}, {y})")

# --- 2. The Flyweight Factory ---
# Nhà máy này tạo và quản lý các đối tượng Flyweight, đảm bảo chúng được chia sẻ.
# Người quản kho
class TreeFactory:
    _tree_types: dict[str, TreeType] = {}

    @classmethod
    def get_tree_type(cls, name: str, color: str, texture: str) -> TreeType:
        """
        Trả về một Flyweight từ cache, hoặc tạo mới nếu chưa có.
        """
        key = f"{name}_{color}"
        if key not in cls._tree_types:
            print(f"Factory: Không tìm thấy loại cây '{name}', đang tạo mới...")
            cls._tree_types[key] = TreeType(name, color, texture)
        else:
            print(f"Factory: Đã có loại cây '{name}', đang tái sử dụng...")
        
        return cls._tree_types[key]

# --- 3. The Context (Bối cảnh) ---
# Lớp này chứa Trạng thái Bên ngoài (Extrinsic State) và tham chiếu đến Flyweight.
class Tree:
    def __init__(self, x: int, y: int, tree_type: TreeType):
        self._x = x
        self._y = y
        self._type = tree_type # Tham chiếu đến đối tượng Flyweight được chia sẻ

    def draw(self):
        # Ủy quyền việc vẽ cho đối tượng Flyweight,
        # truyền vào trạng thái bên ngoài của chính nó.
        self._type.draw(self._x, self._y)

# --- 4. The Client Code ---
class Forest:
    def __init__(self):
        self._trees: list[Tree] = []

    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str):
        # Client yêu cầu flyweight từ nhà máy.
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        # Client tạo đối tượng Context với trạng thái bên ngoài và flyweight.
        tree = Tree(x, y, tree_type)
        self._trees.append(tree)

    def draw(self):
        for tree in self._trees:
            tree.draw()

# --- Cách sử dụng ---
if __name__ == "__main__":
    forest = Forest()

    print("--- Trồng 5 cây sồi ---")
    # Dù chúng ta trồng 5 cây, đối tượng TreeType cho "Sồi" chỉ được tạo MỘT LẦN.
    forest.plant_tree(10, 20, "Sồi", "Xanh lá", "soi_texture.png")
    forest.plant_tree(30, 15, "Sồi", "Xanh lá", "soi_texture.png")
    forest.plant_tree(55, 40, "Sồi", "Xanh lá", "soi_texture.png")
    forest.plant_tree(80, 60, "Sồi", "Xanh lá", "soi_texture.png")
    forest.plant_tree(12, 75, "Sồi", "Xanh lá", "soi_texture.png")

    print("\n--- Trồng 3 cây thông ---")
    # TreeType cho "Thông" cũng chỉ được tạo MỘT LẦN.
    forest.plant_tree(25, 33, "Thông", "Xanh đậm", "thong_texture.png")
    forest.plant_tree(43, 88, "Thông", "Xanh đậm", "thong_texture.png")
    forest.plant_tree(91, 19, "Thông", "Xanh đậm", "thong_texture.png")
    
    print(f"\nTổng số đối tượng TreeType đã tạo: {len(TreeFactory._tree_types)}")
    print(f"Tổng số cây trong rừng: {len(forest._trees)}")
    
    print("\n--- Bắt đầu vẽ khu rừng ---")
    forest.draw()