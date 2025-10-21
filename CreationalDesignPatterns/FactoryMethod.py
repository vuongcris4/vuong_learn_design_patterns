from abc import ABC, abstractmethod

# --- 1. Product Interface (Sản phẩm trừu tượng) ---
# Định nghĩa chung cho tất cả những người có thể phỏng vấn.
class IInterviewer(ABC):
    @abstractmethod
    def ask_questions(self):
        pass

# --- 2. Concrete Products (Sản phẩm cụ thể) ---
# Các loại người phỏng vấn cụ thể.
class Developer(IInterviewer):
    def ask_questions(self):
        return "Hỏi về các thuật toán và mẫu thiết kế (design patterns)..."

class MarketingSpecialist(IInterviewer):
    def ask_questions(self):
        return "Hỏi về các chiến dịch SEO và phân tích thị trường..."

# --- 3. Creator (Lớp cha trừu tượng) ---
# Lớp này định nghĩa một quy trình chung và một factory method trừu tượng.
class HiringManager(ABC):
    """
    Lớp Creator trừu tượng.
    Nó không biết sẽ tạo ra loại người phỏng vấn nào.
    """

    # Đây chính là Factory Method. Nó là một phương thức trừu tượng.
    @abstractmethod
    def create_interviewer(self) -> IInterviewer:
        """Phương thức này sẽ được các lớp con triển khai."""
        pass

    # Đây là một phương thức nghiệp vụ sử dụng factory method.
    def take_interview(self):
        """
        Quy trình phỏng vấn chung.
        Nó gọi factory method để có được đối tượng người phỏng vấn,
        sau đó làm việc với đối tượng đó.
        """
        # Quan trọng: self.create_interviewer() sẽ gọi phiên bản
        # được định nghĩa ở lớp con.
        interviewer = self.create_interviewer()
        print(f"Người phỏng vấn nói: '{interviewer.ask_questions()}'")

# --- 4. Concrete Creators (Các lớp con cụ thể) ---
# Các lớp này sẽ triển khai factory method để tạo ra sản phẩm cụ thể.
class DevelopmentManager(HiringManager):
    """
    Lớp Concrete Creator, chuyên tuyển vị trí lập trình viên.
    """
    def create_interviewer(self) -> IInterviewer:
        print("Trưởng phòng Kỹ thuật: 'OK, tôi sẽ cử một lập trình viên đi phỏng vấn.'")
        return Developer()

class MarketingManager(HiringManager):
    """
    Lớp Concrete Creator, chuyên tuyển vị trí marketing.
    """
    def create_interviewer(self) -> IInterviewer:
        print("Trưởng phòng Marketing: 'OK, tôi sẽ cử một chuyên gia marketing đi phỏng vấn.'")
        return MarketingSpecialist()


# --- Client Code ---
if __name__ == "__main__":
    # Client quyết định sẽ sử dụng "nhà máy" nào.
    dev_manager = DevelopmentManager()
    mkt_manager = MarketingManager()

    print("Tuyển dụng cho vị trí Lập trình viên:")
    # Client gọi cùng một phương thức `take_interview`...
    dev_manager.take_interview()

    print("\n" + "="*30 + "\n")

    print("Tuyển dụng cho vị trí Chuyên viên Marketing:")
    # ... nhưng kết quả lại khác nhau vì logic đã được ủy quyền cho lớp con.
    mkt_manager.take_interview()

# ---------------------------------------- VD2 ----------------------------------

from abc import ABC, abstractmethod

# --- 1. Product Interface (Sản phẩm trừu tượng) ---
# Định nghĩa các đặc tính chung của một món đồ nội thất.
class IFurniture(ABC):
    @abstractmethod
    def get_description(self):
        """Mô tả sản phẩm."""
        pass

# --- 2. Concrete Products (Sản phẩm cụ thể) ---
# Các loại nội thất cụ thể mà xưởng có thể sản xuất.
class Chair(IFurniture):
    def get_description(self):
        return "Đây là một chiếc ghế gỗ sồi 4 chân."

class Table(IFurniture):
    def get_description(self):
        return "Đây là một chiếc bàn cafe hình tròn."

# --- 3. Creator (Lớp cha trừu tượng - Xưởng sản xuất) ---
# Lớp này định nghĩa quy trình sản xuất chung và một factory method trừu tượng.
class FurnitureFactory(ABC):
    """
    Lớp Creator trừu tượng.
    Nó không biết sẽ tạo ra loại nội thất nào.
    """

    # Đây là Factory Method.
    @abstractmethod
    def create_furniture(self) -> IFurniture:
        """Phương thức này sẽ được các lớp con triển khai để tạo sản phẩm."""
        pass

    # Phương thức nghiệp vụ sử dụng factory method.
    def produce_and_ship(self):
        """
        Quy trình sản xuất và vận chuyển chung.
        Nó gọi factory method để lấy sản phẩm, sau đó làm việc với sản phẩm đó.
        """
        print("Bắt đầu quy trình sản xuất...")
        # self.create_furniture() sẽ gọi phiên bản của lớp con.
        product = self.create_furniture()
        print(f"Sản phẩm đã được tạo: {product.get_description()}")
        print("Đóng gói và vận chuyển sản phẩm đến khách hàng.")

# --- 4. Concrete Creators (Các lớp con cụ thể - Phân xưởng) ---
# Các lớp này sẽ triển khai factory method để tạo ra sản phẩm cụ thể.
class ChairFactory(FurnitureFactory):
    """
    Phân xưởng chuyên sản xuất ghế.
    """
    def create_furniture(self) -> IFurniture:
        print("Phân xưởng ghế: Nhận lệnh sản xuất một chiếc ghế.")
        return Chair()

class TableFactory(FurnitureFactory):
    """
    Phân xưởng chuyên sản xuất bàn.
    """
    def create_furniture(self) -> IFurniture:
        print("Phân xưởng bàn: Nhận lệnh sản xuất một chiếc bàn.")
        return Table()


# --- Client Code (Mã khách hàng sử dụng xưởng) ---
if __name__ == "__main__":
    # Client quyết định sẽ sử dụng "phân xưởng" nào.
    chair_factory = ChairFactory()
    table_factory = TableFactory()

    print("Khách hàng đặt một chiếc ghế:")
    # Client gọi cùng một phương thức `produce_and_ship`...
    chair_factory.produce_and_ship()

    print("\n" + "="*40 + "\n")

    print("Khách hàng đặt một chiếc bàn:")
    # ... nhưng kết quả lại khác nhau vì logic tạo sản phẩm đã được ủy quyền cho lớp con.
    table_factory.produce_and_ship()
