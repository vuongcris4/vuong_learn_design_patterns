"""
kiểu tui có sẵn DataAggregator theo interface IAnalyticsDataSource để generate báo cáo đúng không
mà SalesDatabase thì trả về data type không theo IAnalyticsDataSource nên phải có DatabaseAdapter để trả về data theo IAnalyticsDataSource
"""
from abc import ABC, abstractmethod
import json

# --- Giao diện mà hệ thống của bạn yêu cầu ---
class IAnalyticsDataSource(ABC):
    """Bất kỳ nguồn dữ liệu nào cũng phải có phương thức này."""
    @abstractmethod
    def fetch_metrics(self) -> dict:
        """Trả về một dictionary chứa các số liệu, ví dụ: {'users': 100, 'revenue': 5000}"""
        pass

# --- Lớp tái sử dụng mà bạn KHÔNG muốn sửa đổi ---
class DataAggregator:
    """
    Lớp này nhận một nguồn dữ liệu, lấy số liệu và tạo báo cáo.
    Nó đã được viết, kiểm thử và triển khai. Chúng ta sẽ không đụng vào nó nữa.
    """

    # Tôi chỉ làm việc với những ai cung cấp cho tôi phương thức fetch_metrics()
    def generate_report(self, source: IAnalyticsDataSource):
        print("DataAggregator: Bắt đầu lấy số liệu để tạo báo cáo...")
        # Nó chỉ biết gọi `fetch_metrics()`.
        metrics = source.fetch_metrics()
        
        if metrics:
            print("="*20)
            print("BÁO CÁO HÀNG THÁNG")
            for key, value in metrics.items():
                print(f"- {key.capitalize()}: {value}")
            print("="*20)
        else:
            print("Không thể lấy được số liệu.")


# --- Nguồn dữ liệu không tương thích (Adaptee 1) ---
class SalesDatabase:
    def query_monthly_sales(self) -> list[tuple]:
        # Giả lập việc truy vấn CSDL
        print("(Querying sales database...)")
        return [('new_users', 1570), ('total_revenue', 25000.75)]

# --- Adapter cho SalesDatabase ---
class DatabaseAdapter(IAnalyticsDataSource):
    def __init__(self, database: SalesDatabase):
        self._database = database

    def fetch_metrics(self) -> dict:
        # "Dịch" kết quả từ list of tuples sang dictionary
        data = self._database.query_monthly_sales()
        # Chuyển đổi: [('key1', val1), ('key2', val2)] -> {'key1': val1, 'key2': val2}
        return dict(data)

# --- Sử dụng trong hệ thống ---
print("--- GIAI ĐOẠN 1: TÍCH HỢP CSDL ---")
data_aggregator = DataAggregator()
sales_db = SalesDatabase()
db_adapter = DatabaseAdapter(sales_db)

# Truyền adapter vào lớp lõi. Mọi thứ hoạt động trơn tru.
data_aggregator.generate_report(db_adapter)