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