# --- 2. The Memento (Vật ghi nhớ) ---
# Nó chỉ là một object chứa dữ liệu, không có logic phức tạp.
class EditorMemento:
    def __init__(self, content: str):
        # Thuộc tính `_content` này là "riêng tư", chỉ Originator mới nên biết.
        self._content = content

    def get_saved_content(self) -> str:
        # Phương thức này để Originator lấy lại trạng thái đã lưu.
        return self._content

# --- 1. The Originator (Đối tượng có trạng thái cần lưu) ---
class TextEditor:
    def __init__(self):
        self._content = ""

    def write(self, text: str):
        self._content += text

    def get_content(self) -> str:
        return self._content

    def save(self) -> EditorMemento:
        """Tạo ra một Memento chứa ảnh chụp trạng thái hiện tại."""
        print("Editor: Đang lưu trạng thái...")
        return EditorMemento(self._content)

    def restore(self, memento: EditorMemento):
        """Khôi phục lại trạng thái từ một Memento."""
        self._content = memento.get_saved_content()
        print("Editor: Đã khôi phục trạng thái.")

# --- 3. The Caretaker (Người trông coi các Memento) ---
# Lớp này không bao giờ được phép xem nội dung của Memento.
class HistoryManager:
    def __init__(self, editor: TextEditor):
        self._editor = editor
        self._history: list[EditorMemento] = []

    def backup(self):
        """Yêu cầu editor tạo snapshot và cất vào lịch sử."""
        print("\nHistory: Sao lưu trạng thái hiện tại của editor.")
        self._history.append(self._editor.save())

    def undo(self):
        """Lấy snapshot cuối cùng ra khỏi lịch sử và yêu cầu editor khôi phục."""
        if not self._history:
            print("History: Không còn gì để undo.")
            return

        memento = self._history.pop()
        print("History: Đang khôi phục trạng thái trước đó...")
        self._editor.restore(memento)

# --- Client Code ---
if __name__ == "__main__":
    # Thiết lập các "diễn viên"
    editor = TextEditor()            # Originator
    history = HistoryManager(editor) # Caretaker

    # --- Mô phỏng hành động của người dùng ---
    
    # 1. Gõ chữ "A"
    history.backup() # Lưu trạng thái "" (trống)
    editor.write("A")
    print(f"Nội dung hiện tại: '{editor.get_content()}'")
    
    # 2. Gõ thêm chữ "B"
    history.backup() # Lưu trạng thái "A"
    editor.write("B")
    print(f"Nội dung hiện tại: '{editor.get_content()}'")

    # 3. Gõ thêm chữ "C"
    history.backup() # Lưu trạng thái "AB"
    editor.write("C")
    print(f"Nội dung hiện tại: '{editor.get_content()}'")

    print("\n" + "="*20 + " BẮT ĐẦU UNDO " + "="*20)
    
    # Thực hiện Undo lần 1
    history.undo()
    print(f"Sau khi undo 1 lần: '{editor.get_content()}'") # Mong đợi: "AB"

    # Thực hiện Undo lần 2
    history.undo()
    print(f"Sau khi undo 2 lần: '{editor.get_content()}'") # Mong đợi: "A"

    # Thực hiện Undo lần 3
    history.undo()
    print(f"Sau khi undo 3 lần: '{editor.get_content()}'") # Mong đợi: "" (trống)
    
    # Thử undo lần nữa
    history.undo()