from abc import ABC, abstractmethod

# --- 1. Abstract Products (Các giao diện sản phẩm trừu tượng) ---
# Giao diện cho sản phẩm thứ nhất: Cửa
class IDoor(ABC):
    @abstractmethod
    def get_description(self):
        pass

# Giao diện cho sản phẩm thứ hai: Chuyên gia lắp đặt
class IInstallationExpert(ABC):
    @abstractmethod
    def get_description(self):
        pass

# --- 2. Concrete Products (Các sản phẩm cụ thể) ---
# Chúng được nhóm theo "gia đình".

# Gia đình sản phẩm GỖ
class WoodenDoor(IDoor):
    def get_description(self):
        return "Cửa gỗ sồi."

class Carpenter(IInstallationExpert):
    def get_description(self):
        return "Tôi là thợ mộc, chuyên lắp cửa gỗ."

# Gia đình sản phẩm SẮT
class IronDoor(IDoor):
    def get_description(self):
        return "Cửa sắt chống cháy."

class Welder(IInstallationExpert):
    def get_description(self):
        return "Tôi là thợ hàn, chuyên lắp cửa sắt."

# --- 3. Abstract Factory (Giao diện nhà máy trừu tượng) ---
# Giao diện này định nghĩa các phương thức để tạo ra một gia đình sản phẩm.
class IDoorFactory(ABC):
    @abstractmethod
    def create_door(self) -> IDoor:
        pass

    @abstractmethod
    def create_expert(self) -> IInstallationExpert:
        pass

# --- 4. Concrete Factories (Các nhà máy cụ thể) ---
# Mỗi nhà máy cụ thể sẽ tạo ra một gia đình sản phẩm cụ thể và tương thích.

class WoodenDoorFactory(IDoorFactory):
    """Nhà máy này tạo ra bộ sản phẩm liên quan đến GỖ."""
    def create_door(self) -> IDoor:
        return WoodenDoor()

    def create_expert(self) -> IInstallationExpert:
        return Carpenter()

class IronDoorFactory(IDoorFactory):
    """Nhà máy này tạo ra bộ sản phẩm liên quan đến SẮT."""
    def create_door(self) -> IDoor:
        return IronDoor()

    def create_expert(self) -> IInstallationExpert:
        return Welder()

# --- 5. Client Code ---
# Client làm việc với các nhà máy và sản phẩm thông qua giao diện trừu tượng.
def client_code(factory: IDoorFactory):
    """
    Client không biết và không cần quan tâm đến loại nhà máy cụ thể.
    Nó chỉ biết nhà máy có thể tạo ra cửa và chuyên gia.
    """
    door = factory.create_door()
    expert = factory.create_expert()

    print(f"   - Sản phẩm: {door.get_description()}")
    print(f"   - Chuyên gia lắp đặt: {expert.get_description()}")

if __name__ == "__main__":
    print("Client yêu cầu bộ sản phẩm GỖ:")
    # Client chọn nhà máy đồ gỗ
    wooden_factory = WoodenDoorFactory()
    client_code(wooden_factory)

    print("\n" + "="*40 + "\n")

    print("Client yêu cầu bộ sản phẩm SẮT:")
    # Client chọn nhà máy đồ sắt
    iron_factory = IronDoorFactory()
    client_code(iron_factory)