from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

# --- 1. The Handler Interface (Giao diện chung cho các "mắt xích") ---
class IHandler(ABC):
    @abstractmethod
    def set_next(self, handler: IHandler) -> IHandler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass

# --- 2. The Abstract Handler (Lớp cha trừu tượng cho các mắt xích) ---
# Lớp này chứa logic chung về việc "chuyển tiếp" yêu cầu.
"""
self._next_handler trong set_next không liên quan gì với _next_handler
luôn tìm trong đối tượng (self) trước, nếu không thấy mới tìm lên lớp (cls).
"""
class AbstractHandler(IHandler):
    _next_handler: Optional[IHandler] = None

    def set_next(self, handler: IHandler) -> IHandler:
        self._next_handler = handler
        # Trả về handler tiếp theo để có thể gọi nối tiếp (chaining)
        # Ví dụ: a.set_next(b).set_next(c)
        return handler

    def handle(self, request) -> Optional[str]:
        # Nếu có mắt xích tiếp theo, hãy chuyển yêu cầu cho nó.
        if self._next_handler:
            return self._next_handler.handle(request)
        
        # Nếu là mắt xích cuối cùng, không làm gì cả.
        return None

# --- 3. Concrete Handlers (Các "mắt xích" cụ thể) ---
# Mỗi lớp này sẽ triển khai logic xử lý của riêng nó.
class Account(AbstractHandler):
    def __init__(self, name: str, balance: float):
        self._name = name
        self._balance = balance

    def handle(self, amount: float) -> Optional[str]:
        """
        Cố gắng xử lý yêu cầu (thanh toán). Nếu không thể, chuyển cho mắt xích tiếp theo.
        """
        if self._balance >= amount:
            print(f"==> Tài khoản '{self._name}' đã thanh toán ${amount}.")
            return f"Thanh toán thành công bởi tài khoản {self._name}"
        else:
            print(f"Tài khoản '{self._name}' không đủ số dư (còn ${self._balance}). Chuyển tiếp...")
            # Gọi logic "chuyển tiếp" của lớp cha.
            return super().handle(amount)

# --- 4. The Client Code ---
if __name__ == "__main__":
    # Tạo ra các mắt xích
    account_a = Account(name="A (Ưu tiên 1)", balance=100)
    account_b = Account(name="B (Ưu tiên 2)", balance=300)
    account_c = Account(name="C (Ưu tiên 3)", balance=1000)

    # Xây dựng chuỗi trách nhiệm: A -> B -> C
    account_a.set_next(account_b).set_next(account_c)

    # Client chỉ cần biết đến mắt xích đầu tiên (account_a).
    # Nó không cần biết ai sẽ thực sự xử lý yêu cầu.
    
    print("--- Kịch bản 1: Mua món hàng giá $210 ---")
    # Yêu cầu được gửi đến A. A không xử lý được, chuyển cho B. B xử lý được.
    result = account_a.handle(210)
    if not result:
        print("==> Không có tài khoản nào đủ khả năng thanh toán.\n")

    print("\n" + "="*40 + "\n")
    
    print("--- Kịch bản 2: Mua món hàng giá $75 ---")
    # Yêu cầu được gửi đến A. A xử lý được ngay. Chuỗi dừng lại.
    result = account_a.handle(75)
    if not result:
        print("==> Không có tài khoản nào đủ khả năng thanh toán.\n")

    print("\n" + "="*40 + "\n")

    print("--- Kịch bản 3: Mua món hàng giá $1500 ---")
    # Yêu cầu đi hết chuỗi từ A -> B -> C mà không ai xử lý được.
    result = account_a.handle(1500)
    if not result:
        print("==> Không có tài khoản nào đủ khả năng thanh toán.\n")