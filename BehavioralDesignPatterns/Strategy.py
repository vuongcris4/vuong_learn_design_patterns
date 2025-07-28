"""
Mẫu Strategy có cấu trúc khá giống với một số mẫu khác (như Bridge) ở chỗ nó ưu tiên composition hơn là inheritance, nhưng mục đích của nó rất khác biệt.
Ý tưởng cốt lõi là: khi một tác vụ có thể được thực hiện bằng nhiều thuật toán (hay "chiến lược") khác nhau, hãy đóng gói mỗi thuật toán đó vào một lớp riêng biệt. Tất cả các lớp "chiến lược" này sẽ tuân thủ một giao diện (interface) chung.
Một đối tượng chính (gọi là Context) sẽ không tự mình thực hiện thuật toán. Thay vào đó, nó sẽ giữ một tham chiếu đến một trong các đối tượng chiến lược đó. Khi cần thực hiện tác vụ, nó sẽ ủy quyền công việc cho đối tượng chiến lược mà nó đang giữ.
Điều tuyệt vời là client có thể thay đổi chiến lược bên trong Context bất cứ lúc nào tại thời điểm chạy.
Các "diễn viên" chính
- Strategy (Interface): Định nghĩa một phương thức chung mà tất cả các thuật toán/chiến lược phải có.
- Concrete Strategy: Các lớp cụ thể, mỗi lớp triển khai một thuật toán riêng biệt.
- Context: Đối tượng sử dụng một chiến lược. Nó giữ một tham chiếu đến một đối tượng Strategy và có thể thay đổi nó.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

# --- 1. The Strategy Interface (Giao diện cho các chiến lược) ---
class ISortStrategy(ABC):
    """
    Giao diện chung cho tất cả các thuật toán sắp xếp.
    """
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

# --- 2. Concrete Strategies (Các chiến lược cụ thể) ---
# Mỗi lớp này đóng gói một thuật toán cụ thể.
class BubbleSortStrategy(ISortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("Đang sắp xếp bằng Bubble Sort (tốt cho dữ liệu nhỏ)...")
        # Giả lập thuật toán bubble sort, không cần triển khai chi tiết
        # Trong thực tế, đây sẽ là logic của bubble sort
        return sorted(data)

class QuickSortStrategy(ISortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("Đang sắp xếp bằng Quick Sort (tốt cho dữ liệu lớn)...")
        # Giả lập thuật toán quick sort
        return sorted(data)

# --- 3. The Context (Đối tượng sử dụng chiến lược) ---
# Lớp này không biết về chi tiết của các thuật toán.
class Sorter:
    def __init__(self, strategy: ISortStrategy):
        # Context được khởi tạo với một chiến lược mặc định.
        self._strategy = strategy

    def set_strategy(self, strategy: ISortStrategy):
        """Cho phép thay đổi chiến lược tại thời điểm chạy."""
        print("--- Thay đổi chiến lược sắp xếp ---")
        self._strategy = strategy

    def execute_sort(self, data: List[int]) -> List[int]:
        """Context ủy quyền công việc sắp xếp cho đối tượng chiến lược của nó."""
        print("Context: Bắt đầu quá trình sắp xếp.")
        # Nó chỉ gọi phương thức sort() chung, không cần biết đó là thuật toán nào.
        result = self._strategy.sort(data)
        print(f"Context: Sắp xếp hoàn tất. Kết quả: {result}")
        return result

# --- 4. The Client Code ---
if __name__ == "__main__":
    # Client là người quyết định chiến lược nào sẽ được sử dụng.
    
    # Kịch bản 1: Dữ liệu nhỏ
    small_dataset = [5, 1, 4, 2, 8]
    print(f"--- Xử lý tập dữ liệu nhỏ: {small_dataset} ---")
    
    # Client chọn chiến lược phù hợp
    bubble_sorter = Sorter(BubbleSortStrategy())
    bubble_sorter.execute_sort(small_dataset)

    print("\n" + "="*50 + "\n")

    # Kịch bản 2: Dữ liệu lớn
    large_dataset = [int(i) for i in range(15, 0, -1)]
    print(f"--- Xử lý tập dữ liệu lớn: {large_dataset} ---")
    
    # Client chọn một chiến lược khác
    quick_sorter = Sorter(QuickSortStrategy())
    quick_sorter.execute_sort(large_dataset)
    
    print("\n" + "="*50 + "\n")

    # Kịch bản 3: Thay đổi chiến lược tại thời điểm chạy
    print("--- Xử lý lại tập dữ liệu nhỏ, nhưng thay đổi chiến lược ---")
    # Ban đầu dùng Quick Sort
    sorter = Sorter(QuickSortStrategy())
    sorter.execute_sort(small_dataset.copy()) # Dùng quick sort
    
    # Sau đó, client quyết định rằng Bubble Sort tốt hơn và thay đổi chiến lược
    sorter.set_strategy(BubbleSortStrategy())
    sorter.execute_sort(small_dataset.copy()) # Bây giờ lại dùng bubble sort