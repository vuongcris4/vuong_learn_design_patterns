import threading

# Chỉ cho phép tạo ra một đối tượng duy nhất. Nếu đối tượng đã tồn tại, hãy trả về chính nó thay vì tạo mới.
class SingletonMeta(type):
    """
    Metaclass này sẽ triển khai logic của Singleton.
    Nó đảm bảo rằng chỉ có một thực thể (instance) của bất kỳ lớp nào
    sử dụng metaclass này được tạo ra.
    Việc sử dụng lock cũng giúp nó an toàn trong môi trường đa luồng (thread-safe).
    """
    _instances = {}
    _lock: threading.Lock = threading.Lock()

    # truyền vào thành tuple, truyền vào thành dictionary
    def __call__(cls, *args, **kwargs):
        # Sử dụng double-checked locking để tối ưu hóa hiệu năng
        # Chỉ khi instance chưa được tạo thì mới cần lock.
        if cls not in cls._instances:
            with cls._lock:
                # Kiểm tra lại một lần nữa bên trong lock để tránh race condition
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

"tham chiếu đến class President và check xem có object nào trong class President chưa?"
class President(metaclass=SingletonMeta):
    """
    Lớp President sử dụng SingletonMeta.
    Bất kể bạn gọi President() bao nhiêu lần, bạn sẽ luôn nhận được
    cùng một đối tượng.
    """
    def __init__(self, name: str):
        # Lưu ý: __init__ vẫn sẽ được gọi mỗi khi bạn cố gắng tạo
        # một instance mới, nhưng metaclass sẽ luôn trả về instance cũ.
        # Logic phức tạp không nên đặt ở đây nếu bạn chỉ muốn nó chạy 1 lần.
        self.name = name
    
    def __str__(self):
        return f"President [Name: {self.name}, ID: {id(self)}]"

# --- Client Code ---
if __name__ == "__main__":
    print("Bắt đầu cuộc họp...")
    
    # Dù gọi khởi tạo 2 lần với các tên khác nhau...
    p1 = President("Mr. Abraham Lincoln")
    p2 = President("Mr. Barack Obama")
    
    # ...chúng ta vẫn sẽ nhận được cùng một đối tượng.
    if id(p1) == id(p2):
        print("p1 và p2 là cùng một người!")
        print(f"Người thứ nhất: {p1}")
        print(f"Người thứ hai: {p2}")
    else:
        print("Lỗi! Singleton đã không hoạt động, có 2 tổng thống được tạo ra.")

    # Kết quả sẽ cho thấy p1 và p2 là một, và tên của tổng thống sẽ là
    # tên được gán trong lần gọi cuối cùng ("Mr. Barack Obama"),
    # vì __init__ vẫn được chạy lại trên cùng một instance.