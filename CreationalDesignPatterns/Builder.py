# # ANTI-PATTERN: Đây là cách làm không tốt
# class Burger:
#     def __init__(self, bread, sauce=None, cheese=None, vegetables=None, meat=None, toasted=False):
#         # Rất nhiều tham số, khó đọc và dễ nhầm lẫn
#         self.bread = bread
#         self.sauce = sauce
#         # ... và cứ thế tiếp diễn

# # Việc gọi hàm này trở thành một cơn ác mộng
# my_burger = Burger("Wheat", "Chili", "Cheddar", ["Lettuce", "Tomato"], "Chicken", True)
# # Nếu tôi không muốn phô mai thì sao?
# my_burger_no_cheese = Burger("White", "Mayo", None, ["Onion"], "Beef", False) # Tham số None rất xấu


from abc import ABC, abstractmethod
from typing import Any, List

# --- 1. The Product (Sản phẩm phức tạp cần xây dựng) ---
# Đây là đối tượng cuối cùng mà chúng ta muốn tạo ra.
class Burger:
    def __init__(self):
        self.parts: List[str] = []

    def add(self, part: str):
        self.parts.append(part)

    def __str__(self):
        return f"Burger parts: {', '.join(self.parts)}"

# --- 2. The Builder Interface (Giao diện cho Builder) ---
# Định nghĩa tất cả các bước cần thiết để xây dựng sản phẩm.
class IBurgerBuilder(ABC):
    # abstract property, mọi lớp con phải cung cấp thuộc tính là product
    @property
    @abstractmethod
    def product(self) -> Burger:
        pass

        """Tại sao lại dùng dấu nháy đơn 'IBurgerBuilder'? Đây được gọi là "forward reference". 
        Tại thời điểm Python đọc dòng này, lớp IBurgerBuilder vẫn đang trong quá trình định nghĩa, 
        vì vậy nó chưa được biết đến như một kiểu dữ liệu hoàn chỉnh. Dấu nháy đơn báo cho Python 
        biết "đây là tên của một kiểu dữ liệu sẽ được biết đến sau này", tránh gây ra lỗi NameError.
        """
    @abstractmethod
    def set_bread(self, bread_type: str) -> 'IBurgerBuilder':
        pass

    @abstractmethod
    def add_sauce(self, sauce_type: str) -> 'IBurgerBuilder':
        pass

    @abstractmethod
    def add_cheese(self, cheese_type: str) -> 'IBurgerBuilder':
        pass
    
    @abstractmethod
    def add_meat(self, meat_type: str) -> 'IBurgerBuilder':
        pass

# --- 3. The Concrete Builder (Builder cụ thể) ---
# Triển khai các bước xây dựng. Nó giữ một thực thể của sản phẩm đang được lắp ráp.
class CustomBurgerBuilder(IBurgerBuilder):
    def __init__(self):
        """Khởi tạo một builder mới, bắt đầu với một sản phẩm trống."""
        self._product = Burger()

    def reset(self):
        """Tạo lại sản phẩm để bắt đầu xây dựng một chiếc burger mới."""
        self._product = Burger()

    @property
    def product(self) -> Burger:
        """Trả về sản phẩm đã hoàn thành và reset lại builder."""
        product = self._product
        self.reset()
        return product

    def set_bread(self, bread_type: str) -> 'CustomBurgerBuilder':
        self._product.add(f"Bread: {bread_type}")
        return self  # Trả về self để có thể gọi nối tiếp (method chaining, fluent interface)

    def add_sauce(self, sauce_type: str) -> 'CustomBurgerBuilder':
        self._product.add(f"Sauce: {sauce_type}")
        return self

    def add_cheese(self, cheese_type: str) -> 'CustomBurgerBuilder':
        self._product.add(f"Cheese: {cheese_type}")
        return self
    
    def add_meat(self, meat_type: str) -> 'CustomBurgerBuilder':
        self._product.add(f"Meat: {meat_type}")
        return self

# --- 4. The Director (Người điều phối - Tùy chọn) ---
# Chứa các công thức làm bánh mì phổ biến. Nó điều khiển builder.
class BurgerDirector:
    def __init__(self, builder: IBurgerBuilder):
        self._builder = builder

    def build_chicken_teriyaki(self):
        print("Director: Building a Chicken Teriyaki burger...")
        self._builder.set_bread("Honey Oat") \
                     .add_meat("Chicken Teriyaki") \
                     .add_cheese("Cheddar") \
                     .add_sauce("Sweet Onion")

    def build_veggie_delight(self):
        print("Director: Building a Veggie Delight burger...")
        self._builder.set_bread("Whole Wheat") \
                     .add_cheese("Swiss") \
                     .add_sauce("Vinaigrette")


# --- Client Code ---
if __name__ == "__main__":
    builder = CustomBurgerBuilder()

    # --- Cách 1: Client tự tay xây dựng từng bước ---
    print("Building a custom burger step-by-step:")
    builder.set_bread("Italian")
    builder.add_meat("Tuna")
    builder.add_cheese("Provolone")
    builder.add_sauce("Mayonnaise")
    # Lấy sản phẩm cuối cùng
    custom_burger = builder.product
    print(custom_burger)
    
    print("\n" + "="*40 + "\n")
    
    # --- Cách 2: Dùng kỹ thuật gọi nối tiếp (Method Chaining) ---
    print("Building another custom burger with method chaining:")
    another_custom = builder.set_bread("White") \
                            .add_meat("Beef") \
                            .add_sauce("BBQ") \
                            .add_sauce("Chili") \
                            .product
    print(another_custom)
    
    print("\n" + "="*40 + "\n")

    # --- Cách 3: Sử dụng Director để xây dựng theo công thức có sẵn ---
    director = BurgerDirector(builder)
    
    # Director xây dựng một chiếc Chicken Teriyaki
    director.build_chicken_teriyaki()
    chicken_burger = builder.product # Lấy sản phẩm từ builder
    print(chicken_burger)
    
    # Director xây dựng một chiếc Veggie Delight
    director.build_veggie_delight()
    veggie_burger = builder.product
    print(veggie_burger)