from abc import ABC, abstractmethod
from typing import List

# --- 1. The Component Interface (Giao diện chung cho mọi thành phần BOM) ---
class IBomComponent(ABC):
    """
    Bất kỳ thứ gì trong BOM, dù là linh kiện hay cụm lắp ráp,
    đều phải có khả năng cho biết chi phí của nó.
    """
    @abstractmethod
    def get_cost(self) -> float:
        """Trả về chi phí của thành phần."""
        pass

# --- 2. The Leaf (Linh kiện đơn lẻ) ---
class Part(IBomComponent):
    def __init__(self, name: str, cost: float):
        self._name = name
        self._cost = cost

    def get_cost(self) -> float:
        # Chi phí của một linh kiện đơn giản là giá của chính nó.
        print(f"  [Part] '{self._name}': cost = ${self._cost}")
        return self._cost

# --- 3. The Composite (Cụm lắp ráp) ---
class Assembly(IBomComponent):
    def __init__(self, name: str):
        self._name = name
        self._sub_components: List[IBomComponent] = []

    def add(self, component: IBomComponent) -> None:
        self._sub_components.append(component)

    def remove(self, component: IBomComponent) -> None:
        self._sub_components.remove(component)

    def get_cost(self) -> float:
        # Chi phí của một cụm lắp ráp là TỔNG chi phí của các thành phần con.
        print(f"--- Calculating cost for Assembly '{self._name}' ---")
        total_cost = 0.0
        for child in self._sub_components:
            # Gọi đệ quy get_cost() trên từng thành phần con.
            # Không cần quan tâm child là Part hay Assembly.
            total_cost += child.get_cost()
        
        print(f"--- Total cost for Assembly '{self._name}' is ${total_cost:.2f} ---")
        return total_cost

# --- Client Code: Xây dựng BOM và tính toán ---
if __name__ == "__main__":
    # --- Định nghĩa các linh kiện đơn lẻ (Leaves) ---
    saddle = Part("Saddle", 50.0)
    pedals = Part("Pedals", 20.0)
    frame = Part("Main Frame", 150.0)
    tire = Part("Tire", 15.0)
    rim = Part("Rim", 25.0)
    spokes = Part("Spokes", 10.0)

    # --- Xây dựng các cụm lắp ráp con (Composites) ---
    
    # 1. Cụm bánh xe
    wheel_assembly = Assembly("Wheel")
    wheel_assembly.add(tire)
    wheel_assembly.add(rim)
    wheel_assembly.add(spokes)
    
    # 2. Cụm khung xe
    frame_assembly = Assembly("Frame Assembly")
    frame_assembly.add(frame)
    frame_assembly.add(saddle)
    frame_assembly.add(pedals)

    # --- Xây dựng sản phẩm cuối cùng (Composite cấp cao nhất) ---
    bicycle = Assembly("Bicycle - Final Product")
    bicycle.add(frame_assembly)
    bicycle.add(wheel_assembly) # Thêm bánh xe thứ nhất
    bicycle.add(wheel_assembly) # Thêm bánh xe thứ hai (tái sử dụng cụm lắp ráp)

    print("="*40)
    print("BẮT ĐẦU TÍNH TỔNG CHI PHÍ SẢN XUẤT XE ĐẠP")
    print("="*40)
    
    # Client chỉ cần gọi get_cost() trên đối tượng cấp cao nhất.
    total_bicycle_cost = bicycle.get_cost()

    print("\n" + "="*40)
    print(f"==> TỔNG CHI PHÍ VẬT LIỆU CHO 1 CHIẾC XE ĐẠP LÀ: ${total_bicycle_cost:.2f}")
    print("="*40)