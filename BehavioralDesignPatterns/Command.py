"""
Light (receiver): Là đối tượng cuối cùng thực hiện công việc. Nó không biết gì về command hay remote.
ICommand: Interface execute(), undo()
TurnOnCommand/TurnOffCommand (Concrete Commands): Mỗi command là một object nhỏ,
    chỉ có mục đích duy nhất: khi execute được gọi, nó sẽ gọi một phương thức 
    cụ thể của _light (Receiver) mà nó đang giữ
RemoteControl (Invoker): Hoàn toàn tách biệt. Nó không biết "bật đèn" là gì.
    Nó chỉ biết rằng khi nút ON được nhấn, nó sẽ gọi execute() trên bất kì
    command nào được gán cho nút đó.
Client: Kết nối các thành phần lại với nhau

Bóng đèn chỉ biết On/Off
ConcreteCommand biết gọi đến On/Off của từng object bóng đèn (hồng ngoại) (_Receiver)
Invoker biết nhấn nút thì thực hiện phương thức của command nào
"""


from abc import ABC, abstractmethod

# --- 1. The Receiver (Người thực hiện lệnh) ---
# Lớp này chứa logic nghiệp vụ thực tế.
class Light:
    def __init__(self, location: str):
        self.location = location

    def turn_on(self):
        print(f"Đèn ở '{self.location}' đã bật.")

    def turn_off(self):
        print(f"Đèn ở '{self.location}' đã tắt.")

# --- 2. The Command Interface (Giao diện Mệnh lệnh) ---
class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass

# --- 3. Concrete Commands (Các Mệnh lệnh cụ thể) ---
# Mỗi command sẽ "bọc" một hành động của Receiver.
class TurnOnCommand(ICommand):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_on()

    def undo(self) -> None:
        self._light.turn_off()

class TurnOffCommand(ICommand):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_off()
    
    def undo(self) -> None:
        self._light.turn_on()

# --- 4. The Invoker (Người kích hoạt lệnh) ---
# Lớp này không biết gì về Light. Nó chỉ biết về ICommand.
class RemoteControl:
    def __init__(self):
        self._on_command: ICommand = None
        self._off_command: ICommand = None
        self._undo_command: ICommand = None # Để theo dõi lệnh cuối cùng

    def set_command(self, on_command: ICommand, off_command: ICommand):
        self._on_command = on_command
        self._off_command = off_command

    def press_on_button(self):
        print("Remote: Nhấn nút ON...")
        self._on_command.execute()
        self._undo_command = self._on_command # Lưu lại để undo

    def press_off_button(self):
        print("Remote: Nhấn nút OFF...")
        self._off_command.execute()
        self._undo_command = self._off_command # Lưu lại để undo

    def press_undo_button(self):
        print("Remote: Nhấn nút UNDO...")
        if self._undo_command:
            self._undo_command.undo()
            self._undo_command = None # Chỉ undo được 1 lần

# --- 5. The Client Code ---
if __name__ == "__main__":
    # Client là người thiết lập mọi thứ
    
    # 1. Tạo Receiver
    living_room_light = Light("Phòng khách")

    # 2. Tạo các Command cụ thể và gán Receiver cho chúng
    light_on = TurnOnCommand(living_room_light)
    light_off = TurnOffCommand(living_room_light)

    # 3. Tạo Invoker
    remote = RemoteControl()

    # 4. Cấu hình Invoker với các Command
    remote.set_command(light_on, light_off)
    
    # 5. Bắt đầu sử dụng
    remote.press_on_button()
    remote.press_off_button()
    
    print("\n--- Thử chức năng Undo ---")
    # Lệnh cuối cùng là TẮT đèn. Undo sẽ BẬT lại đèn.
    remote.press_undo_button()

    print("\n--- Thử lại ---")
    remote.press_on_button()
    # Lệnh cuối cùng là BẬT đèn. Undo sẽ TẮT đèn.
    remote.press_undo_button()