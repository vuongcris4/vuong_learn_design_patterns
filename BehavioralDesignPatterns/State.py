from __future__ import annotations
from abc import ABC, abstractmethod

# --- 1. The Context ---
# Lớp này giữ một tham chiếu đến một trạng thái cụ thể và ủy quyền công việc cho nó.
class Document:
    _state: IState = None # Trạng thái hiện tại của tài liệu

    def __init__(self, state: IState):
        self.transition_to(state)

    def transition_to(self, state: IState):
        """Context cho phép các đối tượng State thay đổi trạng thái của nó."""
        print(f"Context: Chuyển sang trạng thái {type(state).__name__}.")
        self._state = state
        self._state.set_context(self)

    # Context ủy quyền các hành động cho đối tượng state.
    def render(self):
        self._state.render()

    def publish(self):
        self._state.publish()

# --- 2. The State Interface (Giao diện chung cho các trạng thái) ---
class IState(ABC):
    @property
    def context(self) -> Document:
        return self._context

    def set_context(self, context: Document):
        self._context = context

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def publish(self) -> None:
        pass

# --- 3. Concrete States (Các trạng thái cụ thể) ---
# Mỗi lớp này triển khai hành vi cho một trạng thái cụ thể.

class DraftState(IState):
    def render(self) -> None:
        print("Đang hiển thị tài liệu ở chế độ BẢN NHÁP (có watermark).")

    def publish(self) -> None:
        print("Tài liệu được gửi đi để kiểm duyệt...")
        # Khi publish, nó sẽ chuyển context sang trạng thái Moderation.
        self.context.transition_to(ModerationState())

class ModerationState(IState):
    def render(self) -> None:
        print("Đang hiển thị tài liệu ở chế độ CHỜ DUYỆT (chỉ cho người duyệt xem).")

    def publish(self) -> None:
        print("Tài liệu đã được duyệt và xuất bản!")
        # Sau khi được duyệt, nó chuyển context sang trạng thái Published.
        self.context.transition_to(PublishedState())

class PublishedState(IState):
    def render(self) -> None:
        print("Đang hiển thị tài liệu đã XUẤT BẢN cho công chúng.")

    def publish(self) -> None:
        # Khi đã ở trạng thái này, không thể publish lại.
        print("Lỗi: Tài liệu đã được xuất bản rồi.")

# --- 4. The Client Code ---
if __name__ == "__main__":
    # Client tạo một tài liệu mới, ban đầu ở trạng thái Draft.
    document = Document(DraftState())
    
    print("\n--- Trạng thái ban đầu: Draft ---")
    document.render() # Hiển thị theo kiểu Draft

    print("\n--- Hành động: Publish lần 1 ---")
    document.publish() # Sẽ chuyển trạng thái sang Moderation
    
    print("\n--- Trạng thái hiện tại: Moderation ---")
    document.render() # Hiển thị theo kiểu Moderation
    document.render() # Hiển thị theo kiểu Moderation

    print("\n--- Hành động: Publish lần 2 ---")
    document.publish() # Sẽ chuyển trạng thái sang Published
    
    print("\n--- Trạng thái cuối cùng: Published ---")
    document.render() # Hiển thị theo kiểu Published
    
    print("\n--- Hành động: Publish lần 3 ---")
    document.publish() # Sẽ báo lỗi

"""
draftState = DraftState()
Đầu tiên document = Document(draftState)
thì nhảy vào __init__ của document,
truyền state = draftState vào và gọi self.transition_to(state) thì
document có instance property self._state là draftState
self._state.set_context(self) là truyền document vào draftState để tham chiếu ngược

nghĩa là khi gán document = Document(DraftState()) thì DraftState() đã tự động tham chiếu tới document

self._state đang ở draftState vậy nên
khi gọi document.render() thì lấy State hiện tại và gọi render() của state hiện tại.

gọi document.publish() thì lấy State hiện tại và gọi publish() của state hiện tại.

self.context.transition_to(ModerationState()) là
document.transition_to(ModerationState())

mỗi state là một object, document delegation đến các state chuyển đổi
"""