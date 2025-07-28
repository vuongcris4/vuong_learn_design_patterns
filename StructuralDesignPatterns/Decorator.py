from abc import ABC, abstractmethod

# --- 1. The Component Interface (Giao diện chung) ---
# Cả dịch vụ cơ bản và các dịch vụ "trang trí" thêm đều phải tuân thủ giao diện này.
class ICarService(ABC):
    @abstractmethod
    def get_cost(self) -> int:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

# --- 2. The Concrete Component (Đối tượng gốc) ---
# Đây là đối tượng cơ bản, cốt lõi mà chúng ta muốn "trang trí".
class BasicInspection(ICarService):
    def get_cost(self) -> int:
        return 50 # Chi phí kiểm tra cơ bản là $50

    def get_description(self) -> str:
        return "Kiểm tra xe cơ bản"

# --- 3. The Base Decorator (Lớp Decorator cơ sở) ---
# Lớp này cũng tuân thủ giao diện, và quan trọng là nó "bọc" một đối tượng ICarService khác.
class CarServiceDecorator(ICarService):
    def __init__(self, service: ICarService):
        self._wrapped_service = service

    def get_cost(self) -> int:
        # Mặc định, nó chỉ ủy quyền lời gọi cho đối tượng được bọc.
        return self._wrapped_service.get_cost()

    def get_description(self) -> str:
        # Mặc định, nó chỉ ủy quyền lời gọi cho đối tượng được bọc.
        return self._wrapped_service.get_description()

# --- 4. Concrete Decorators (Các "lớp vỏ trang trí" cụ thể) ---
# Mỗi lớp này sẽ thêm một chức năng/chi phí mới.
class OilChange(CarServiceDecorator):
    def get_cost(self) -> int:
        # Lấy chi phí của dịch vụ được bọc và CỘNG THÊM chi phí của mình.
        return super().get_cost() + 30

    def get_description(self) -> str:
        # Lấy mô tả của dịch vụ được bọc và NỐI THÊM mô tả của mình.
        return super().get_description() + ", thay dầu"

class TireRotation(CarServiceDecorator):
    def get_cost(self) -> int:
        return super().get_cost() + 20

    def get_description(self) -> str:
        return super().get_description() + ", đảo lốp"

# --- Client Code ---
if __name__ == "__main__":
    # 1. Bắt đầu với một dịch vụ cơ bản
    service: ICarService = BasicInspection()
    print(f"Dịch vụ: '{service.get_description()}' - Chi phí: ${service.get_cost()}")

    # 2. Khách hàng muốn thay dầu. Chúng ta "bọc" dịch vụ hiện tại bằng OilChange decorator.
    """Cấu trúc bây giờ là
    [Đối tượng OilChange]
    - có một thuộc tính _wrapped_service trỏ đến --> [Đối tượng BasicInspection]
    """
    service = OilChange(service)
    print(f"Dịch vụ: '{service.get_description()}' - Chi phí: ${service.get_cost()}")

    # 3. Khách hàng muốn đảo lốp nữa. Chúng ta tiếp tục "bọc" dịch vụ ĐÃ ĐƯỢC BỌC.
    """[Đối tượng TireRotation]
        - có _wrapped_service trỏ đến --> [Đối tượng OilChange]
                                        - có _wrapped_service trỏ đến --> [Đối tượng BasicInspection]
    """
    service = TireRotation(service)
    print(f"Dịch vụ: '{service.get_description()}' - Chi phí: ${service.get_cost()}")
    
    # service._wrapped_service._wrapped_service


"""1. Bắt đầu tại TireRotation.get_cost():

Code của nó là: return super().get_cost() + 20

Để tính được, nó phải gọi super().get_cost(), tức là gọi get_cost() trên đối tượng mà nó đang bọc (_wrapped_service).

Đối tượng nó đang bọc là ai? Là đối tượng OilChange.

Lời gọi self._wrapped_service.get_cost() được thực hiện, và TireRotation đợi kết quả...

2. Chuyển đến OilChange.get_cost():

Code của nó là: return super().get_cost() + 30

Tương tự, nó phải gọi get_cost() trên đối tượng mà nó đang bọc.

Đối tượng nó đang bọc là ai? Là đối tượng BasicInspection.

Lời gọi self._wrapped_service.get_cost() được thực hiện, và OilChange đợi kết quả...

3. Chuyển đến BasicInspection.get_cost():

Đây là đối tượng trong cùng, không bọc ai cả.

Code của nó là: return 50

Nó trả về giá trị 50.

4. Chuỗi trả về (Unwinding):

Giá trị 50 được trả về cho nơi đã gọi nó, tức là OilChange.get_cost().

Biểu thức trong OilChange bây giờ trở thành return 50 + 30. Nó tính toán và trả về 80.

5. Chuỗi trả về tiếp tục:

Giá trị 80 được trả về cho nơi đã gọi nó, tức là TireRotation.get_cost().

Biểu thức trong TireRotation bây giờ trở thành return 80 + 20. Nó tính toán và trả về 100.

6. Kết quả cuối cùng:

Giá trị 100 được trả về cho lời gọi ban đầu của client.
"""