"""
Colleagues (TextBox, Button...): Rất "ngây thơ". Chúng chỉ biết về trạng thái 
    của bản thân và biết cách báo cáo cho Mediator khi có thay đổi. Chúng không biết gì về nhau.
Mediator (AuthenticationDialog): Là "bộ não". Nó chứa tham chiếu đến tất cả các
    Colleague. Phương thức notify của nó chứa toàn bộ logic điều phối: "OK, TextBox vừa thay đổi, 
    vậy thì tôi phải kiểm tra cả hai ô text rồi ra lệnh cho Button thay đổi trạng thái."
Client: Chỉ cần tạo ra một đối tượng AuthenticationDialog và sau đó mô phỏng
    các hành động trên các thành phần con. Toàn bộ sự tương tác phức tạp được tự động xử lý bởi Mediator.
"""

# mỗi khi gán text, click check box, hay click button đều truyền đến mediator 

from __future__ import annotations # k cần phải viết sender: 'BaseComponent'
from abc import ABC

# --- 1. The Mediator Interface (và lớp Base Colleague) ---
# Mediator sẽ điều phối giao tiếp giữa các Colleague.
class Mediator(ABC):
    # ai gửi, sự kiện gì?
    def notify(self, sender: BaseComponent, event: str):
        pass

class BaseComponent:
    """
    Lớp Colleague cơ sở. Mỗi component sẽ giữ một tham chiếu đến mediator.
    """
    def __init__(self, mediator: Mediator = None):
        self._mediator = mediator

    def set_mediator(self, mediator: Mediator):
        self._mediator = mediator

# --- 2. Concrete Colleagues (Các thành phần cụ thể) ---
# Chúng không biết về nhau, chỉ biết về Mediator.
class TextBox(BaseComponent):
    def __init__(self, mediator=None):
        super().__init__(mediator)
        self._text = ""

    # GET
    @property
    def text(self):
        return self._text

    # SET
    @text.setter
    def text(self, new_text):
        self._text = new_text
        # Khi trạng thái thay đổi, nó thông báo cho Mediator.
        print(f"TextBox: Text changed. Notifying mediator...")
        self._mediator.notify(self, "text_changed")

class Checkbox(BaseComponent):
    def __init__(self, mediator=None):
        super().__init__(mediator)
        self._checked = False
    
    def check(self):
        self._checked = not self._checked
        print("Checkbox: State changed. Notifying mediator...")
        self._mediator.notify(self, "checkbox_changed")

class Button(BaseComponent):
    def __init__(self, mediator=None):
        super().__init__(mediator)
        self.is_enabled = False
    
    def click(self):
        print("Button: Clicked. Notifying mediator...")
        self._mediator.notify(self, "button_clicked")
        # self._mediator.notify là notify trong AuthenticationDialog


# --- 3. The Concrete Mediator (Người điều phối cụ thể) ---
# Mediator chứa tất cả logic phức tạp về sự tương tác.
class AuthenticationDialog(Mediator):
    def __init__(self):
        print("--- Creating Authentication Dialog ---")
        # Mediator tạo và quản lý các Colleague.
        self.username_box = TextBox()
        self.password_box = TextBox()
        self.remember_me_checkbox = Checkbox()
        self.login_button = Button()
        
        # Quan trọng: Nó "tiêm" chính nó vào cho các Colleague.
        # các colleague đều có object Mediator AuthenticationDialog
        self.username_box.set_mediator(self)
        self.password_box.set_mediator(self)
        self.remember_me_checkbox.set_mediator(self)
        self.login_button.set_mediator(self)
        print("Dialog created and components are linked to it.")

    def notify(self, sender: BaseComponent, event: str):
        """Đây là nơi tất cả logic điều phối được tập trung."""
        print(f"Dialog (Mediator): Received event '{event}' from '{type(sender).__name__}'.")
        
        if event == "text_changed":
            # Nếu cả 2 ô có nội dung mới bật nút login.
            if self.username_box.text and self.password_box.text:
                print("Dialog: Both fields have text. Enabling button.")
                self.login_button.is_enabled = True
            else:
                print("Dialog: One or more fields are empty. Disabling button.")
                self.login_button.is_enabled = False
        
        elif event == "button_clicked":
            if self.login_button.is_enabled:
                print("Dialog: Attempting login...")
                # ... (thực hiện logic đăng nhập) ...
            else:
                print("Dialog: Login button is disabled.")

# --- 4. The Client Code ---
if __name__ == "__main__":
    dialog = AuthenticationDialog()
    
    print("\n--- Simulating user actions ---")
    
    # Ban đầu nút Login bị vô hiệu hóa.
    print(f"Login button enabled? {dialog.login_button.is_enabled}")
    dialog.login_button.click()
    
    print("\nUser types username:")
    dialog.username_box.text = "user123"
    print(f"Login button enabled? {dialog.login_button.is_enabled}")

    print("\nUser types password:")
    dialog.password_box.text = "password"
    print(f"Login button enabled? {dialog.login_button.is_enabled}")

    print("\nUser clicks login button:")
    dialog.login_button.click()