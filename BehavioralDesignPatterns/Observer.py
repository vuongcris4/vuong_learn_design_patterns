from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

# --- 1. The Subject Interface (Giao diện "Người phát hành") ---
class ISubject(ABC):
    @abstractmethod
    def attach(self, observer: IObserver) -> None:
        """Đính kèm một observer vào subject."""
        pass

    @abstractmethod
    def detach(self, observer: IObserver) -> None:
        """Gỡ bỏ một observer."""
        pass

    @abstractmethod
    def notify(self) -> None:
        """Thông báo cho tất cả observer về một sự thay đổi."""
        pass

# --- 2. The Observer Interface (Giao diện "Người đăng ký") ---
class IObserver(ABC):
    @abstractmethod
    def update(self, subject: ISubject) -> None:
        """Nhận cập nhật từ subject."""
        pass

# --- 3. The Concrete Subject (Chủ thể cụ thể) ---
class JobAgency(ISubject):
    _observers: List[IObserver] = []
    _latest_job_posting: str = None

    def attach(self, observer: IObserver) -> None:
        print("Agency: Một người mới đã đăng ký nhận tin.")
        self._observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        print("Agency: Một người đã hủy đăng ký.")
        self._observers.remove(observer)

    def notify(self) -> None:
        """Kích hoạt việc cập nhật cho mỗi người đăng ký."""
        print("Agency: Đang thông báo cho tất cả người đăng ký...")
        for observer in self._observers:
            observer.update(self)

    def add_job(self, job_posting: str):
        """Hành động làm thay đổi trạng thái của Subject."""
        print(f"\nAgency: Vừa có một công việc mới: '{job_posting}'")
        self._latest_job_posting = job_posting
        # Sau khi trạng thái thay đổi, nó sẽ thông báo cho mọi người.
        self.notify()

# --- 4. The Concrete Observer (Người quan sát cụ thể) ---
class JobSeeker(IObserver):
    def __init__(self, name: str):
        self._name = name

    def update(self, subject: ISubject) -> None:
        """
        Đây là nơi Observer phản ứng lại với thông báo.
        """
        # Kiểm tra để chắc chắn subject là JobAgency
        if isinstance(subject, JobAgency):
            # Lấy trạng thái mới từ subject
            latest_job = subject._latest_job_posting
            print(f"   -> {self._name}: 'Ồ, có việc mới nè: {latest_job}'. Cảm ơn đã thông báo!")


# --- 5. The Client Code ---
if __name__ == "__main__":
    # Tạo ra chủ thể
    job_agency = JobAgency()

    # Tạo ra các người quan sát
    seeker1 = JobSeeker("Alice")
    seeker2 = JobSeeker("Bob")
    seeker3 = JobSeeker("Charlie")

    # Đăng ký nhận tin
    job_agency.attach(seeker1)
    job_agency.attach(seeker2)

    # Chủ thể có sự thay đổi -> tất cả người đăng ký đều nhận được thông báo
    job_agency.add_job("Software Engineer tại Google")

    # Thử thêm một người đăng ký nữa
    job_agency.attach(seeker3)
    
    # Hủy đăng ký của một người
    job_agency.detach(seeker1)

    # Chủ thể lại có sự thay đổi
    job_agency.add_job("Data Scientist tại Meta")
    # Bây giờ chỉ những người còn trong danh sách đăng ký mới nhận được tin