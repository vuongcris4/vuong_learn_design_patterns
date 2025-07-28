from abc import ABC, abstractmethod

# --- 1. The Target Interface (Giao diện mục tiêu) ---
# Đây là giao diện mà hệ thống của bạn (Client) hiểu và mong muốn làm việc cùng.
class INotifier(ABC):
    """
    Hệ thống của chúng ta chỉ làm việc với các đối tượng có phương thức send().
    """
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# --- 2. The Adaptee (Đối tượng cần được 'chuyển đổi') ---
# Đây là một lớp có sẵn, có thể là từ một thư viện bên thứ ba hoặc code cũ.
# Giao diện của nó không tương thích với INotifier.
class SlackService:
    """
    Lớp này gửi thông báo Slack, nhưng có phương thức và tham số khác.
    """
    def post_to_channel(self, channel_id: str, text: str) -> None:
        print(f"SLACK_API: Gửi tin nhắn '{text}' đến kênh '{channel_id}'...")
        # Giả lập việc gọi API của Slack
        print("SLACK_API: Gửi thành công.")

# --- 3. The Adapter (Bộ chuyển đổi) ---
# Lớp này làm cho SlackService tương thích với INotifier.
# Nó thực hiện 2 việc:
#   a. Triển khai giao diện Target (kế thừa từ INotifier).
#   b. "Bọc" (chứa) một đối tượng Adaptee (SlackService).
class SlackAdapter(INotifier):
    def __init__(self, slack_service: SlackService, channel_id: str):
        self._slack_service = slack_service
        self._channel_id = channel_id

    def send(self, message: str) -> None:
        """
        Đây là nơi phép màu xảy ra.
        Phương thức send() nhận một message đơn giản và "dịch" nó
        thành lời gọi phương thức post_to_channel() phức tạp hơn của SlackService.
        """
        print("Adapter: Nhận được yêu cầu send(). Đang chuyển đổi sang Slack API...")
        self._slack_service.post_to_channel(self._channel_id, message)

# --- 4. The Client (Người dùng) ---
# Client không hề biết về sự tồn tại của SlackService.
# Nó chỉ làm việc với giao diện INotifier.
def send_notification(notifier: INotifier, message: str):
    print("Client: Chuẩn bị gửi thông báo quan trọng.")
    notifier.send(message)
    print("Client: Gửi thông báo xong.")

# --- Cách sử dụng ---
if __name__ == "__main__":
    # Tạo đối tượng không tương thích
    slack_service = SlackService()
    
    # Tạo bộ chuyển đổi, "bọc" đối tượng slack_service vào trong nó.
    # Client sẽ làm việc với adapter này.
    slack_adapter = SlackAdapter(slack_service, channel_id="engineering_alerts")
    
    # Client có thể gửi thông báo qua Slack mà không cần biết chi tiết về Slack API.
    # Hàm send_notification chỉ cần một đối tượng tuân thủ giao diện INotifier.
    send_notification(slack_adapter, "Hệ thống sắp hết dung lượng ổ đĩa!")